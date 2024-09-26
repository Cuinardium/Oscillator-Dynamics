package ar.edu.itba.ss.g2.model;

public class Particle {
    private int id;

    private Double position;
    private Double v;

    private final Double mass;

    public Particle(int id, Double position, Double v, Double mass) {
        this.id = id;
        this.position = position;
        this.v = v;
        this.mass = mass;
    }

    public Particle(Particle particle) {
        this.id = particle.id;
        this.position = particle.position;
        this.v = particle.v;
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

    public Double getMass() {
        return mass;
    }

    public void setPosition(Double position) {
        this.position = position;
    }

    public void setV(Double v) {
        this.v = v;
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
