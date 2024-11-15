package ar.edu.itba.ss.g2.utils;

import ar.edu.itba.ss.g2.model.Particle;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.text.DecimalFormat;
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

    public static void serializeStaticCoupled(
            ar.edu.itba.ss.g2.coupled.config.Configuration configuration) throws IOException {

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
            writer.write(configuration.getA() + "\n");
            writer.write(configuration.getL0() + "\n");
            writer.write(configuration.getN() + "\n");
            writer.write(configuration.getW() + "\n");
            writer.write(configuration.getDt() + "\n");
            writer.write(configuration.getDt2() + "\n");
            writer.write(configuration.getTf() + "\n");
            writer.write(configuration.getIntegrator() + "\n");
        }
    }

    public static void serializeDynamic(List<List<Double>> snapshots, String directory, Double dt)
            throws IOException {
        System.out.println("Writing...");
        try (BufferedWriter writer =
                new BufferedWriter(new FileWriter(directory + "/dynamic.txt"))) {

            DecimalFormat formatter = new DecimalFormat("0.0000000000000000000000000000");

            int elapsed = 0;
            int printStep = snapshots.size() >= 10 ? snapshots.size() / 10 : 1;

            int particleCount = snapshots.get(0).size();
            int totalSnapshots = snapshots.size();

            writer.write(particleCount + " " + totalSnapshots + "\n");

            for (int i = 0; i < snapshots.size(); i++) {
                double t = (i + 1) * dt;
                writer.write(formatter.format(t) + "\n");

                elapsed++;
                if (elapsed >= printStep) {
                    System.out.println("Progress: " + (i + 1) + "/" + snapshots.size());
                    elapsed = 0;
                }

                List<Double> positions = snapshots.get(i);
                for (Double position : positions) {
                    writer.write(String.format("%s\n", formatter.format(position)));
                }
            }
        }
    }
}
