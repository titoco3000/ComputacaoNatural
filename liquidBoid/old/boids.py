import pygame
from pygame import Vector2 as Vec2
import numpy as np
import random
import math

BOID_COLOR = (0, 0, 200)
BOID_RADIUS = 5
SIM_SIZE = (400, 300)
MAX_SPEED = 2
NUM_BOIDS = 300

NOISE = 0.01
ALIGNMENT = 0.001
SEPARATION = 1
GRAVITY = 0.098
INFLUENCE_RADIUS = 30
INERCIA = 0.9
DRAG = 0.01


def vec2_lerp(a, b, c):
    return Vec2(a.x * (1 - c) + b.x * c, a.y * (1 - c) + b.y * c)


class Boid:
    def __init__(self):
        self.pos = Vec2(random.uniform(0, SIM_SIZE[0]), random.uniform(0, SIM_SIZE[1]))
        angle = random.uniform(0, 2 * math.pi)
        self.vel = Vec2(math.cos(angle), math.sin(angle)) * MAX_SPEED

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

    def update(self, others, obstacles):
        neighbors = [
            b
            for b in others
            if b != self and self.pos.distance_to(b.pos) < INFLUENCE_RADIUS
        ]

        # Alignment: steer towards the average velocity of neighbors
        if neighbors:
            avg_vel = sum((b.vel for b in neighbors), Vec2()) / len(neighbors)
            align_force = (avg_vel - self.vel) * ALIGNMENT
        else:
            align_force = Vec2()

        # Separation: steer away from close neighbors
        separation_force = Vec2()
        for b in neighbors:
            dist = self.pos.distance_to(b.pos)
            diff = self.pos - b.pos
            separation_force += diff.normalize() / (dist + 0.01)
        separation_force *= SEPARATION

        # Obstacle and wall avoidance
        avoidance_force = Vec2()
        padding = 1
        if self.pos.x < padding:
            avoidance_force.x += 1
        elif self.pos.x > SIM_SIZE[0] - padding:
            avoidance_force.x -= 1
        if self.pos.y < padding:
            avoidance_force.y += 1
        elif self.pos.y > SIM_SIZE[1] - padding:
            avoidance_force.y -= 1

        for p1, p2 in obstacles:
            closest_point = self._closest_point_on_segment(p1, p2, self.pos)
            dist = self.pos.distance_to(closest_point)
            if dist < 30:
                avoidance_force += (self.pos - closest_point).normalize() / dist

        random_force = Vec2(random.uniform(-1, 1), random.uniform(-1, 1)) * NOISE

        gravity_force = Vec2(0, GRAVITY)

        # Combine forces
        self.vel = vec2_lerp(
            self.vel,
            (
                self.vel
                + align_force
                + separation_force
                + avoidance_force
                + random_force
                + gravity_force
            )
            * (1 - DRAG),
            INERCIA,
        )

        # Limit speed
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)

        self.pos += self.vel

    def _closest_point_on_segment(self, a, b, p):
        """Return closest point on segment ab to point p."""
        ab = b - a
        t = max(0, min(1, (p - a).dot(ab) / ab.length_squared()))
        return a + ab * t


def generate_obstacles(num=10):
    obstacles = []
    for _ in range(num):
        p1 = Vec2(random.randint(0, SIM_SIZE[0]), random.randint(0, SIM_SIZE[1]))
        p2 = p1 + Vec2(random.randint(-50, 50), random.randint(-50, 50))
        obstacles.append((p1, p2))
    return obstacles


def main():
    pygame.init()
    screen = pygame.display.set_mode(SIM_SIZE)
    pygame.display.set_caption("Boids")
    clock = pygame.time.Clock()
    width, height = screen.get_size()

    obstacles = generate_obstacles()

    boids = [Boid() for _ in range(NUM_BOIDS)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            boids = [Boid() for _ in range(NUM_BOIDS)]

        for boid in boids:
            boid.update(boids, obstacles)

        screen.fill((0, 0, 0))
        for boid in boids:
            boid.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
