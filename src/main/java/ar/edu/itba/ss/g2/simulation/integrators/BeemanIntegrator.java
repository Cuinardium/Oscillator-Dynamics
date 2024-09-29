package ar.edu.itba.ss.g2.simulation.integrators;

import ar.edu.itba.ss.g2.model.Particle;

import java.util.ArrayList;
import java.util.List;

public class BeemanIntegrator implements MovementIntegrator {

    private final List<Particle> particles;
    private final List<Particle> previousParticles;

    private final double deltaTime;

    private final Equation forceEquation;

    private double time;

    public BeemanIntegrator(List<Particle> particles, Equation forceEquation, double deltaTime) {
        this.deltaTime = deltaTime;
        this.particles = new ArrayList<>(particles);
        this.previousParticles = new ArrayList<>(particles.size());
        this.time = 0;

        // Euler for new pos and vel
        List<Double> forces = forceEquation.apply(particles, time);
        for (int i = 0; i < particles.size(); i++) {
            Particle particle = particles.get(i);
            double previousPosition =
                    particle.getPosition()
                            - particle.getV() * deltaTime
                            + (deltaTime * deltaTime / (2 * particle.getMass())) * forces.get(i);

            double previousVelocity =
                    particle.getV() - (deltaTime / particle.getMass()) * forces.get(i);

            previousParticles.add(
                    new Particle(
                            particle.getId(),
                            previousPosition,
                            previousVelocity,
                            particle.getMass()));
        }

        this.forceEquation = forceEquation;
    }

    @Override
    public List<Double> getState() {
        return particles.stream().map(Particle::getPosition).toList();
    }

    @Override
    public void integrate() {
        time += deltaTime;
        List<Double> currentForces = forceEquation.apply(particles, time);
        List<Double> previousForces = forceEquation.apply(previousParticles, time);

        // Positions
        for (int i = 0; i < particles.size(); i++) {

            Particle particle = particles.get(i);
            Particle previousParticle = previousParticles.get(i);

            double mass = particle.getMass();

            // r(t)
            double currentPosition = particle.getPosition();

            // v(t)
            double currentVelocity = particle.getV();

            // a(t)
            double currentAcceleration = currentForces.get(i) / mass;

            // a(t-dt)
            double previousAcceleration = previousForces.get(i) / mass;

            // r(t+dt)
            double nextPosition =
                    currentPosition
                            + currentVelocity * deltaTime
                            + (2.0 / 3.0) * currentAcceleration * Math.pow(deltaTime, 2)
                            - (1.0 / 6.0) * previousAcceleration * Math.pow(deltaTime, 2);

            // predicted v(t+dt)
            double predictedVelocity =
                    currentVelocity
                            + (3.0 / 2.0) * currentAcceleration * deltaTime
                            - (1.0 / 2.0) * previousAcceleration * deltaTime;

            previousParticle.setPosition(currentPosition);
            previousParticle.setV(currentVelocity);

            particle.setPosition(nextPosition);
            particle.setV(predictedVelocity);
        }

        List<Double> nextForces = forceEquation.apply(particles, time);

        // Correct velocities
        for (int i = 0; i < particles.size(); i++) {

            Particle particle = particles.get(i);
            Particle previousParticle = previousParticles.get(i);

            double mass = particle.getMass();

            // v(t)
            double currentVelocity = previousParticle.getV();

            // a(t-dt), a(t), a(t+dt)
            double previousAcceleration = previousForces.get(i) / mass;
            double currentAcceleration = currentForces.get(i) / mass;
            double nextAcceleration = nextForces.get(i) / mass;

            // corrected v(t+dt)
            double correctedVelocity =
                    currentVelocity
                            + (1.0 / 3.0) * nextAcceleration * deltaTime
                            + (5.0 / 6.0) * currentAcceleration * deltaTime
                            - (1.0 / 6.0) * previousAcceleration * deltaTime;

            particle.setV(correctedVelocity);
        }
    }
}
