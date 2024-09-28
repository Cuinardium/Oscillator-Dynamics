package ar.edu.itba.ss.g2.coupled;

import ar.edu.itba.ss.g2.coupled.config.ArgParser;
import ar.edu.itba.ss.g2.coupled.config.Configuration;
import ar.edu.itba.ss.g2.model.Particle;
import ar.edu.itba.ss.g2.simulation.Simulation;
import ar.edu.itba.ss.g2.simulation.integrators.BeemanIntegrator;
import ar.edu.itba.ss.g2.simulation.integrators.Equation;
import ar.edu.itba.ss.g2.simulation.integrators.GearIntegrator;
import ar.edu.itba.ss.g2.simulation.integrators.MovementIntegrator;
import ar.edu.itba.ss.g2.simulation.integrators.VerletIntegrator;
import ar.edu.itba.ss.g2.utils.FileUtil;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class App {
    public static void main(String[] args) {

        ArgParser parser = new ArgParser(args);
        Configuration configuration = parser.parse();

        if (configuration == null) {
            parser.printHelp();
            System.exit(1);
        }

        double m = configuration.getM();
        double k = configuration.getK();
        double A = configuration.getA();
        int N = configuration.getN();
        double w = configuration.getW();

        List<Particle> particleList = new ArrayList<>(N);

        for (int i = 0; i < N; i++) {
            particleList.add(new Particle(i, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, m));
        }

        double dt = configuration.getDt();
        double dt2 = configuration.getDt2();
        double tf = configuration.getTf();

        MovementIntegrator integrator;

        Equation forceEquation = 
        (particles, t) -> {
            List<Double> result = new ArrayList<>(N);
            double yAnterior = 0;
            double yActual = particles.get(0).getPosition();
            double ySiguiente = particles.get(1).getPosition();
            // first particle
            double force = -k*(yActual - ySiguiente) + A*Math.cos(w*t);
            result.add(force);
            int limit = N-1;
            for(int i = 1; i < limit; i++) {
                yAnterior = yActual;
                yActual = ySiguiente;
                ySiguiente = particles.get(i+1).getPosition();
                force = -k*((yActual - yAnterior) + (yActual - ySiguiente));
                result.add(force);
            }
            yAnterior = yActual;
            yActual = ySiguiente;
            // last particle
            force = -k*((yActual - yAnterior) + (yActual - 0));
            result.add(force);

            return result;
        };

        switch (configuration.getIntegrator()) {
            case "verlet":
                integrator = new VerletIntegrator(particleList, forceEquation, dt);
                break;
            case "beeman":
                integrator = new BeemanIntegrator(particleList, forceEquation, dt);
                break;
            case "gear":
                integrator = new GearIntegrator(particleList, forceEquation, dt);
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
            FileUtil.serializeStaticCoupled(configuration);
            FileUtil.serializeDynamic(snapshots, outputDir, dt);
        } catch (IOException e){
            System.err.println("Error writing output files: " + e.getMessage());
            System.exit(1);
        }
    }
}
