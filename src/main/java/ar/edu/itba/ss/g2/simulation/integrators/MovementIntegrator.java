package ar.edu.itba.ss.g2.simulation.integrators;

import java.util.List;

import ar.edu.itba.ss.g2.model.Particle;

public interface MovementIntegrator {

    List<Particle> getState();

    void integrate();
}
