import pygame
import numpy as np
import random
import math

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("3D Points Projection with Camera Rotation")
clock = pygame.time.Clock()

# Parameters
WIDTH, HEIGHT = screen.get_size()
FOV = 90  # degrees
NEAR = 0.1
FAR = 100.0
ASPECT_RATIO = WIDTH / HEIGHT


# Perspective projection matrix
def perspective(fov, aspect, near, far):
    f = 1.0 / math.tan(math.radians(fov) / 2)
    proj = np.array(
        [
            [f / aspect, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, (far + near) / (near - far), (2 * far * near) / (near - far)],
            [0, 0, -1, 0],
        ]
    )
    return proj


# View matrix: rotate camera around the origin
def view_matrix(angle_degrees):
    angle = math.radians(angle_degrees)
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return np.array(
        [
            [cos_a, 0, -sin_a, 0],
            [0, 1, 0, 0],
            [sin_a, 0, cos_a, -2.2],  # move back 5 units from origin
            [0, 0, 0, 1],
        ]
    )


# Simple model matrix
def model_matrix():
    return np.identity(4)


def project(point, mvp):
    transformed = mvp @ point
    if transformed[3] != 0:
        transformed /= transformed[3]
    x = int((transformed[0] + 1) * 0.5 * WIDTH)
    y = int((1 - transformed[1]) * 0.5 * HEIGHT)
    return (x, y)


def run(boids, update_fn, reset_fn):
    # Projection matrix (fixed)
    P = perspective(FOV, ASPECT_RATIO, NEAR, FAR)

    # Camera rotation state
    camera_angle = 0

    running = True
    while running:
        screen.fill((0, 0, 0))  # Clear screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Key press check
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            camera_angle -= 1
        if keys[pygame.K_RIGHT]:
            camera_angle += 1
        if keys[pygame.K_r]:
            reset_fn(boids)

        update_fn(boids)

        # Update matrices
        V = view_matrix(camera_angle)
        M = model_matrix()
        MVP = P @ V @ M

        # Draw all points
        for boid in boids:
            x, y = project(boid.pos, MVP)
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                pygame.draw.circle(screen, (0, 0, 255), (x, y), 3)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
