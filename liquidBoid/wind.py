import pygame
from pygame import Vector2 as Vec2
import random
import math

BOID_COLOR = (0, 0, 200)
TRAIL_COLOR = (255, 255, 255)
SIM_SIZE = (1000, 800)
BOID_RADIUS = 5
NUM_BOIDS = 500
MAX_SPEED = 4

NOISE = 0.01
ALIGNMENT = 0.1
SEPARATION = 10
INFLUENCE_RADIUS = 5 * BOID_RADIUS
OBSTACLE_INFLUENCE_RADIUS = 3 * BOID_RADIUS
INERTIA = 0.9
DRAG = 0.0001


def vec2_lerp(a, b, c):
    return Vec2(a.x * (1 - c) + b.x * c, a.y * (1 - c) + b.y * c)


class Boid:
    def __init__(self):
        self.reset()

    def reset(self):
        self.pos = Vec2(-BOID_RADIUS, random.uniform(0, SIM_SIZE[1]))
        self.vel = Vec2(MAX_SPEED, 0)

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
        # get other boids that are close enough to affect
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
            separation_force += diff.normalize() / (dist + 0.1)
        separation_force *= SEPARATION

        # move to the start when leaving the area
        if (
            self.pos.x < -BOID_RADIUS
            or self.pos.x > SIM_SIZE[0]
            or self.pos.y < -BOID_RADIUS
            or self.pos.y > SIM_SIZE[1] + BOID_RADIUS
        ):
            self.reset()

        # avoid obstacles
        avoidance_force = Vec2()
        for obs in obstacles:
            for i in range(len(obs.vertices)):
                a = obs.vertices[i]
                b = obs.vertices[(i + 1) % len(obs.vertices)]
                closest = _closest_point_on_segment(a, b, self.pos)
                dist = self.pos.distance_to(closest)
                if dist < OBSTACLE_INFLUENCE_RADIUS:
                    away = self.pos - closest
                    if away.length() > 0:
                        avoidance_force += away.normalize() * (
                            OBSTACLE_INFLUENCE_RADIUS - dist
                        )

        # noise
        random_force = Vec2(random.uniform(-1, 1), random.uniform(-1, 1)) * NOISE

        # Combine forces
        self.vel = vec2_lerp(
            (self.vel + align_force + separation_force + avoidance_force + random_force)
            * (1 - DRAG),
            self.vel,
            INERTIA,
        )

        # Limit speed
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)

        self.pos += self.vel

        # for obs in obstacles:
        #     if obs.contains(self.pos):
        #         self.reset()
        #         break

    def marcar(self, surface):
        surface.set_at((int(self.pos.x), int(self.pos.y)), TRAIL_COLOR)


class Obstacle:
    def __init__(self, vertices):
        self.vertices = vertices

    def draw(self, screen):
        pygame.draw.polygon(screen, (200, 50, 50), self.vertices, width=2)

    def contains(self, point):
        x, y = point
        inside = False
        n = len(self.vertices)
        for i in range(n):
            xi, yi = self.vertices[i]
            xj, yj = self.vertices[(i + 1) % n]
            intersect = ((yi > y) != (yj > y)) and (
                x < (xj - xi) * (y - yi) / (yj - yi + 1e-6) + xi
            )
            if intersect:
                inside = not inside
        return inside


def _closest_point_on_segment(a, b, p):
    """Return closest point on segment ab to point p."""
    ab = b - a
    t = max(0, min(1, (p - a).dot(ab) / ab.length_squared()))
    return a + ab * t


def generate_obstacles(num=5):
    obstacles = []
    for _ in range(num):
        center = Vec2(
            random.uniform(100, SIM_SIZE[0] - 100),
            random.uniform(100, SIM_SIZE[1] - 100),
        )
        radius = random.uniform(20, 60)
        sides = random.randint(3, 6)
        angle_offset = random.uniform(0, 2 * math.pi)
        vertices = [
            Vec2(
                center.x + radius * math.cos(2 * math.pi * i / sides + angle_offset),
                center.y + radius * math.sin(2 * math.pi * i / sides + angle_offset),
            )
            for i in range(sides)
        ]
        obstacles.append(Obstacle(vertices))
    return obstacles


def darken_surface(surface, amount=1):
    dark = pygame.Surface(surface.get_size())
    dark.fill((amount, amount, amount))
    surface.blit(dark, (0, 0), special_flags=pygame.BLEND_RGB_SUB)


def main():
    pygame.init()
    screen = pygame.display.set_mode(SIM_SIZE)
    pygame.display.set_caption("Boids")

    rastros = pygame.Surface(SIM_SIZE)
    rastros.fill((0, 0, 0))

    clock = pygame.time.Clock()

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

        darken_surface(rastros)

        screen.blit(rastros, (0, 0))
        for obstacle in obstacles:
            obstacle.draw(screen)
        for boid in boids:
            boid.draw(screen)
            boid.marcar(rastros)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
