import os
import shutil
import subprocess
import concurrent.futures
import numpy as np
from scipy import signal
import utils
import json
import plots
import sys


def execute_simulation(
    k, m, A, l0, N, w, i, dt, dt2, tf, memory, root_dir="data/simulations"
):

    name = f"w-{w}_k-{k}"
    unique_dir = os.path.join(root_dir, name)

    # If unique dir exists return it
    if os.path.exists(unique_dir):
        return unique_dir

    os.makedirs(unique_dir, exist_ok=True)

    command = [
        "java",
        f"-Xms{memory}",
        f"-Xmx{memory}",
        "-jar",
        "target/coupled-oscillator-jar-with-dependencies.jar",
        "-out",
        unique_dir,
        "-k",
        str(k),
        "-m",
        str(m),
        "-A",
        str(A),
        "-l0",
        str(l0),
        "-N",
        str(N),
        "-w",
        str(w),
        "-i",
        i,
        "-dt",
        str(dt),
        "-dt2",
        str(dt2),
        "-tf",
        str(tf),
    ]

    try:
        print(f"[WORKER] - Running simulation, w={w}, k={k}")
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"[WORKER] - Simulation finished, w={w}, k={k}")
    except subprocess.CalledProcessError as e:
        print(f"[WORKER] - Error running simulation, w={w}, k={k}")
        print(f"[WORKER] - {e.stderr}")

    return unique_dir


def execute_simulations(
    m,
    A,
    l0,
    N,
    i,
    k_params,
    combinations_to_animate,
    simulation_dir="data/simulations",
    memory=1500,
    max_workers=4,
):

    print("Executing simulations")

    dirs = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(
                execute_simulation,
                k,
                m,
                A,
                l0,
                N,
                w,
                i,
                params["dt"],
                params["dt2"],
                params["tf"],
                f"{memory}m",
                root_dir=simulation_dir,
            )
            for k, params in k_params.items()
            for w in params["ws"]
        ]

        jobs = len(futures)
        completed = 0

        results = []
        for future in concurrent.futures.as_completed(futures):
            try:
                dir = future.result()
                dirs.append(dir)
                print(f"[MAIN {completed + 1}/{jobs}] - Parsing results from {dir}")

                static_file = os.path.join(dir, "static.txt")
                dynamic_file = os.path.join(dir, "dynamic.txt")

                static_data = utils.parse_static_file_coupled(static_file)
                time, positions = utils.parse_dynamic_file(dynamic_file)

                amplitudes = utils.calculate_amplitudes(positions)

                # Convert to python lists
                result = (
                    {
                        "parameters": static_data,
                        "time": list(time),
                        "amplitudes": list(amplitudes),
                        "positions": [list(p) for p in positions],
                        "k": static_data["K"],
                        "w": static_data["W"],
                    }
                    if (static_data["K"], static_data["W"]) in combinations_to_animate
                    else {
                        "parameters": static_data,
                        "time": list(time),
                        "amplitudes": list(amplitudes),
                        "k": static_data["K"],
                        "w": static_data["W"],
                    }
                )

                results.append(result)
                print(f"[MAIN {completed + 1}/{jobs}] - Results parsed from {dir}")
                completed += 1
            except Exception as e:
                print(f"[MAIN {completed + 1}/{jobs}] - Error parsing results: {e}")

    try:
        print("Removing simulation directories")
        shutil.rmtree(simulation_dir)
    except Exception as e:
        print(f"Error removing simulation directories: {e}")

    return results


