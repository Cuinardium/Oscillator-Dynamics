package ar.edu.itba.ss.g2.simulation;

import ar.edu.itba.ss.g2.model.Particle;
import ar.edu.itba.ss.g2.simulation.integrators.MovementIntegrator;

import java.util.LinkedList;
import java.util.List;

public class Simulation {

    private final double timeStep;
    private final double snapshotStep;

    private final MovementIntegrator integrator;

    private final List<List<Double>> snapshots;

    public Simulation(double timeStep, double snapshotStep, MovementIntegrator integrator) {
        this.timeStep = timeStep;
        this.snapshotStep = snapshotStep;
        this.integrator = integrator;
        this.snapshots = new LinkedList<>();
    }

    public void run(double maxTime) {

        int printElapsed = 0;
        int iterations = (int) (maxTime / timeStep);
        int printStep = iterations >= 10 ? iterations / 10 : 1;

        for (double t = 0, elapsed = 0; t < maxTime; t += timeStep, elapsed += timeStep) {
            integrator.integrate();

            printElapsed++;
            if (printElapsed >= printStep) {
                System.out.println(String.format("Progress: %.2f/%.2f", t, maxTime));
                printElapsed = 0;
            }

            if (elapsed >= snapshotStep) {
                snapshots.add(integrator.getState());
                elapsed = 0;
            }
        }
    }

    public List<List<Double>> getSnapshots() {
        return snapshots;
    }
}
