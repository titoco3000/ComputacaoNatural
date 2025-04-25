import pygame
from pygame import Vector2 as Vec2
import random
import math

BOID_RADIUS = 5
SIGHT_DISTANCE = 50
NUM_BOIDS = 10
BOID_COLOR = (0, 0, 200)
DRAG = 1
MAX_SPEED = 2
SIM_SIZE = (400, 300)
DRAW_RAYCAST = True

GRAVITY = 0.1
INERCIA = 1
RAYCAST_FORCE = 1
OTHERS_FORCE = 0
RANDOM_ROT = 0.001


def vec2_lerp(a, b, c):
    return Vec2(a.x * (1 - c) + b.x * c, a.y * (1 - c) + b.y * c)


class Boid:
    def __init__(self):
        self.pos = Vec2(random.uniform(0, SIM_SIZE[0]), random.uniform(0, SIM_SIZE[1]))
        angle = random.uniform(0, 2 * math.pi)
        self.vel = Vec2(math.cos(angle), math.sin(angle)) * MAX_SPEED
        self.last_raycast_hit = None  # store for debug draw

    def draw(self, screen):
        angle = self.vel.angle_to(Vec2(1, 0))
        points = [
            Vec2(BOID_RADIUS * 2, 0),
            Vec2(-BOID_RADIUS, BOID_RADIUS),
            Vec2(-BOID_RADIUS, -BOID_RADIUS),
        ]
        rotated = [p.rotate(-angle) + self.pos for p in points]
        pygame.draw.polygon(screen, BOID_COLOR, rotated)

        # draw raycast line
        if DRAW_RAYCAST:
            direction = self.vel.normalize()
            end_point = self.pos + direction * SIGHT_DISTANCE
            color = (255, 0, 0) if self.last_raycast_hit is not None else (0, 255, 0)
            pygame.draw.line(screen, color, self.pos, end_point, 1)

    def raycast(self, others, obstacles):
        direction = self.vel.normalize()
        end_point = self.pos + direction * SIGHT_DISTANCE
        ray = (self.pos, end_point)
        closest_distance = None

        # Check boids
        for other in others:
            if other == self:
                continue
            to_other = other.pos - self.pos
            proj = to_other.dot(direction)
            if 0 < proj < SIGHT_DISTANCE:
                perpendicular = to_other - direction * proj
                if perpendicular.length() < BOID_RADIUS * 2:
                    if closest_distance is None or proj < closest_distance:
                        closest_distance = proj

        # Check obstacles
        for start, end in obstacles:
            intersect = segment_intersection(ray[0], ray[1], start, end)
            if intersect:
                dist = (intersect - self.pos).length()
                if dist < SIGHT_DISTANCE and (
                    closest_distance is None or dist < closest_distance
                ):
                    closest_distance = dist

        # Check screen borders as obstacles
        screen_edges = [
            (Vec2(0, 0), Vec2(SIM_SIZE[0], 0)),  # Top
            (Vec2(0, SIM_SIZE[1]), Vec2(SIM_SIZE[0], SIM_SIZE[1])),  # Bottom
            (Vec2(0, 0), Vec2(0, SIM_SIZE[1])),  # Left
            (Vec2(SIM_SIZE[0], 0), Vec2(SIM_SIZE[0], SIM_SIZE[1])),  # Right
        ]

        for start, end in screen_edges:
            intersect = segment_intersection(ray[0], ray[1], start, end)
            if intersect:
                dist = (intersect - self.pos).length()
                if dist < SIGHT_DISTANCE and (
                    closest_distance is None or dist < closest_distance
                ):
                    closest_distance = dist

        self.last_raycast_hit = closest_distance
        return closest_distance

    def avoid_others(self, others):
        force = Vec2(0, 0)
        for other in others:
            diff = self.pos - other.pos
            dist = diff.length()
            if dist < 4 * BOID_RADIUS and dist > 0:
                force += diff.normalize() / dist
        return force

    def update(self, others, obstacles):
        hit_distance = self.raycast(others, obstacles)

        raycast_avoid_vel = Vec2(0, 0)
        if hit_distance is not None:
            t = 1 - hit_distance / SIGHT_DISTANCE
            angle = 360 * t  # rotate more the closer it is
            raycast_avoid_vel = self.vel.rotate(angle * random.uniform(-1, 1))

        boid_avoid_vel = self.avoid_others(others)

        self.vel = (
            self.vel * INERCIA
            + raycast_avoid_vel * RAYCAST_FORCE
            + boid_avoid_vel * OTHERS_FORCE
            + Vec2(random.uniform(-1, 1), random.uniform(-1, 1)) * RANDOM_ROT
            + Vec2(0, GRAVITY)
        )

        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)

        self.pos += self.vel

        self.pos.x = max(0, min(SIM_SIZE[0], self.pos.x))
        self.pos.y = max(0, min(SIM_SIZE[1], self.pos.y))


def segment_intersection(p1, p2, q1, q2):
    """Return the point of intersection between segments p1-p2 and q1-q2, or None."""

    def det(a, b):
        return a.x * b.y - a.y * b.x

    r = p2 - p1
    s = q2 - q1
    denominator = det(r, s)
    if denominator == 0:
        return None  # Parallel

    t = det(q1 - p1, s) / denominator
    u = det(q1 - p1, r) / denominator
    if 0 <= t <= 1 and 0 <= u <= 1:
        return p1 + t * r
    return None


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
    pygame.display.set_caption("Boids with Raycasting")
    clock = pygame.time.Clock()

    boids = [Boid() for _ in range(NUM_BOIDS)]
    obstacles = generate_obstacles()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            boids = [Boid() for _ in range(NUM_BOIDS)]
            obstacles = generate_obstacles()

        for boid in boids:
            boid.update(boids, obstacles)

        screen.fill((0, 0, 0))
        for boid in boids:
            boid.draw(screen)

        for start, end in obstacles:
            pygame.draw.line(screen, (255, 255, 255), start, end, 2)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
