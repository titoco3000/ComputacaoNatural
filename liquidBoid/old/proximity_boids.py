import pygame
from pygame import Vector2 as Vec2
import numpy as np
import random
import math

BOID_RADIUS = 5
SIGHT_DISTANCE = 50
BOID_AVOID_FORCE = 0.5
OBSTACLE_AVOID_FORCE = 0.05
BORDER_PADDING = 3
NUM_BOIDS = 160
MAX_SPEED = 2
BOID_COLOR = (0, 0, 200)
DRAG = 0.999

SIM_SIZE = (400, 300)


class Boid:
    def __init__(self, width, height):
        self.pos = Vec2(random.uniform(0, width), random.uniform(0, height))
        angle = random.uniform(0, 2 * math.pi)
        self.vel = Vec2(math.cos(angle), math.sin(angle)) * MAX_SPEED
        self.width = width
        self.height = height

    def draw(self, screen):
        # Draw a triangle pointing in the direction of velocity
        angle = self.vel.angle_to(Vec2(1, 0))
        points = [
            Vec2(BOID_RADIUS * 2, 0),
            Vec2(-BOID_RADIUS, BOID_RADIUS),
            Vec2(-BOID_RADIUS, -BOID_RADIUS),
        ]
        # Rotate and translate
        rotated = [p.rotate(-angle) + self.pos for p in points]
        pygame.draw.polygon(screen, BOID_COLOR, rotated)

    def avoid_others(self, others):
        force = Vec2(0, 0)
        for other in others:
            diff = self.pos - other.pos
            dist = diff.length()
            if dist < 4 * BOID_RADIUS and dist > 0:
                force += diff.normalize() / dist
        return force

    def avoid_borders(self):
        force = Vec2(0, 0)
        if self.pos.x < BORDER_PADDING:
            force.x += BORDER_PADDING - self.pos.x
        elif self.pos.x > self.width - BORDER_PADDING:
            force.x += self.width - BORDER_PADDING - self.pos.x
        if self.pos.y < BORDER_PADDING:
            force.y += BORDER_PADDING - self.pos.y
        elif self.pos.y > self.height - BORDER_PADDING:
            force.y += self.height - BORDER_PADDING - self.pos.y
        return force

    def update(self, others):
        avoid_force = self.avoid_others(others) * BOID_AVOID_FORCE
        border_force = self.avoid_borders() * OBSTACLE_AVOID_FORCE
        self.vel = (self.vel + avoid_force + border_force) * DRAG + Vec2(0, 0.03)
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)
        self.pos += self.vel
        # self.pos.x = max(0, min(SIM_SIZE[0], self.pos.x))
        self.pos.y = max(0, min(SIM_SIZE[1], self.pos.y))


def main():
    pygame.init()
    screen = pygame.display.set_mode(SIM_SIZE)
    pygame.display.set_caption("Boids")
    clock = pygame.time.Clock()
    width, height = screen.get_size()

    boids = [Boid(width, height) for _ in range(NUM_BOIDS)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            boids = [Boid(width, height) for _ in range(NUM_BOIDS)]

        for boid in boids:
            boid.update(boids)

        screen.fill((0, 0, 0))
        for boid in boids:
            boid.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
