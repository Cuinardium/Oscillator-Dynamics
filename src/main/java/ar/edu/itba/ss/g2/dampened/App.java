package ar.edu.itba.ss.g2.dampened;

import ar.edu.itba.ss.g2.dampened.config.ArgParser;
import ar.edu.itba.ss.g2.dampened.config.Configuration;
import ar.edu.itba.ss.g2.model.Particle;
import ar.edu.itba.ss.g2.simulation.Simulation;
import ar.edu.itba.ss.g2.simulation.integrators.BeemanIntegrator;
import ar.edu.itba.ss.g2.simulation.integrators.Equation;
import ar.edu.itba.ss.g2.simulation.integrators.GearIntegrator;
import ar.edu.itba.ss.g2.simulation.integrators.MovementIntegrator;
import ar.edu.itba.ss.g2.simulation.integrators.VerletIntegrator;
import ar.edu.itba.ss.g2.utils.FileUtil;

import java.io.IOException;
import java.util.List;

public class App {
    public static void main(String[] args) {

        ArgParser parser = new ArgParser(args);
        Configuration configuration = parser.parse();

        if (configuration == null) {
            parser.printHelp();
            System.exit(1);
        }

        double k = configuration.getK();
        double gamma = configuration.getGamma();
        double m = configuration.getM();

        double r0 = configuration.getR0();
        double r1 = -r0 * (gamma / (2 * m));
        double r2 = (-k * r0 - gamma * r1) / m;
        double r3 = (-k * r1 - gamma * r2) / m;
        double r4 = (-k * r2 - gamma * r3) / m;
        double r5 = (-k * r3 - gamma * r4) / m;

        Particle particle = new Particle(0, r0, r1, r2, r3, r4, r5, m);

        Equation forceEquation =
                (particles, t) ->
                        particles.stream()
                                .map(p -> -k * p.getPosition() - gamma * p.getV())
                                .toList();

        double dt = configuration.getDt();
        double dt2 = configuration.getDt2();
        double tf = configuration.getTf();

        MovementIntegrator integrator;

        switch (configuration.getIntegrator()) {
            case "verlet":
                integrator = new VerletIntegrator(List.of(particle), forceEquation, dt);
                break;
            case "beeman":
                integrator = new BeemanIntegrator(List.of(particle), forceEquation, dt);
                break;
            case "gear":
                integrator = new GearIntegrator(List.of(particle), forceEquation, dt);
                break;
            default:
                System.err.println("Invalid integrator: " + configuration.getIntegrator());
                System.exit(1);
                return;
        }

        Simulation simulation = new Simulation(dt, dt2, integrator);
        simulation.run(tf);

        List<List<Particle>> snapshots = simulation.getSnapshots();
        String outputDir = configuration.getOutputDir();

        try {
            FileUtil.serializeStaticDampened(configuration);
            FileUtil.serializeDynamic(snapshots, outputDir, dt2);
        } catch (IOException e) {
            System.err.println("Error writing output files: " + e.getMessage());
            System.exit(1);
        }
    }
}
