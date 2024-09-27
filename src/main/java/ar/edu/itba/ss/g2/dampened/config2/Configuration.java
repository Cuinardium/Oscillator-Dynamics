package ar.edu.itba.ss.g2.dampened.config2;

public class Configuration {
    private final double m;
    private final double k;
    private final double A;
    private final double l0;
    private final int N;
    private final double tf;
    private final double dt;
    private final double dt2;

    private final String integrator;

    private final String outputDir;

    private Configuration(Builder builder) {
        this.m = builder.m;
        this.k = builder.k;
        this.A = builder.A;
        this.l0 = builder.l0;
        this.N = builder.N;
        this.tf = builder.tf;
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

    public double getA() {
        return A;
    }

    public double getL0() {
        return l0;
    }

    public int getN() {
        return N;
    }

    public double getTf() {
        return tf;
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
        private double A;
        private double l0;
        private int N;
        private double tf;
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

        public Builder setA(double A) {
            this.A = A;
            return this;
        }

        public Builder setL0(double l0) {
            this.l0 = l0;
            return this;
        }

        public Builder setN(int N) {
            this.N = N;
            return this;
        }

        public Builder setTf(double tf) {
            this.tf = tf;
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
