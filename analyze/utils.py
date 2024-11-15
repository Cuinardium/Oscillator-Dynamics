import numpy as np


def parse_dynamic_file(path="dynamic.txt"):
    with open(path, "r") as f:
        num_particles, num_times = map(int, f.readline().strip().split())

    data = np.loadtxt(path, skiprows=1)

    # Reshape the data: each time step includes 1 time value + num_particles positions
    data = data.reshape((num_times, num_particles + 1))

    # First column is time, the rest are positions
    time = data[:, 0]
    positions = data[:, 1:]

    return time, positions


def parse_static_file_dampened(path="static.txt"):
    with open(path, "r") as f:
        lines = f.readlines()

    # Parse each line and convert to float
    M = float(lines[0].strip())
    K = float(lines[1].strip())
    Gamma = float(lines[2].strip())
    R0 = float(lines[3].strip())
    Dt = float(lines[4].strip())
    Dt2 = float(lines[5].strip())
    Tf = float(lines[6].strip())
    Integrator = lines[7].strip()

    return {
        "M": M,
        "K": K,
        "Gamma": Gamma,
        "R0": R0,
        "Dt": Dt,
        "Dt2": Dt2,
        "Tf": Tf,
        "Integrator": Integrator,
    }


def parse_static_file_coupled(path="static.txt"):
    with open(path, "r") as f:
        lines = f.readlines()

    # Parse each line and convert to the appropriate data type
    M = float(lines[0].strip())
    K = float(lines[1].strip())
    A = float(lines[2].strip())
    L0 = float(lines[3].strip())
    N = int(lines[4].strip())  # N is likely an integer (number of particles)
    W = float(lines[5].strip())
    Dt = float(lines[6].strip())
    Dt2 = float(lines[7].strip())
    Tf = float(lines[8].strip())
    integrator = lines[9].strip()  # Assuming integrator is a string

    return {
        "M": M,
        "K": K,
        "A": A,
        "L0": L0,
        "N": N,
        "W": W,
        "Dt": Dt,
        "Dt2": Dt2,
        "Tf": Tf,
        "Integrator": integrator,
    }


# Positions is a 2D NumPy array where each row represents a snapshot in time
def calculate_amplitudes(positions):
    # Return the maximum distance to equilibrium for each time snapshot

    system_amplitudes = []

    for snapshot in positions:
        # Calculate the amplitude for each particle in the snapshot
        particle_amplitudes = [abs(pos) for pos in snapshot]
        system_amplitudes.append(max(particle_amplitudes))

    return system_amplitudes


# Para generar frecuencias para graficar
# mayor numero de frecuencias cerca de wo y sus armonicos
def generate_frequencies(k, m, N, num_points=1000):
    harmonics = [
        2 * (np.sqrt(k) / np.sqrt(m)) * np.sin((n * np.pi) / (2 * N))
        for n in range(1, 4)
    ]

    # Definir proporciones de puntos: 1/5 para cada armónico, 2/5 para el resto del rango
    points_per_harmonic = num_points // 5
    remaining_points = num_points - 3 * points_per_harmonic

    frequencies = []

    # Generar puntos alrededor de cada armónico (espejado desde el armónico)
    for harmonic in harmonics:
        delta = 0.05 * harmonic if k < 100 else 0.01 * harmonic
        freqs_near_harmonic = np.linspace(
            harmonic - delta, harmonic + delta, points_per_harmonic
        )
        frequencies.extend(freqs_near_harmonic)

    # Generar los puntos restantes entre 0.5 y 3.5 veces el primer armónico
    min_freq = 0.5 * harmonics[0]
    max_freq = 3.5 * harmonics[0]
    remaining_freqs = np.linspace(min_freq, max_freq, remaining_points)
    frequencies.extend(remaining_freqs)
    frequencies.extend(harmonics)

    return np.sort(np.unique(np.array(frequencies))), harmonics
