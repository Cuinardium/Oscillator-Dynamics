package ar.edu.itba.ss.g2.simulation.integrators;

import java.util.List;

import ar.edu.itba.ss.g2.model.Particle;

@FunctionalInterface
public interface Equation {
    List<Double> apply(List<Particle> state, double t);
}
