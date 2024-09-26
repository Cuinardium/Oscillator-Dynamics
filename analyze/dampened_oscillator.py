import numpy as np
import matplotlib.pyplot as plt
import utils
import sys


# Solucion analitica M.A.S subamortiguado
def get_analitic_positions(time_steps, gamma, m, k, A):
    analitic_positions = []
    for t in time_steps:
        exponent = -(gamma / (2 * m)) * t
        cosine_argument = np.sqrt((k / m) - (gamma / (2 * m)) ** 2) * t
        analitic_positions.append(A * np.exp(exponent) * np.cos(cosine_argument))

    return analitic_positions


# Set up the figure and axis for the plot
def plot_positions_through_time(time_steps, verlet_positions, analitic_positions, file_name="positions_vs_time.png"):
    plt.figure(figsize=(10, 6))
    plt.plot(
        time_steps,
        verlet_positions,
        color="b",
        marker="o",
        linestyle="-",
        markersize=1,
        label="Verlet",
    )
    plt.plot(
        time_steps,
        analitic_positions,
        color="r",
        marker="o",
        linestyle=":",
        markersize=1,
        label="Analitic",
    )
    plt.xlim(min(time_steps), max(time_steps))

    verlet_min = min(verlet_positions)
    verlet_max = max(verlet_positions)
    analitic_min = min(analitic_positions)
    analitic_max = max(analitic_positions)

    plt.ylim(
        min(verlet_min, analitic_min) - 0.1,
        max(verlet_max, analitic_max) + 0.1,
    )

    plt.xlabel("Tiempo (s)")
    plt.ylabel("Posición (m)")
    
    plt.legend()
    plt.savefig(file_name)


if __name__ == "__main__":

    # First and only argument is directory
    if len(sys.argv) != 2:
        print("Usage: python dampened_oscillator.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]

    static_data = utils.parse_static_file_dampened(f"{directory}/static.txt")

    time, positions, _ = utils.parse_dynamic_file(1, f"{directory}/dynamic.txt")

    gamma = static_data["Gamma"]
    k = static_data["K"]
    m = static_data["M"]
    A = static_data["R0"]

    analitic_positions = get_analitic_positions(time, gamma, m, k, A)

    plot_positions_through_time(time, positions[:, 0], analitic_positions, f"{directory}/positions_vs_time.png")


