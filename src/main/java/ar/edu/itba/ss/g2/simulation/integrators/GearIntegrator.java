package ar.edu.itba.ss.g2.simulation.integrators;

import ar.edu.itba.ss.g2.model.Particle;

import java.util.List;

public class GearIntegrator implements MovementIntegrator {

    private final List<Particle> particles;

    private final double dt;

    private final Equation forceEquation;

    private double time;

    public GearIntegrator(List<Particle> particles, Equation forceEquation, double dt) {
        this.particles = particles.stream().map(Particle::new).toList();
        this.dt = dt;
        this.forceEquation = forceEquation;
        this.time = 0;
    }

    @Override
    public List<Particle> getState() {
        return particles.stream().map(Particle::new).toList();
    }

    @Override
    public void integrate() {

        // Predict
        for (int i = 0; i < particles.size(); i++) {

            Particle particle = particles.get(i);

            double r5 = particle.getR5();
            double nextR5 = r5;

            double r4 = particle.getR4();
            double nextR4 = r4 + r5 * dt;

            double r3 = particle.getR3();
            double nextR3 = r3 + r4 * dt + r5 * (Math.pow(dt, 2) / 2);

            double r2 = particle.getR2();
            double nextR2 =
                    r2 + r3 * dt + r4 * (Math.pow(dt, 2) / 2) + r5 * (Math.pow(dt, 3) / (3 * 2));

            double r1 = particle.getV();
            double nextR1 =
                    r1
                            + r2 * dt
                            + r3 * (Math.pow(dt, 2) / 2)
                            + r4 * (Math.pow(dt, 3) / (3 * 2))
                            + r5 * (Math.pow(dt, 4) / (4 * 3 * 2));

            double r = particle.getPosition();
            double nextR =
                    r
                            + r1 * dt
                            + r2 * (Math.pow(dt, 2) / 2)
                            + r3 * (Math.pow(dt, 3) / (3 * 2))
                            + r4 * (Math.pow(dt, 4) / (4 * 3 * 2))
                            + r5 * (Math.pow(dt, 5) / (5 * 4 * 3 * 2));

            particle.setR5(nextR5);
            particle.setR4(nextR4);
            particle.setR3(nextR3);
            particle.setR2(nextR2);
            particle.setV(nextR1);
            particle.setPosition(nextR);
        }

        time += dt;
        List<Double> forces = forceEquation.apply(particles, time);

        // Correct
        for (int i = 0; i < particles.size(); i++) {
            Particle particle = particles.get(i);
            double force = forces.get(i);

            double da = force / particle.getMass() - particle.getR2();
            double dR2 = da * Math.pow(dt, 2) / 2;

            double rc = particle.getPosition() + (3.0 / 16.0) * dR2;
            double r1c = particle.getV() + (251.0 / 360.0) * dR2 * (1 / dt);
            double r2c = particle.getR2() + dR2 * (2 / Math.pow(dt, 2));
            double r3c = particle.getR3() + (11.0 / 18.0) * dR2 * ((3 * 2) / Math.pow(dt, 3));
            double r4c = particle.getR4() + (1.0 / 6.0) * dR2 * ((4 * 3 * 2) / Math.pow(dt, 4));
            double r5c =
                    particle.getR5() + (1.0 / 60.0) * dR2 * ((5 * 4 * 3 * 2) / Math.pow(dt, 5));

            particle.setR5(r5c);
            particle.setR4(r4c);
            particle.setR3(r3c);
            particle.setR2(r2c);
            particle.setV(r1c);
            particle.setPosition(rc);
        }
    }
}
