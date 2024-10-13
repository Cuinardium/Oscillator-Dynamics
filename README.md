# Oscillator Dynamics
This project simulates the behavior of oscillating systems using numerical integration techniques. It includes both a dampened oscillator and a coupled oscillator system, where the oscillators are modeled as particles connected by springs. This project also provides tools for analyzing the simulation results, including generating plots and animations of the oscillators movements.

## Requirements

- `Java 17` (Simulation)
- `Python` (Analysis)
  - `numpy`
  - `matplotlib`
  - `scipy`

## Building

To build the project run the following:

```sh
mvn clean package
```

This will generate the following JAR files in the `target` directory:
- `dampened-oscillator-jar-with-dependencies.jar` (Dampened Oscillator System)
- `coupled-oscillator-jar-with-dependencies.jar` (Coupled Oscillators System)

# Dampened Oscillator

## Usage 

To run the simulation, execute the following command:

```sh
java -jar dampened-oscillator-jar-with-dependencies.jar [options]
```

Options
|Short|	Long|	Arguments|	Description|
|---|---|---|---|
|`-m`|	`--mass`|	required|	The mass of the oscillator (kg).|
|`-k`|	`--spring`|	required|	The spring constant (N/m), defining the stiffness of the spring.|
|`-g`|	`--gamma`|	required|	The damping coefficient (kg/s), affecting the energy dissipation rate.|
|`-tf`|	`--time`|	required|	The final simulation time (s).|
|`-r0`|	`--position`|	required|	The initial position of the mass (m).|
|`-dt`	|`--delta`|	required|	The integration time step (s), defining the granularity of the simulation.|
|`-dt2`|	`--delta2`|	required|	The snapshot time step (s), defining how often results are recorded.|
|`-i`	|`--integrator`|	required|	The movement integration scheme to be used (beeman, verlet, or gear).|
|`-out`|	`--output`|	required|	The directory where output files will be stored.|

## Output

The results of the simulation are saved in the specified output directory. The files generated include:

### `static.txt`
This file contains the static configuration parameters used for the simulation, written in the following order:

1. Mass (kg)
2. Spring constant (N/m)
3. Damping coefficient (kg/s)
4. Initial position (m)
5. Integration time step (s)
6. Snapshot time step (s)
7. Final time (s)
8. Selected integration scheme (beeman, verlet, gear)

Example of `static.txt`:

```
1.0
10.0
0.5
0.0
0.01
0.1
10.0
beeman
```

### `dynamic.txt`
This file contains the time evolution of the oscillator’s position for each snapshot, with each entry formatted to high precision. The content includes:

- The number of particles and total number of snapshots.
- For each snapshot, the time in seconds and the corresponding position(s).

Example of `dynamic.txt`:

```
1 1001
0.0100000000000000
0.0000000000000000
0.0200000000000000
0.0010000000000000
0.0300000000000000
0.0019995000000000
0.0400000000000000
0.0029980000000000
...
10.0000000000000000
0.0998334166468281
```

In this example:

- The file starts by specifying there is 1 particle and 1001 snapshots.
- For each snapshot, it lists the time and the corresponding position of the particle at that moment.


## Analysis Script

A Python script is provided in the `analysis` directory that is designed to either generate simulation data or plot the results of analysing the data.

The script accepts two modes of operation, `generate` and `plot`, and an optional argument specifying the output directory. If no directory is provided, the default directory is `data/`.

Command to generate simulation data:

```sh
python dampened_oscillator.py generate [directory]
```

Command to plot results:

```sh
python dampened_oscillator.py plot [directory]
```

# Coupled Oscillator Simulation

## Usage
To run the coupled oscillator simulation, use the following command:

```sh
java -jar coupled-oscillator-jar-with-dependencies.jar [options]
```

Options

| Short | Long         | Arguments | Description                                                           |
|-------|--------------|-----------|-----------------------------------------------------------------------|
| -m    | --mass       | required  | The mass of each oscillator particle (kg).                            |
| -k    | --spring     | required  | The spring constant (N/m), defining the stiffness of the spring between particles. |
| -A    | --amplitude  | required  | The force applied amplitude (m).                                       |
| -l0   | --l0         | required  | Resting distance between the particles (m).                            |
| -N    | --N          | required  | The number of particles in the coupled system.                         |
| -w    | --w          | required  | Driving frequency (rad/t), used to apply an external force.            |
| -tf   | --time       | required  | The final simulation time (s).                                         |
| -dt   | --delta      | required  | The integration time step (s), defining the simulation granularity.    |
| -dt2  | --delta2     | required  | The snapshot time step (s), defining how often results are recorded.   |
| -i    | --integrator | required  | The integration scheme used for movement simulation (beeman, verlet, or gear). |
| -out  | --output     | required  | The directory where output files will be saved.                        |


## Output
The simulation generates two main output files in the specified directory:

### `static.txt`
This file contains the static configuration parameters used for the simulation, listed in the following order:

1. Mass (kg)
2. Spring constant (N/m)
3. Amplitude (m)
4. Resting distance between particles (m)
5. Number of particles
6. Driving frequency (rad/t)
7. Integration time step (s)
8. Snapshot time step (s)
9. Final time (s)
10. Selected integration scheme (beeman, verlet, gear)

Example of `static.txt`:

```
0.001
100.0
0.01
0.001
100
50.0
0.00001
0.001
10.0
verlet
```

### `dynamic.txt`
This file contains the time evolution of the positions of all particles for each snapshot, formatted with high precision. The content includes:

- The number of particles and total number of snapshots.
- For each snapshot, the time and corresponding positions of each particle.

Example of `dynamic.txt`:

```
100 10001
0.0000100000000000000
0.0000000000000000
0.0001000000000000
...
10.0000000000000000
0.0998334166468281
```

In this example:

- The file starts by specifying there are 100 particles and 10001 snapshots.
- Each snapshot lists the time followed by the positions of all particles at that moment.

## Analysis Script
A Python script is provided in the `analysis` directory to generate simulation data, plot results, or create animations.

To generate data, use:

```sh
python dampened_oscillator.py generate [directory] [ideal_ws]
```

To plot results, use:

```sh
python dampened_oscillator.py plot [directory]
```

To animate the particle motion, use:

```sh
python dampened_oscillator.py animate [directory]
```

By default, the script outputs data to the `data/` directory. The optional `ideal_ws` flag generates simulations using idealized frequency ranges for resonance.
