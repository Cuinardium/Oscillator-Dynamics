package ar.edu.itba.ss.g2.utils;

import ar.edu.itba.ss.g2.model.Particle;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.List;

public class FileUtil {

    private FileUtil() {
        throw new RuntimeException("Util class");
    }

    public static void serializeStaticDampened(
            ar.edu.itba.ss.g2.dampened.config.Configuration configuration) throws IOException {

        String directory = configuration.getOutputDir();

        // Create directory if it doesn't exist
        File dir = new File(directory);
        if (!dir.exists()) {
            dir.mkdirs();
        }

        // Static
        try (FileWriter writer = new FileWriter(directory + "/static.txt")) {
            writer.write(configuration.getM() + "\n");
            writer.write(configuration.getK() + "\n");
            writer.write(configuration.getGamma() + "\n");
            writer.write(configuration.getR0() + "\n");
            writer.write(configuration.getDt() + "\n");
            writer.write(configuration.getDt2() + "\n");
            writer.write(configuration.getTf() + "\n");
            writer.write(configuration.getIntegrator() + "\n");
        }
    }

    public static void serializeDynamic(List<List<Particle>> snapshots, String directory, Double dt)
            throws IOException {
        try (BufferedWriter writer =
                new BufferedWriter(new FileWriter(directory + "/dynamic.txt"))) {
            for (int i = 0; i < snapshots.size(); i++) {
                double t = i * dt;
                writer.write(t + "\n");

                List<Particle> snapshot = snapshots.get(i);
                for (Particle particle : snapshot) {
                    writer.write(
                            String.format("%.7f %.7f\n", particle.getPosition(), particle.getV()));
                }
            }
        }
    }
}
