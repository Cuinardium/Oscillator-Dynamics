import matplotlib.pyplot as plt


# Set up the figure and axis for the plot
def plot_positions_vs_time(
    times,
    positions,
    labels,
    file_name="positions_vs_time.png",
):
    plt.figure(figsize=(10, 6))

    line_styles = ["-", "--", "-.", ":"]

    for i, time_steps, position, label in zip(range(len(times)), times, positions, labels):
        line_style = line_styles[i % len(line_styles)]
        plt.plot(time_steps, position, linestyle=line_style, label=label)

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

    plt.legend()
    plt.savefig(file_name)

    plt.close()


def plot_squared_error_vs_time(
    times, squared_errors, labels, file_name="squared_error_vs_time.png"
):
    plt.figure(figsize=(10, 6))

    line_styles = ["-", "--", "-.", ":"]

    for i, time_steps, squared_error, label in zip(range(len(times)), times, squared_errors, labels):
        line_style = line_styles[i % len(line_styles)]
        plt.plot(time_steps, squared_error, linestyle=line_style, label=label)

    plt.xlim(
        min([min(time_steps) for time_steps in times]),
        max([max(time_steps) for time_steps in times]),
    )

    plt.ylim(
        0,
        max(max(squared_error) for squared_error in squared_errors),
    )

    plt.xlabel("Tiempo (s)")
    plt.ylabel("Error cuadrático (m$^2$)")

    plt.legend()

    plt.savefig(file_name)

    plt.close()


def plot_mean_squared_error_vs_dt(
    dt_values, mean_squared_errors, file_name="mean_squared_error_vs_dt.png"
):
    plt.figure(figsize=(10, 6))


    line_styles = ["-", "--", "-.", ":"]

    for i, integrator, mean_squared_error in zip(range(len(mean_squared_errors)), mean_squared_errors.keys(), mean_squared_errors.values()):
        plt.plot(
            dt_values, mean_squared_error, linestyle=line_styles[i % len(line_styles)], label=integrator
        )

    plt.xlabel("dt (s)")
    plt.ylabel("Error cuadrático medio (m$^2$)")

    plt.legend()

    plt.savefig(file_name)

    plt.close()

    # Repeat with logaritmic and semi-logaritmic scale
    plt.figure(figsize=(10, 6))

    for i, integrator, mean_squared_error in zip(range(len(mean_squared_errors)), mean_squared_errors.keys(), mean_squared_errors.values()):
        plt.plot(
            dt_values, mean_squared_error, linestyle=line_styles[i % len(line_styles)], label=integrator
        )

    plt.xlabel("dt (s)")
    plt.ylabel("Error cuadrático medio (m$^2$)")

    plt.legend()

    plt.yscale("log")
    plt.savefig(file_name.replace(".png", "_log.png"))

    plt.close()

    plt.figure(figsize=(10, 6))

    
    for i, integrator, mean_squared_error in zip(range(len(mean_squared_errors)), mean_squared_errors.keys(), mean_squared_errors.values()):
        plt.plot(
            dt_values, mean_squared_error, linestyle=line_styles[i % len(line_styles)], label=integrator
        )

    plt.xlabel("dt (s)")
    plt.ylabel("Error cuadrático medio (m$^2$)")

    plt.legend()

    plt.xscale("log")
    plt.yscale("log")

    plt.savefig(file_name.replace(".png", "_loglog.png"))

    plt.close()
