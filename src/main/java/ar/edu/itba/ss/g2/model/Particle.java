package ar.edu.itba.ss.g2.model;

public class Particle {
    private int id;

    private Double position;
    private Double v;
    private Double r2;
    private Double r3;
    private Double r4;
    private Double r5;

    private final Double mass;

    public Particle(int id, Double position, Double v, Double mass) {
        this.id = id;
        this.position = position;
        this.v = v;
        this.mass = mass;
    }

    public Particle(
            int id,
            Double position,
            Double v,
            Double r2,
            Double r3,
            Double r4,
            Double r5,
            Double mass) {
        this.id = id;
        this.position = position;
        this.v = v;
        this.r2 = r2;
        this.r3 = r3;
        this.r4 = r4;
        this.r5 = r5;
        this.mass = mass;
    }

    public Particle(Particle particle) {
        this.id = particle.id;
        this.position = particle.position;
        this.v = particle.v;
        this.r2 = particle.r2;
        this.r3 = particle.r3;
        this.r4 = particle.r4;
        this.r5 = particle.r5;
        this.mass = particle.mass;
    }

    public int getId() {
        return id;
    }

    public Double getPosition() {
        return position;
    }

    public Double getV() {
        return v;
    }

    public Double getR2() {
        return r2;
    }

    public Double getR3() {
        return r3;
    }

    public Double getR4() {
        return r4;
    }

    public Double getR5() {
        return r5;
    }

    public Double getMass() {
        return mass;
    }

    public void setPosition(Double position) {
        this.position = position;
    }

    public void setV(Double v) {
        this.v = v;
    }

    public void setR2(Double r2) {
        this.r2 = r2;
    }

    public void setR3(Double r3) {
        this.r3 = r3;
    }

    public void setR4(Double r4) {
        this.r4 = r4;
    }

    public void setR5(Double r5) {
        this.r5 = r5;
    }

    @Override
    public String toString() {
        return "Particle{"
                + "id="
                + id
                + ", position="
                + position
                + ", v="
                + v
                + ", mass="
                + mass
                + '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Particle particle)) return false;
        return this.id == particle.id;
    }

    @Override
    public int hashCode() {
        return Integer.hashCode(id);
    }
}
