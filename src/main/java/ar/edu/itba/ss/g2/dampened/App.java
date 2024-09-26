package ar.edu.itba.ss.g2.dampened;

import ar.edu.itba.ss.g2.dampened.config.ArgParser;
import ar.edu.itba.ss.g2.dampened.config.Configuration;
import ar.edu.itba.ss.g2.model.Particle;
import ar.edu.itba.ss.g2.simulation.Simulation;
import ar.edu.itba.ss.g2.simulation.integrators.Equation;
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

        double r0 = configuration.getR0();
        double v0 = -r0 * (gamma / (2 * configuration.getM()));

        Particle particle = new Particle(0, r0, v0, configuration.getM());

        Equation forceEquation =
                (particles) ->
                        particles.stream()
                                .map(p -> -k * p.getPosition() - gamma * p.getV())
                                .toList();

        double dt = configuration.getDt();
        double dt2 = configuration.getDt2();
        double tf = configuration.getTf();

        MovementIntegrator integrator = new VerletIntegrator(List.of(particle), forceEquation, dt);

        Simulation simulation = new Simulation(dt, dt2, integrator);
        simulation.run(tf);

        List<List<Particle>> snapshots = simulation.getSnapshots();
        String outputDir = configuration.getOutputDir();

        try {
            FileUtil.serializeStaticDampened(configuration);
            FileUtil.serializeDynamic(snapshots, outputDir, dt);
        } catch (IOException e){
            System.err.println("Error writing output files: " + e.getMessage());
            System.exit(1);
        }
    }
}
