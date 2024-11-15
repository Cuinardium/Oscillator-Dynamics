package ar.edu.itba.ss.g2.dampened.config;

public class Configuration {
    private final double m;
    private final double k;
    private final double gamma;
    private final double tf;
    private final double r0;
    private final double dt;
    private final double dt2;

    private final String integrator;

    private final String outputDir;

    private Configuration(Builder builder) {
        this.m = builder.m;
        this.k = builder.k;
        this.gamma = builder.gamma;
        this.tf = builder.tf;
        this.r0 = builder.r0;
        this.dt = builder.dt;
        this.dt2 = builder.dt2;

        this.integrator = builder.integrator;
        
        this.outputDir = builder.outputDir;
    }

    public double getM() {
        return m;
    }

    public double getK() {
        return k;
    }

    public double getGamma() {
        return gamma;
    }

    public double getTf() {
        return tf;
    }

    public double getR0() {
        return r0;
    }

    public double getDt() {
        return dt;
    }

    public double getDt2() {
        return dt2;
    }

    public String getIntegrator() {
        return integrator;
    }

    public String getOutputDir() {
        return outputDir;
    }

    public static class Builder {
        private double m;
        private double k;
        private double gamma;
        private double tf;
        private double r0;
        private double dt;
        private double dt2;

        private String integrator;

        private String outputDir;

        public Builder setM(double m) {
            this.m = m;
            return this;
        }

        public Builder setK(double k) {
            this.k = k;
            return this;
        }

        public Builder setGamma(double gamma) {
            this.gamma = gamma;
            return this;
        }

        public Builder setTf(double tf) {
            this.tf = tf;
            return this;
        }

        public Builder setR0(double r0) {
            this.r0 = r0;
            return this;
        }

        public Builder setDt(double dt) {
            this.dt = dt;
            return this;
        }

        public Builder setDt2(double dt2) {
            this.dt2 = dt2;
            return this;
        }

        public Builder setIntegrator(String integrator) {
            this.integrator = integrator;
            return this;
        }

        public Builder setOutputDir(String outputDir) {
            this.outputDir = outputDir;
            return this;
        }

        public Configuration build() {
            return new Configuration(this);
        }
    }
}