def plot_results(results, output_dir="data/"):

    print("Plotting results")

    # dict of k -> (w, max_amplitude)
    max_amplitudes = {}

    # Create output directories
    os.makedirs(os.path.join(output_dir, "amplitudes_vs_time"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "amplitudes_vs_w"), exist_ok=True)

    for result in results:
        amplitudes = result["amplitudes"]
        w = result["w"]
        k = result["k"]

        # Plot the amplitudes over time
        plots.plot_amplitudes_vs_time(
            result["time"],
            amplitudes,
            os.path.join(
                output_dir, "amplitudes_vs_time", f"amplitudes_vs_time_k-{k}_w-{w}.png"
            ),
        )

        if k not in max_amplitudes:
            max_amplitudes[k] = []

        if len(amplitudes) > 0:
            max_amplitudes[k].append((w, max(amplitudes)))

    resonances = []

    for k, data in max_amplitudes.items():
        ws = []
        amplitudes = []

        for w, amplitude in sorted(data, key=lambda x: x[0]):
            ws.append(w)
            amplitudes.append(amplitude)

        plots.plot_amplitudes_vs_w(
            ws,
            amplitudes,
            os.path.join(output_dir, "amplitudes_vs_w", f"amplitudes_vs_w_k-{k}.png"),
        )

        peaks, _ = signal.find_peaks(amplitudes)

        top_3_peaks = sorted(peaks, key=lambda x: amplitudes[x], reverse=True)[:3]
        top_3_ws = [ws[i] for i in top_3_peaks]
        w0 = min(top_3_ws)

        resonances.append((k, w0))

    ks = [k for k, _ in sorted(resonances, key=lambda x: x[0])]
    ws = [w for _, w in sorted(resonances, key=lambda x: x[0])]

    plots.plot_resonances_vs_k(
        ks,
        ws,
        os.path.join(output_dir, "resonances.png"),
    )

    # Try to do regression (raiz)
    constants = np.linspace(0.098, 0.101, num=100)
    cuadratic_errors = []
    for constant in constants:
        cuadratic_error = 0
        for k, w in zip(ks, ws):
            cuadratic_error += (w - constant * np.sqrt(k)) ** 2

        cuadratic_errors.append(cuadratic_error)

    best_constant = constants[cuadratic_errors.index(min(cuadratic_errors))]

    plots.plot_resonance_with_best_constant_vs_k(
        ks,
        ws,
        best_constant,
        os.path.join(output_dir, "resonance.png"),
    )

    plots.plot_cuadratic_error_vs_constant(
        constants,
        cuadratic_errors,
        os.path.join(output_dir, "cuadratic_error.png"),
    )

    print("Results plotted")


from matplotlib.animation import FuncAnimation, FFMpegWriter
import matplotlib.pyplot as plt


