import unittest

from kelloggs.main import (
    Force,
    Particle,
    Position,
    update_repulsive_forces,
    update_wall_forces,
    BOX_WIDTH
)

class testUpdateRepulsiveForces(unittest.TestCase):
    def setUp(self):
        pass

    def testParticlesApart(self):
        particles = [
            Particle([0.0, 0.0], 1.0),
            Particle([4.0, 0.0], 2.0)
        ]
        update_repulsive_forces(particles)
        self.assertEqual(particles[0].force, [0.0, 0.0])
        self.assertEqual(particles[1].force, [0.0, 0.0])

    def testParticlesTouch(self):
        particles = [
            Particle([0.0, 0.0], 1.0),
            Particle([2.0, 0.0], 1.0)
        ]
        update_repulsive_forces(particles)
        self.assertEqual(particles[0].force, [0.0, 0.0])
        self.assertEqual(particles[1].force, [0.0, 0.0])

    def testParticlesOverlap(self):
        particles = [
            Particle([0.0, 0.0], 2.0),
            Particle([4.0, 0.0], 3.0),
            Particle([8.0, 0.0], 3.0)
        ]
        update_repulsive_forces(particles)
        self.assertTrue(particles[1].force[0] < 0.0)
        self.assertTrue(particles[0].force[0] < 0.0)
        self.assertTrue(particles[2].force[0] > 0.0)
        self.assertTrue(-particles[0].force[0] < particles[2].force[0])


class testUpdateWallForces(unittest.TestCase):
    def setUp(self):
        """
             |     |
          0  |  1  |  2
             |     |
             |     |
             #-----#

          3     4     5
        """
        self.particles = [
            Particle([-1.0, 2.0], 1.0),
            Particle([BOX_WIDTH / 2.0, 2.0], 1.0),
            Particle([BOX_WIDTH + 1.0, 2.0], 1.0),
            Particle([-2.0, -2.0], 1.0),
            Particle([BOX_WIDTH / 2.0, -1.0], 1.0),
            Particle([BOX_WIDTH + 2.0, -2.0], 1.0),
        ]
        update_wall_forces(self.particles)

    def testForceParticle0(self):
        self.assertTrue(self.particles[0].force[0] > 0)
        self.assertEqual(self.particles[0].force[1], 0.0)
