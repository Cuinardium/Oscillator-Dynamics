package ar.edu.itba.ss.g2.dampened.config;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.Options;

import java.util.Comparator;
import java.util.List;

public class ArgParser {

    private static final List<Option> OPTIONS =
            List.of(
                    new Option("m", "mass", true, "Mass (kg)"),
                    new Option("k", "spring", true, "Spring constant (N/m)"),
                    new Option("g", "gamma", true, "Damping coefficient (kg/s)"),
                    new Option("tf", "time", true, "Final time (s)"),
                    new Option("r0", "position", true, "Initial position (m)"),
                    new Option("dt", "delta", true, "Integration time step (s)"),
                    new Option("dt2", "delta2", true, "Snapshot time step (s)"),
                    new Option("out", "output", true, "Output directory"),
                    new Option("h", "help", false, "Print help"));

    private final String[] args;
    private final Options options;

    public ArgParser(String[] args) {
        this.args = args;

        this.options = new Options();
        OPTIONS.forEach(options::addOption);
    }

    public Configuration parse() {
        CommandLineParser parser = new DefaultParser();
        CommandLine cmd;

        Options cliOptions = new Options();
        OPTIONS.forEach(cliOptions::addOption);

        try {
            // Parse the arguments
            cmd = parser.parse(cliOptions, args);

            // Use the builder pattern for creating Configuration instance
            Configuration.Builder builder = new Configuration.Builder();
            if (cmd.hasOption("h")) {
                printHelp();
                return null;
            }
            if (!cmd.hasOption("m")
                    || !cmd.hasOption("k")
                    || !cmd.hasOption("g")
                    || !cmd.hasOption("tf")
                    || !cmd.hasOption("r0")
                    || !cmd.hasOption("dt")
                    || !cmd.hasOption("dt2")
                    || !cmd.hasOption("out")) {
                System.out.println("Error: Missing parameters. All parameters are required.");
                return null;
            }

            // Parse and set parameters, with individual error messages for each
            try {

                builder.setM(Double.parseDouble(cmd.getOptionValue("m")));
            } catch (NumberFormatException e) {
                System.out.println("Error: Invalid format for mass (m). Expected a valid number.");
                return null;
            }

            try {
                builder.setK(Double.parseDouble(cmd.getOptionValue("k")));
            } catch (NumberFormatException e) {
                System.out.println(
                        "Error: Invalid format for spring constant (k). Expected a valid number.");
                return null;
            }

            try {
                builder.setGamma(Double.parseDouble(cmd.getOptionValue("g")));
            } catch (NumberFormatException e) {
                System.out.println(
                        "Error: Invalid format for damping coefficient (gamma). Expected a valid"
                                + " number.");
                return null;
            }

            try {
                builder.setTf(Double.parseDouble(cmd.getOptionValue("tf")));
            } catch (NumberFormatException e) {
                System.out.println(
                        "Error: Invalid format for final time (tf). Expected a valid number.");
                return null;
            }

            try {
                builder.setR0(Double.parseDouble(cmd.getOptionValue("r0")));
            } catch (NumberFormatException e) {
                System.out.println(
                        "Error: Invalid format for initial position (r0). Expected a valid"
                                + " number.");
                return null;
            }

            try {
                builder.setDt(Double.parseDouble(cmd.getOptionValue("dt")));
            } catch (NumberFormatException e) {
                System.out.println(
                        "Error: Invalid format for integration time step (dt). Expected a valid"
                                + " number.");
                return null;
            }

            try {
                builder.setDt2(Double.parseDouble(cmd.getOptionValue("dt2")));
            } catch (NumberFormatException e) {
                System.out.println(
                        "Error: Invalid format for snapshot time step (dt2). Expected a valid"
                                + " number.");
                return null;
            }

            builder.setOutputDir(cmd.getOptionValue("out"));

            // Build and return the configuration object
            return builder.build();

        } catch (Exception e) {
            System.out.println("Error: Missing or invalid parameters. " + e.getMessage());
        }

        return null; // Return null if there was an error
    }

    public void printHelp() {

        HelpFormatter formatter = new HelpFormatter();
        formatter.setOptionComparator(Comparator.comparingInt(OPTIONS::indexOf));

        formatter.setLeftPadding(4);
        formatter.setWidth(120);

        String commandLineSyntax =
                "java -jar dampened-oscillator-jar-with-dependencies.jar"
                        + " [options]";

        formatter.printHelp(commandLineSyntax, options);
    }
}
