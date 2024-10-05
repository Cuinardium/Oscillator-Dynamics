import matplotlib.pyplot as plt
import numpy as np


# Set up the figure and axis for the plot
def plot_positions_vs_time(
    times,
    positions,
    labels,
    file_name="positions_vs_time.png",
):
    plt.figure(figsize=(10, 6))

    line_styles = ["-", "--", "-.", ":"]
    colors = ["blue", "orange", "green", "purple"]

    for i, time_steps, position, label in zip(
        range(len(times)), times, positions, labels
    ):
        line_style = line_styles[i % len(line_styles)]
        color = colors[i % len(colors)]
        plt.plot(time_steps, position, linestyle=line_style, label=label, color=color)

    plt.xlim(
        min([min(time_steps) for time_steps in times]),
        max([max(time_steps) for time_steps in times]),
    )

    plt.ylim(
        min(min(position) for position in positions) - 0.1,
        max(max(position) for position in positions) + 0.1,
    )

    plt.xlabel("Tiempo (s)")
    plt.ylabel("Posición (m)")

    ax = plt.gca()
    handles, labels = ax.get_legend_handles_labels()
    custom_order = ["verlet", "beeman", "gear", "analitic"]
    label_to_handle = dict(zip(labels, handles))
    sorted_handles = [label_to_handle[label] for label in custom_order]
    sorted_labels = custom_order
    ax.legend(sorted_handles, sorted_labels)

    plt.savefig(file_name)

    plt.close()

    # Plot zoomed in version

    plt.figure(figsize=(10, 6))

    for i, time_steps, position, label in zip(
        range(len(times)), times, positions, labels
    ):
        line_style = line_styles[i % len(line_styles)]
        color = colors[i % len(colors)]
        plt.plot(
            time_steps,
            position,
            linestyle=line_style,
            label=label,
            color=color,
        )

    plt.xlim(
        1.0405,
        1.0406,
    )

    plt.ylim(
        -0.516,
        -0.505,
    )



    plt.xlabel("Tiempo (s)")
    plt.ylabel("Posición (m)")

    ax = plt.gca()

    handles, labels = ax.get_legend_handles_labels()
    custom_order = ["verlet", "beeman", "gear", "analitic"]
    label_to_handle = dict(zip(labels, handles))
    sorted_handles = [label_to_handle[label] for label in custom_order]
    sorted_labels = custom_order
    ax.legend(sorted_handles, sorted_labels)

    plt.savefig(file_name.replace(".png", "_zoomed.png"))

    plt.close()


def plot_squared_error_vs_time(
    times, squared_errors, labels, file_name="squared_error_vs_time.png"
):
    plt.figure(figsize=(10, 6))

    for time_steps, squared_error, label in zip(times, squared_errors, labels):
        plt.plot(time_steps, squared_error, label=label)

    plt.xlim(
        min([min(time_steps) for time_steps in times]),
        max([max(time_steps) for time_steps in times]),
    )

    plt.xlabel("Tiempo (s)")
    plt.ylabel("Error cuadrático (m$^2$)")

    plt.yscale("log")

    ax = plt.gca()
    handles, labels = ax.get_legend_handles_labels()
    custom_order = ["verlet", "beeman", "gear"]
    label_to_handle = dict(zip(labels, handles))
    sorted_handles = [label_to_handle[label] for label in custom_order]
    sorted_labels = custom_order
    ax.legend(sorted_handles, sorted_labels)

    plt.savefig(file_name)

    plt.close()


