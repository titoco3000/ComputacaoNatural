import numpy as np
import random
import engine

NUM_POINTS = 1000
ATRITO = 0.99
GRAVIDADE = 0.05
RAIO_BOID = 0.05


class Boid:
    def __init__(self):
        self.randomize()

    def randomize(self):
        self.pos = np.array(
            [random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1), 1.0]
        )
        self.vel = np.array(
            [random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1), 1.0]
        )

    def update_vel(self, boids):
        # adiciona atrito
        self.vel[0] *= ATRITO
        self.vel[1] *= ATRITO
        self.vel[2] *= ATRITO

        # se vai bater num limite:
        # calcula distancia
        # calcula reflexao
        # se vai esbarrar em outra particula:
        # calcula distancia
        # calcula reflexao

        # se calculou distancia e reflexao:
        # aplica reflexao na velocidade usando uma interpolação linear com base na distancia
        # se não:
        # adiciona gravidade
        self.vel[1] -= GRAVIDADE


boids = [Boid() for _ in range(NUM_POINTS)]


def reset_boids(boids):
    random.seed(0)
    for b in boids:
        b.randomize()


def update_boids(boids):
    for b in boids:
        b.update_vel(boids)

        b.pos[0] = max(-1, min(1, b.pos[0] + b.vel[0] * 0.01))
        b.pos[1] = max(-1, min(1, b.pos[1] + b.vel[1] * 0.01))
        b.pos[2] = max(-1, min(1, b.pos[2] + b.vel[2] * 0.01))


engine.run(boids, update_boids, reset_boids)
