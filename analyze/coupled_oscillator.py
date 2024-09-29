import os
import shutil
import subprocess
import concurrent.futures
import numpy as np
import utils
import json
import plots
import sys


def execute_simulation(k, m, A, l0, N, w, i, dt, dt2, tf, root_dir="data/simulations"):

    name = f"w-{w}_k-{k}"
    unique_dir = os.path.join(root_dir, name)

    os.makedirs(unique_dir, exist_ok=True)

    command = [
        "java",
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
                dt,
                0.005 if dt <= 0.005 else dt,
                tf,
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

            # Convert to python lists
            results.append(
                {
                    "parameters": static_data,
                    "time": list(time),
                    "positions": list(
                        list(particle_positions) for particle_positions in positions
                    ),
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
        - 2 * l0, l0 * num_particles
    )  # Fixed x-limits based on particle separation
    min_y = min(positions.flatten())
    max_y = max(positions.flatten())
    ax.set_ylim(
        min_y - 0.1 * min_y,
        max_y + 0.1 * max_y,
    )  # Dynamic y-limits based on particle movement

    # Initialize the scatter plot for particles
    (particles,) = ax.plot([], [], "bo", ms=6)  # 'bo' means blue circles

    # Line objects for connecting particles and the wall
    particle_lines, = ax.plot([], [], "b-", lw=1)  # Lines between particles
    (wall_line,) = ax.plot([], [], "b-", lw=1)
    # Initialize a quiver for the cosine output
    quiver = ax.quiver(-l0, 0, 0, 0, angles='xy', scale_units='xy', scale=1, color='g')

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
        y_quiver = np.cos(omega * (dt * frame)) * (max_y - min_y) / 10  # Scale to y-limits
        
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
            N=3,
            i="gear",
            dt=0.001,
            tf=5,
            ws=[1],
            ks=[100],
            simulation_dir=os.path.join(output_dir, "simulations"),
            max_workers=5,
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
        selected_w = 1

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

        print(f"Results for k={selected_k}, w={selected_w} not found")
        sys.exit(1)

    else:
        print("Usage: python dampened_oscillator.py <generate|plot>")
        sys.exit(1)