# mean_squared_errors, dict integrator -> list (dt, mean_squared_error)
def plot_mean_squared_error_vs_dt(
    mean_squared_errors, file_name="mean_squared_error_vs_dt.png"
):
    plt.figure(figsize=(10, 6))

    for integrator, errors in mean_squared_errors.items():
        # Sort by dt
        errors = sorted(errors, key=lambda x: x[0])
        dts, mean_squared_error = zip(*errors)
        plt.plot(dts, mean_squared_error, label=integrator, marker="o", markersize=3, linestyle=":")

    plt.xlabel("dt (s)")
    plt.ylabel("Error cuadrático medio (m$^2$)")

    ax = plt.gca()
    handles, labels = ax.get_legend_handles_labels()
    custom_order = ["verlet", "beeman", "gear"]
    label_to_handle = dict(zip(labels, handles))
    sorted_handles = [label_to_handle[label] for label in custom_order]
    sorted_labels = custom_order
    ax.legend(sorted_handles, sorted_labels)

    plt.xscale("log")
    plt.yscale("log")

    plt.savefig(file_name)

    plt.close()


def plot_amplitudes_vs_time(
    times, amplitudes, file_name="amplitudes_vs_time.png"
):
    plt.figure(figsize=(10, 6))

    plt.plot(times, amplitudes)

    y_max = max(amplitudes)

    plt.ylim(
        0,
        y_max + 0.1 * y_max,
    )

    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud (m)")

    plt.savefig(file_name)

    plt.close()


def plot_amplitudes_vs_w(ws, normal_frequencies, amplitudes, file_name="amplitudes_vs_w.png"):
    plt.figure(figsize=(10, 6))

    # Asymptotes at normal frequencies
    for w in normal_frequencies:
        plt.axvline(x=w, color="red", linestyle="--", linewidth=0.5)

    # Split the ws and amplitudes into segments based on normal frequencies
    segments = []
    current_segment_ws = []
    current_segment_amplitudes = []
    
    for w, amp in zip(ws, amplitudes):
        if w in normal_frequencies:
            # Store the current segment and reset for the next one
            if current_segment_ws:
                segments.append((current_segment_ws, current_segment_amplitudes))
            current_segment_ws = []
            current_segment_amplitudes = []
        else:
            current_segment_ws.append(w)
            current_segment_amplitudes.append(amp)

    # Append the last segment if any data remains
    if current_segment_ws:
        segments.append((current_segment_ws, current_segment_amplitudes))

    # Plot each segment as a separate line
    for segment_ws, segment_amplitudes in segments:
        plt.plot(segment_ws, segment_amplitudes, marker="o", markersize=2, linestyle=":", color="C0")

    plt.xlabel("w (rad/s)")
    plt.ylabel("Amplitud (m)")
    
    plt.savefig(file_name)
    plt.close()

def plot_resonances_vs_k(
    ks, resonances, file_name="resonances_vs_k.png"
):
    plt.figure(figsize=(10, 6))

    plt.plot(ks, resonances, marker="o", markersize=5, linestyle="")

    plt.xlabel("k (N/m)")
    plt.ylabel("Frecuencia de resonancia (rad/s)")

    plt.savefig(file_name)

    plt.close()

def plot_resonance_with_best_constant_vs_k(
    ks, resonances, best_constant, file_name="resonances_with_best_constant_vs_k.png"
):
    plt.figure(figsize=(10, 6))

    plt.plot(ks, resonances, marker="o", markersize=5, linestyle="", label="Frecuencia de resonancia")

    # Curve is best_constant * k^1/2
    ks = np.linspace(0, max(ks), 100)
    resonances = best_constant * np.sqrt(ks)
    best_constant = "{:.4f}".format(best_constant)
    plt.plot(ks, resonances, linestyle="-", color="r", label=f"{best_constant} * k$^1/2$")


    plt.xlabel("k (N/m)")
    plt.ylabel("Frecuencia de resonancia (rad/s)")

    plt.legend()

    plt.savefig(file_name)

    plt.close()

def plot_cuadratic_error_vs_constant(
    constants, errors, file_name="cuadratic_error_vs_constant.png"
):
    plt.figure(figsize=(10, 6))

    plt.plot(constants, errors, marker="o", markersize=3, linestyle=":")

    plt.xlabel("Constante")
    plt.ylabel("Error cuadrático (m$^2$)")

    plt.savefig(file_name)

    plt.close()

