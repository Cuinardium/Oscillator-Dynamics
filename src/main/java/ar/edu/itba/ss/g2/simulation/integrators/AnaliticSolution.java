package ar.edu.itba.ss.g2.simulation.integrators;

import java.util.List;

import ar.edu.itba.ss.g2.model.Particle;

public class AnaliticSolution  implements MovementIntegrator {

    private final List<Particle> particles;

    private final double dt;
    private double time;

    private final Equation positionEquation;

    public AnaliticSolution(List<Particle> particles, Equation positionEquation, double dt) {
        this.particles = particles;
        this.dt = dt;
        this.positionEquation = positionEquation;
        this.time = 0;
    }

    @Override
    public List<Particle> getState() {
        return particles.stream().map(Particle::new).toList();
    }

    @Override
    public void integrate() {
        time += dt;
        List<Double> positions = positionEquation.apply(particles, time);

        for (int i = 0; i < particles.size(); i++) {
            particles.get(i).setPosition(positions.get(i));
        }
    }
}
