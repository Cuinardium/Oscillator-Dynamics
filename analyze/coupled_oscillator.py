import os
import shutil
import subprocess
import concurrent.futures
import numpy as np
import utils
import json
import plots
import sys


def execute_simulation(
    k, m, A, l0, N, w, i, dt, dt2, tf, memory, root_dir="data/simulations"
):

    name = f"w-{w}_k-{k}"
    unique_dir = os.path.join(root_dir, name)

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
        print(f"Running simulation, w={w}, k={k}")
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Simulation finished, w={w}, k={k}")
    except subprocess.CalledProcessError as e:
        print(f"Error running simulation, w={w}, k={k}")
        print(f"Error: {e.stderr}")

    return unique_dir


def execute_simulations(
    m,
    A,
    l0,
    N,
    i,
    dt,
    tf,
    ws,
    ks,
    simulation_dir="data/simulations",
    memory=6,
    max_workers=4,
):

    print("Executing simulations")

    dirs = []
    memory = memory // max_workers

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
                dt,
                0.01 if dt <= 0.01 else dt,
                tf if k > 100 else 100,
                f"{memory}G",
                root_dir=simulation_dir,
            )
            for k in ks
            for w in ws
        ]

        for future in concurrent.futures.as_completed(futures):
            try:
                dir = future.result()
                dirs.append(dir)
            except Exception as e:
                print(f"Error: {e}")

    results = []

    for dir in dirs:

        try:
            print(f"Parsing results from {dir}")

            static_file = os.path.join(dir, "static.txt")
            dynamic_file = os.path.join(dir, "dynamic.txt")

            static_data = utils.parse_static_file_coupled(static_file)
            time, positions = utils.parse_dynamic_file(N, dynamic_file)

            amplitudes = utils.calculate_amplitudes(positions)

            # Convert to python lists
            results.append(
                {
                    "parameters": static_data,
                    "time": list(time),
                    "amplitudes": list(amplitudes),
                    "k": static_data["K"],
                    "w": static_data["W"],
                }
            )

            print(f"Results parsed from {dir}")
        except Exception as e:
            print(f"Error: {e}")

    try:
        print("Cleaning up")
        shutil.rmtree(simulation_dir)
    except Exception as e:
        print(f"Error: {e}")

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
                output_dir, "amplitudes_vs_time", f"amplitudes_vs_time_k-{k}_w-{w:.2f}.png"
            ),
        )

        if k not in max_amplitudes:
            max_amplitudes[k] = []

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

        resonances.append((k, ws[amplitudes.index(max(amplitudes))]))

    ks = [k for k, _ in sorted(resonances, key=lambda x: x[0])]
    ws = [w for _, w in sorted(resonances, key=lambda x: x[0])]

    plots.plot_resonances_vs_k(
        ks,
        ws,
        os.path.join(output_dir, "resonances.png"),
    )

    plots.plot_resonance_squared_vs_k(
        ks,
        ws,
        os.path.join(output_dir, "resonance_square.png"),
    )

    print("Results plotted")


from matplotlib.animation import FuncAnimation, FFMpegWriter
import matplotlib.pyplot as plt


def animate(positions, l0, omega, dt, output_file="data/animation.mp4"):
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
    # Initialize a quiver for the cosine output
    quiver = ax.quiver(-l0, 0, 0, 0, angles="xy", scale_units="xy", scale=1, color="g")

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

        # Calculate the output of cos(ω * (dt * frame))
        y_quiver = (
            np.cos(omega * (dt * frame)) * (max_y - min_y) / 10
        )  # Scale to y-limits

        # Update the quiver to represent the cosine output
        quiver.set_offsets([-l0, positions[frame][0]])
        quiver.set_UVC(0, y_quiver)  # Update the quiver's vertical component

        return particles, particle_lines, wall_line, quiver

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
        results = execute_simulations(
            m=0.001,
            A=0.01,
            l0=0.0001,
            N=1000,
            i="beeman",
            dt=0.0001,
            tf=10,
            ws=list(np.linspace(0.01, 0.99, 30)) + list(np.linspace(1, 10, 80)),
            ks=[100, 2000, 4000, 7000, 10000],
            simulation_dir=os.path.join(output_dir, "simulations"),
            memory=12,
            max_workers=12,
        )

        with open(os.path.join(output_dir, "results.json"), "w") as f:
            json.dump(results, f)

    elif sys.argv[1] == "plot":
        with open(os.path.join(output_dir, "results.json"), "r") as f:
            results = json.load(f)

        plot_results(results, output_dir=output_dir)
    elif sys.argv[1] == "animate":
        with open(os.path.join(output_dir, "results.json"), "r") as f:
            results = json.load(f)

        selected_k = 100
        selected_w = 10

        for result in results:
            if result["k"] == selected_k and result["w"] == selected_w:
                animate(
                    result["positions"],
                    result["parameters"]["L0"],
                    result["parameters"]["W"],
                    result["parameters"]["Dt2"],
                    output_file=os.path.join(output_dir, "animation.mp4"),
                )
                sys.exit(0)

        # Randomly select a result if the selected k and w are not found
        result = results[0]
        print(
            f"Selected k={selected_k} and w={selected_w} not found. Using k={result['k']} and w={result['w']} instead."
        )
        animate(
            result["positions"],
            result["parameters"]["L0"],
            result["parameters"]["W"],
            result["parameters"]["Dt2"],
            output_file=os.path.join(output_dir, "animation.mp4"),
        )

    else:
        print("Usage: python dampened_oscillator.py <generate|plot>")
        sys.exit(1)
