import numpy as np

def parse_dynamic_file(num_particles, path="dynamic.txt"):
    time = []
    positions = []
    velocities = []

    with open(path, "r") as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        t = float(lines[i].strip())
        time.append(t)
        i += 1

        snapshot_positions = []
        snapshot_velocities = []

        for _ in range(num_particles):
            pos, vel = map(float, lines[i].strip().split())
            snapshot_positions.append(pos)
            snapshot_velocities.append(vel)
            i += 1

        # Store the current snapshot's positions and velocities
        positions.append(snapshot_positions)
        velocities.append(snapshot_velocities)

    return np.array(time), np.array(positions), np.array(velocities)

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
