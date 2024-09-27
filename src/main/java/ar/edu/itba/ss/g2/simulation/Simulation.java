package ar.edu.itba.ss.g2.simulation;

import ar.edu.itba.ss.g2.model.Particle;
import ar.edu.itba.ss.g2.simulation.integrators.MovementIntegrator;

import java.util.LinkedList;
import java.util.List;

public class Simulation {

    private final double timeStep;
    private final double snapshotStep;

    private final MovementIntegrator integrator;

    private final List<List<Particle>> snapshots;

    public Simulation(double timeStep, double snapshotStep, MovementIntegrator integrator) {
        this.timeStep = timeStep;
        this.snapshotStep = snapshotStep;
        this.integrator = integrator;
        this.snapshots = new LinkedList<>();
    }

    public void run(double maxTime) {
        for (double t = 0, elapsed = 0; t < maxTime; t += timeStep, elapsed += timeStep) {
            integrator.integrate();

            if (elapsed >= snapshotStep) {
                snapshots.add(integrator.getState());
                elapsed = 0;
            }
        }
    }

    public List<List<Particle>> getSnapshots() {
        return snapshots;
    }
}
