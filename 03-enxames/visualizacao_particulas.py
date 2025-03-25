import pygame
import numpy as np
from itertools import chain
from itertools import cycle
import math
import random
from time import time

WIDTH, HEIGHT = 1000, 800
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

ANGULO = 45
escala = 0.7, 0.3
translacao = 0, 0.2


def lerp(a, b, x):
    try:
        return [lerp(a, b, x) for a, b in zip(a, b)]
    except:
        return a * (1 - x) + b * x


def rotate_points(points, angle_degrees=45):
    """Rotate points around the center (0.5, 0.5) by a given angle."""
    angle = np.radians(angle_degrees)
    cos_a, sin_a = np.cos(angle), np.sin(angle)
    rotation_matrix = np.array([[cos_a, -sin_a], [sin_a, cos_a]])
    center = np.array([0.5, 0.5])
    return [center + rotation_matrix @ (np.array(p) - center) for p in points]


def scale_points(points, scale):
    return [
        ((point[0] - 0.5) * scale[0] + 0.5, (point[1] - 0.5) * scale[1] + 0.5)
        for point in points
    ]


def translate_points(points, translation):
    return [(point[0] + translation[0], point[1] + translation[1]) for point in points]


def polys_individuo_wireframe(pos, val, w=0.05):
    pos = lerp(0, 1 - w, pos[0]), lerp(0, 1 - w, pos[1])
    return [
        [
            (pos[0] - val, pos[1] - val),
            (pos[0] - val + w, pos[1] - val),
            (pos[0] - val + w, pos[1] + w - val),
            (pos[0] - val, pos[1] + w - val),
        ],
        [
            (pos[0], pos[1]),
            (pos[0] + w, pos[1]),
            (pos[0] + w, pos[1] + w),
            (pos[0], pos[1] + w),
        ],
        [
            (pos[0] - val, pos[1] - val),
            (pos[0] + w - val, pos[1] - val),
            (pos[0] + w, pos[1]),
            (pos[0] + w, pos[1] + w),
        ],
        [
            (pos[0] - val, pos[1] - val),
            (pos[0] - val, pos[1] - val + w),
            (pos[0], pos[1] + w),
            (pos[0] + w, pos[1] + w),
        ],
    ]


def polys_individuo(pos, val, w=0.05):
    pos = lerp(0, 1 - w, pos[0]), lerp(0, 1 - w, pos[1])
    return [
        [
            (pos[0] - val, pos[1] - val),
            (pos[0] - val + w, pos[1] - val),
            (pos[0] - val + w, pos[1] + w - val),
            (pos[0] - val, pos[1] + w - val),
        ],
        [
            (pos[0] - val + w, pos[1] - val + w),
            (pos[0] + w - val, pos[1] - val),
            (pos[0] + w, pos[1]),
            (pos[0] + w, pos[1] + w),
        ],
        [
            (pos[0] - val + w, pos[1] - val + w),
            (pos[0] - val, pos[1] - val + w),
            (pos[0], pos[1] + w),
            (pos[0] + w, pos[1] + w),
        ],
    ]


# Scale points to fit the screen
def scale_to_screen(points):
    return [(int(x * WIDTH), int(y * HEIGHT)) for x, y in points]


def transform_points(*lists, angulo, escala, translacao):
    lengths = [len(lst) for lst in lists]
    combined = list(chain.from_iterable(lists))  # Flatten all lists into one
    rotated = rotate_points(combined, angulo)
    perspective = scale_points(rotated, escala)
    translated = translate_points(perspective, translacao)
    scaled = scale_to_screen(translated)

    result = []
    start = 0
    for length in lengths:
        result.append(scaled[start : start + length])
        start += length

    return result


def colorir_faces(faces, inidividuos):
    multipliers = cycle([0, 0.1, 0.2])
    for i in range(len(faces)):
        faces[i] = (
            lerp(inidividuos[math.floor(i / 3)].cor, BLACK, next(multipliers)),
            faces[i],
        )


def random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


class VisualizacaoParticulas:
    def __init__(self, n, intervalo=0):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Particulas")

        self.base = [(0, 0), (1, 0), (1, 1), (0, 1)]
        self.base = transform_points(
            self.base, angulo=ANGULO, escala=escala, translacao=translacao
        )[0]

        self.individuos = [Particula() for _ in range(n)]

        self.intervalo = intervalo
        self.last_step = time()

    def loop(self, step_fn=None):
        running = True
        while running:
            runtime = time()
            if step_fn is not None and runtime - self.last_step > self.intervalo:
                self.last_step = runtime
                step_fn(self.individuos)

            self.screen.fill(BLACK)
            self.individuos.sort(
                key=lambda i: ((i.pos[0] - 0) ** 2 + (i.pos[1] - 0) ** 2)
            )

            flat_poly_list = [
                x
                for xs in [polys_individuo(i.pos, i.val / 150) for i in self.individuos]
                for x in xs
            ]
            faces = transform_points(
                *flat_poly_list, angulo=ANGULO, escala=escala, translacao=translacao
            )
            colorir_faces(faces, self.individuos)

            pygame.draw.polygon(self.screen, (255, 0, 0), self.base, True)

            for face in faces:
                pygame.draw.polygon(self.screen, *face)

            pygame.display.flip()  # Update screen

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()


class Particula:
    def __init__(self):
        self.pos = random.random(), random.random()
        self.melhor_pos = self.pos
        self.vel = random.random(), random.random()
        self.val = 0.1
        self.cor = random_color()
