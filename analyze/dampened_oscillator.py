import os
import shutil
import subprocess
import concurrent.futures
import numpy as np
import utils
import json
import plots
import sys


def execute_simulation(gamma, k, m, A, i, dt, dt2, tf, root_dir="data/simulations"):

    name = f"dt-{dt}_i-{i}-d"
    unique_dir = os.path.join(root_dir, name)

    os.makedirs(unique_dir, exist_ok=True)

    command = [
        "java",
        "-jar",
        "target/dampened-oscillator-jar-with-dependencies.jar",
        "-out",
        unique_dir,
        "-g",
        str(gamma),
        "-k",
        str(k),
        "-m",
        str(m),
        "-r0",
        str(A),
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
        print(f"Running simulation, i={i}, dt={dt}")
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Simulation finished, i={i}, dt={dt}")
    except subprocess.CalledProcessError as e:
        print(f"Error running simulation, i={i}, dt={dt}")
        print(f"Error: {e.stderr}")

    return unique_dir


def execute_simulations(
    gamma,
    k,
    m,
    A,
    integrators,
    dts,
    tf,
    simulation_dir="data/simulations",
    max_workers=4,
):

    print("Executing simulations")

    dirs = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(
                execute_simulation,
                gamma,
                k,
                m,
                A,
                i,
                dt,
                0.01 if dt <= 0.01 else dt,
                tf,
                root_dir=simulation_dir,
            )
            for i in integrators
            for dt in dts
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

            static_data = utils.parse_static_file_dampened(static_file)
            time, positions = utils.parse_dynamic_file(1, dynamic_file)

            # Convert to python lists
            results.append(
                {
                    "parameters": static_data,
                    "time": list(time),
                    "positions": list(positions[:, 0]),
                    "integrator": static_data["Integrator"],
                    "dt": static_data["Dt"],
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

    all_positions = []
    all_times = []
    all_squared_errors = []
    labels = []

    # Dict of dt -> analitic_positions (positions for analitic integrator)
    analitic_positions = {}
    analitic_times = {}
    dts = set()
    for result in results:
        positions = result["positions"]
        integrator = result["integrator"]
        dt = result["dt"]

        dts.add(dt)

        if integrator == "analitic":
            analitic_positions[dt] = positions
            analitic_times[dt] = result["time"]

    # Nearest dt to 0.01, used for plots vs time
    selected_dt = min(dts, key=lambda x: abs(x - 0.01))
    analitic_pos_for_selected_dt = analitic_positions[selected_dt]
    analitic_times_for_selected_dt = analitic_times[selected_dt]

    # Dict of integrator -> (dt, squared_error)
    mean_squared_errors = {}

    for result in results:

        if result["integrator"] == "analitic":
            continue

        time = result["time"]
        positions = result["positions"]
        integrator = result["integrator"]
        dt = result["dt"]

        squared_error = np.square(
            np.array(positions) - np.array(analitic_positions[dt])
        )
        mean_squared_error = np.mean(squared_error)

        if integrator not in mean_squared_errors:
            mean_squared_errors[integrator] = []

        mean_squared_errors[integrator].append((dt, mean_squared_error))

        if dt != selected_dt:
            continue

        all_squared_errors.append(squared_error)
        all_positions.append(positions)
        all_times.append(time)
        labels.append(integrator)

    plots.plot_positions_vs_time(
        all_times + [analitic_times_for_selected_dt],
        all_positions + [analitic_pos_for_selected_dt],
        labels + ["analitic"],
        file_name=f"{output_dir}/positions_vs_time.png",
    )

    plots.plot_squared_error_vs_time(
        all_times,
        all_squared_errors,
        labels,
        file_name=f"{output_dir}/squared_error_vs_time.png",
    )

    plots.plot_mean_squared_error_vs_dt(
        mean_squared_errors,
        file_name=f"{output_dir}/mean_squared_error_vs_dt.png",
    )

    print("Results plotted")


if __name__ == "__main__":

    # First and only argument is directory
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print("Usage: python dampened_oscillator.py <generate|plot> [directory]")
        sys.exit(1)

    output_dir = sys.argv[2] if len(sys.argv) == 3 else "data/"

    if sys.argv[1] == "generate":
        results = execute_simulations(
            gamma=100,
            k=10000,
            m=170,
            A=1,
            integrators=["beeman", "gear", "verlet", "analitic"],
            dts=list(np.logspace(-6, -1, num=50)),
            # dts=[1e-6],
            tf=5,
            simulation_dir=os.path.join(output_dir, "simulations"),
            max_workers=5,
        )

        with open(os.path.join(output_dir, "results.json"), "w") as f:
            json.dump(results, f)

    elif sys.argv[1] == "plot":
        with open(os.path.join(output_dir, "results.json"), "r") as f:
            results = json.load(f)

        plot_results(results, output_dir=output_dir)

    else:
        print("Usage: python dampened_oscillator.py <generate|plot>")
        sys.exit(1)
