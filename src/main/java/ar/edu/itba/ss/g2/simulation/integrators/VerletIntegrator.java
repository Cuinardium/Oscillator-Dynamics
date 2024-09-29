package ar.edu.itba.ss.g2.simulation.integrators;

import ar.edu.itba.ss.g2.model.Particle;

import java.util.ArrayList;
import java.util.List;

public class VerletIntegrator implements MovementIntegrator {

    private final List<Particle> particles;
    private final List<Particle> previousParticles;

    private final double deltaTime;

    private final Equation forceEquation;

    private double time;

    public VerletIntegrator(List<Particle> particles, Equation forceEquation, double deltaTime) {
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
        List<Double> forces = forceEquation.apply(particles, time);

        for (int i = 0; i < particles.size(); i++) {

            Particle particle = particles.get(i);
            Particle previousParticle = previousParticles.get(i);

            double mass = particle.getMass();

            // r(t)
            double currentPosition = particle.getPosition();

            // r(t-dt)
            double previousPosition = previousParticle.getPosition();

            // f(t)
            double force = forces.get(i);

            // r(t+dt) = 2r(t) - r(t-dt) + (dt^2 / m) * f(t)
            double nextPosition =
                    2 * currentPosition
                            - previousPosition
                            + (Math.pow(deltaTime, 2) / mass) * force;

            // v(t) = (r(t+dt) - r(t-dt)) / 2dt
            double currentVelocity = (nextPosition - previousPosition) / (2 * deltaTime);

            previousParticle.setPosition(currentPosition);
            previousParticle.setV(currentVelocity);

            // TODO (mal?): v(t+dt) = (r(t+dt) - r(t)) / dt
            double nextVelocity = (nextPosition - currentPosition) / deltaTime;

            particle.setPosition(nextPosition);
            particle.setV(nextVelocity);
        }
    }
}
