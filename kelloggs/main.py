from dataclasses import dataclass
from math import sqrt
from typing import TypeAlias


DIMENSION = 2
BOX_WIDTH = 100.0
SPRING_CONSTANT = 1.0
WALL_SPRING_CONSTANT = 100.0
GRAVITY_CONSTANT = 1.0

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
        if (elongation := -particle.position[0] - particle.radius) > 0:
            particle.force[0] += WALL_SPRING_CONSTANT * elongation
        # right wall
        if (elongation := particle.position[0] + particle.radius - BOX_WIDTH) > 0:
            particle.force[0] -= WALL_SPRING_CONSTANT * elongation
        # bottom wall
        if (elongation := -particle.position[1] - particle.radius) > 0:
            particle.force[1] += WALL_SPRING_CONSTANT * elongation


def main() -> None:
    pass

if __name__ == "__main__":
    main()
