import numpy as np

def parse_dynamic_file(num_particles, path="dynamic.txt"):
    time = []
    positions = []

    with open(path, "r") as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        t = float(lines[i].strip())
        time.append(t)
        i += 1

        snapshot_positions = []

        for _ in range(num_particles):
            pos = float(lines[i].strip())
            snapshot_positions.append(pos)
            i += 1

        # Store the current snapshot's positions and velocities
        positions.append(snapshot_positions)

    return np.array(time), np.array(positions)

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
        "Integrator": integrator
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
def generate_frequencies(w0, num_points=1000):
    w_min = 0.01
    w_max = 3.5 * w0
    ws = np.linspace(w_min, w_max, num_points)
    
    # Crear más puntos alrededor de w0, 2*w0, 3*w0
    fine_range = 0.1      
    harmonics = [w0, 2 * w0, 3 * w0]
    
    for harmonic in harmonics:
        fine_ws = np.linspace(harmonic - fine_range, harmonic + fine_range, num_points // 5)
        ws = np.concatenate((ws, fine_ws))
    
    return np.unique(np.sort(ws))
