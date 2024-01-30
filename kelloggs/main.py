from dataclasses import dataclass
import random
from math import sqrt
from typing import TypeAlias

import matplotlib.axes
import matplotlib.pyplot as plt

DIMENSION = 2
BOX_WIDTH = 100.0
SPRING_CONSTANT = 1.0
WALL_SPRING_CONSTANT = 5.0
GRAVITY_CONSTANT = 1.0
DT = 1.0

Position: TypeAlias = list[float]
Velocity: TypeAlias = list[float]
Force: TypeAlias = list[float]

@dataclass
class Particle:
    position: Position
    radius: float

    def __post_init__(self):
        self.mass = self.radius ** DIMENSION
        self.force = [0.0] * DIMENSION
        self.velocity = [0.0] * DIMENSION


def update_repulsive_forces(particles: list[Particle]) -> None:
    for i in range(len(particles)):
        for j in range(i+1, len(particles)):
            pos_ix, pos_iy = particles[i].position
            pos_jx, pos_jy = particles[j].position
            distance = sqrt((pos_ix - pos_jx) ** 2 + (pos_iy - pos_jy) ** 2)
            if (elongation := particles[i].radius + particles[j].radius - distance) > 0:
                force_ix = SPRING_CONSTANT * elongation * (pos_ix - pos_jx) / distance
                force_iy = SPRING_CONSTANT * elongation * (pos_iy - pos_jy) / distance
                particles[i].force[0] += force_ix
                particles[i].force[1] += force_iy
                particles[j].force[0] -= force_ix
                particles[j].force[1] -= force_iy


def update_wall_forces(particles: list[Particle]) -> None:
    for particle in particles:
        # left wall
        if (elongation := particle.radius - particle.position[0]) > 0:
            particle.force[0] += WALL_SPRING_CONSTANT * elongation
        # right wall
        if (elongation := particle.position[0] + particle.radius - BOX_WIDTH) > 0:
            particle.force[0] -= WALL_SPRING_CONSTANT * elongation
        # bottom wall
        if (elongation := particle.radius - particle.position[1]) > 0:
            particle.force[1] += WALL_SPRING_CONSTANT * elongation


def apply_gravity(particles: list[Particle]) -> None:
    for particle in particles:
        particle.force[1] -= particle.mass * GRAVITY_CONSTANT


def setup_initial_state() -> list[Particle]:
    return [Particle([random.uniform(0, BOX_WIDTH), random.uniform(0, BOX_WIDTH)], random.uniform(5, 15)) for _ in range(20)]


def compute_forces(particles: list[Particle]) -> None:
    for particle in particles:
        particle.force = [0.0, 0.0]

    update_wall_forces(particles)
    update_repulsive_forces(particles)
    apply_gravity(particles)


def setup_dynamics(particles: list[Particle]):
    compute_forces(particles)
    for particle in particles:
        particle.velocity = [0.0, 0.0]
    for particle in particles:
        particle.velocity[0] += 0.5 * DT * particle.force[0] / particle.mass
        particle.velocity[1] += 0.5 * DT * particle.force[1] / particle.mass


def dynamic_step(particles: list[Particle]) -> None:
    for particle in particles:
        particle.position[0] += DT * particle.velocity[0]
        particle.position[1] += DT * particle.velocity[1]
    compute_forces(particles)
    for particle in particles:
        particle.velocity[0] += DT * particle.force[0] / particle.mass
        particle.velocity[1] += DT * particle.force[1] / particle.mass


def finish_dynamics(particles: list[Particle]) -> None:
    for particle in particles:
        particle.position[0] += DT * particle.velocity[0]
        particle.position[1] += DT * particle.velocity[1]
    compute_forces(particles)
    for particle in particles:
        particle.velocity[0] += 0.5 * DT * particle.force[0] / particle.mass
        particle.velocity[1] += 0.5 * DT * particle.force[1] / particle.mass


def run_dynamics(particles: list[Particle], num_steps: int) -> None:
    setup_dynamics(particles)
    for _ in range(1, num_steps):
        dynamic_step(particles)
    finish_dynamics(particles)


def draw_box(ax: matplotlib.axes.Axes) -> None:
    ax.axline((0.0, 0.0), (0.0, 1000.0))
    ax.plot((0.0, BOX_WIDTH), (0.0, 0.0))
    ax.axline((BOX_WIDTH, 0.0), (BOX_WIDTH, 1000.0))

def draw_particle(particle: Particle, ax: matplotlib.axes.Axes) -> None:
    ax.add_patch(plt.Circle(particle.position, int(particle.radius), fill=False))  # type: ignore=
    ax.arrow(*particle.position, *particle.force, width=1)

def main() -> None:
    fig = plt.figure()
    ax = fig.add_subplot()
    draw_box(ax)
    particles = setup_initial_state()
    update_wall_forces(particles)
    update_repulsive_forces(particles)
    for particle in particles:
        draw_particle(particle, ax)
    ax.set_aspect("equal")
    ax.set_ylim((-10, BOX_WIDTH))
    plt.show()


if __name__ == "__main__":
    main()