def animate(positions, l0, omega, dt, A, output_file="data/animation.mp4"):
    # Convert positions to a NumPy array for easier indexing
    positions = np.array(positions)

    # Number of particles is the length of each snapshot
    num_particles = positions.shape[1]

    # Fixed x-coordinates based on L0 separation
    x_coords = np.arange(num_particles) * l0

    # Set up the figure and axis
    fig, ax = plt.subplots()
    ax.set_xlim(
        -2 * l0, l0 * num_particles
    )  # Fixed x-limits based on particle separation
    min_y = min(positions.flatten())
    max_y = max(positions.flatten())
    extra = (max_y - min_y) / 5
    ax.set_ylim(
        min_y - extra, max_y + extra
    )  # Dynamic y-limits based on particle movement

    # Initialize the scatter plot for particles
    (particles,) = ax.plot([], [], "bo", ms=1)  # 'bo' means blue circles

    # Line objects for connecting particles and the wall
    (particle_lines,) = ax.plot([], [], "b-", lw=1)  # Lines between particles
    (wall_line,) = ax.plot([], [], "b-", lw=1)
    # Forced particle that follows the A * sin(ωt) function
    # Initialize the particle at the leftmost particle's position
    (forced_particle,) = ax.plot([-l0], [0], "go", ms=2)

    frames = len(positions)

    def update(frame):
        # Print progress every 5% of frames, if frames is greater than 20
        if frames > 20 and frame % (frames // 20) == 0:
            print(f"Progress: {frame / frames * 100:.1f}%")

        # Update particle positions
        particles.set_data(x_coords, positions[frame])  # Fixed x, dynamic y

        # Update lines between particles
        particle_lines.set_data(x_coords, positions[frame])  # Connect particles

        # Update line to the wall at y=0 from the rightmost particle
        wall_line.set_data(
            [x_coords[-1], x_coords[-1] + l0], [positions[frame][-1], 0]
        )  # Rightmost particle to wall

        # Update the forced particle
        t = frame * dt
        forced_particle.set_data([-l0], [A * np.sin(omega * t)])

        return particles, particle_lines, wall_line, forced_particle

    # Number of frames equals the number of snapshots
    frames = len(positions)

    # Create the animation
    ani = FuncAnimation(fig, update, frames=frames, interval=100, blit=True)

    # Save the animation as an MP4 file
    writer = FFMpegWriter(fps=10, metadata=dict(artist="Me"), bitrate=1800)
    ani.save(output_file, writer=writer)

    plt.close()  # Close the figure to avoid displaying it in interactive mode


if __name__ == "__main__":

    # First and only argument is directory
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print(
            "Usage: python dampened_oscillator.py <generate|plot|animate> [directory]"
        )
        sys.exit(1)

    output_dir = sys.argv[2] if len(sys.argv) == 3 else "data/"

    if sys.argv[1] == "generate":
        expected_resonances = [
            1.0157894736842106,
            4.4447368421052635,
            6.290263157894737,
            8.315263157894737,
            9.929736842105264,
        ]
        k_params = {
            100: {
                "ws": utils.generate_frequencies(1, 100),
                "dt": 0.0001,
                "dt2": 0.01,
                "tf": 50,
            },
            2000: {
                "ws": utils.generate_frequencies(4.45, 100),
                "dt": 0.0001,
                "dt2": 0.01,
                "tf": 50,
            },
            4000: {
                "ws": utils.generate_frequencies(6.285, 100),
                "dt": 0.0001,
                "dt2": 0.01,
                "tf": 50,
            },
            7000: {
                "ws": utils.generate_frequencies(8.31, 100),
                "dt": 0.0001,
                "dt2": 0.01,
                "tf": 50,
            },
            10000: {
                "ws": utils.generate_frequencies(9.935, 100),
                "dt": 0.0001,
                "dt2": 0.01,
                "tf": 50,
            },
        }

        combinations_to_animate = []
        for expected_resonance, k in zip(expected_resonances, k_params.keys()):
            for harmonic in range(1, 4):
                res_w = harmonic * expected_resonance
                closest_w = min(k_params[k]["ws"], key=lambda w: abs(w - res_w))
                if abs(closest_w - res_w) < 0.1:
                    combinations_to_animate.append((k, closest_w))

        results = execute_simulations(
            m=0.001,
            A=0.01,
            l0=0.001,
            N=1000,
            i="verlet",
            k_params=k_params,
            combinations_to_animate=combinations_to_animate,
            simulation_dir=os.path.join(output_dir, "simulations"),
            memory=1792,
            max_workers=8,
        )

        print("Saving results")

        with open(os.path.join(output_dir, "results.json"), "w") as f:
            json.dump(results, f)

    elif sys.argv[1] == "plot":
        print("Loading results")
        with open(os.path.join(output_dir, "results.json"), "r") as f:
            results = json.load(f)

        plot_results(results, output_dir=output_dir)
    elif sys.argv[1] == "animate":
        print("Loading results")
        with open(os.path.join(output_dir, "results.json"), "r") as f:
            results = json.load(f)

        animated = False
        os.makedirs(os.path.join(output_dir, "animations"), exist_ok=True)

        for result in results:
            if "positions" in result:
                print(f"Animating k={result['k']} w={result['w']}")
                animate(
                    result["positions"],
                    result["parameters"]["L0"],
                    result["parameters"]["W"],
                    result["parameters"]["Dt2"],
                    result["parameters"]["A"],
                    output_file=os.path.join(
                        output_dir,
                        "animations",
                        f"animation_{result['k']}_{result['w']}.mp4",
                    ),
                )
                animated = True

        if not animated:
            print("No results with positions found")
            sys.exit(1)

    else:
        print("Usage: python dampened_oscillator.py <generate|plot>")
        sys.exit(1)
