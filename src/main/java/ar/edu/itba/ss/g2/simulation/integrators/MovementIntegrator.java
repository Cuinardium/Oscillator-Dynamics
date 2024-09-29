package ar.edu.itba.ss.g2.simulation.integrators;

import java.util.List;

public interface MovementIntegrator {

    List<Double> getState();

    void integrate();
}
