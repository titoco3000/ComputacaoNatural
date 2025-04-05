import pygame
from pygame import Vector2


DEAD_COLOR = (0, 0, 0)
LIVE_COLOR = (0, 0, 255)
WHITE = (255, 255, 255)
SIDEBAR_COLOR = (200, 200, 200)

SIMULATION_SIZE = 100
HEADER_SIZE = 0.1
ZOOM_SPEED = 0.01
ZOOM_RATIO = 10


def getPixelLife(frame, x, y):
    w, h = frame.get_size()
    # try:
    #     print(x, y, frame.get_at((x, y)))
    # except:
    #     pass
    if x > 0 and x < w and y > 0 and y < h and frame.get_at((x, y)) == LIVE_COLOR:
        return 1
    return 0


def countNeighbours(frame, x, y):
    v = [
        getPixelLife(frame, i, j)
        for i in range(x - 1, x + 2)
        for j in range(y - 1, y + 2)
    ]
    # print(f"{x}, {y}: {v}")
    return sum(v)


def get_new_state(frame, coord):
    count = countNeighbours(frame, *coord)
    # coord == (4, 6) and print(f"count: {count}")
    if count < 3 or count > 4:
        return False
    elif count == 3:
        return True
    return frame.get_at(coord) == LIVE_COLOR


def load_pattern(pattern_name, frame):
    frame.fill(DEAD_COLOR)
    x, y = 0, 0
    with open(f"patterns/{pattern_name}.txt", "rb") as f:
        while 1:
            char = f.read(1)
            if not char:
                break
            if char == b"\n":
                y += 1
                x = -1
            elif char == b"X":
                if x < SIMULATION_SIZE and y < SIMULATION_SIZE:
                    print(x, y)
                    frame.set_at((x, y), LIVE_COLOR)
            x += 1


def main():
    pygame.init()

    screen_size = Vector2(1000, 700)

    screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)

    simulation_surface = pygame.Surface((SIMULATION_SIZE, SIMULATION_SIZE))
    auxiliary_surface = pygame.Surface((SIMULATION_SIZE, SIMULATION_SIZE))

    load_pattern("pulsar", simulation_surface)

    for y in range(SIMULATION_SIZE):
        print(
            [
                ("." if simulation_surface.get_at((x, y)) == DEAD_COLOR else "X")
                for x in range(SIMULATION_SIZE)
            ]
        )

    # for x in range(SIMULATION_SIZE):
    #     for y in range(SIMULATION_SIZE):
    #         color = LIVE_COLOR if (x + y) % 2 == 0 else DEAD_COLOR  # Checker pattern
    #         simulation_surface.set_at((x, y), color)

    zoom = 0.1
    view_position = Vector2(0, 0)
    drag_start = None

    celula_atual = 0
    sync = True

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen_size = Vector2(event.dict["size"])
            elif event.type == pygame.MOUSEWHEEL:
                mouse_pos = Vector2(
                    pygame.mouse.get_pos()
                )  # Get mouse position in screen space
                zoom_factor = event.y * ZOOM_SPEED
                new_zoom = max(0, min(1, zoom + zoom_factor))

                if new_zoom != zoom:  # Only adjust if zoom changes
                    # Convert mouse position to surface space before zooming
                    rel_mouse_pos = (mouse_pos - view_position) / (
                        arena_size * (1 + zoom * ZOOM_RATIO)
                    )

                    # Apply zoom
                    zoom = new_zoom

                    # Compute new view position to keep mouse in place
                    new_surface_size = arena_size * (1 + zoom * ZOOM_RATIO)
                    view_position = mouse_pos - rel_mouse_pos * new_surface_size
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drag_start = Vector2(event.pos)
                elif event.button == 3:
                    pass

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drag_start = None

        if sync:
            for i in range(SIMULATION_SIZE):
                for j in range(SIMULATION_SIZE):
                    coord_celula = (i, j)
                    auxiliary_surface.set_at(
                        coord_celula,
                        (
                            LIVE_COLOR
                            if get_new_state(simulation_surface, coord_celula)
                            else DEAD_COLOR
                        ),
                    )

            auxiliary_surface, simulation_surface = (
                simulation_surface,
                auxiliary_surface,
            )

        else:
            # atualiza uma celula
            coord_celula = (
                celula_atual % SIMULATION_SIZE,
                celula_atual // SIMULATION_SIZE,
            )
            simulation_surface.set_at(
                coord_celula,
                (
                    LIVE_COLOR
                    if get_new_state(simulation_surface, coord_celula)
                    else DEAD_COLOR
                ),
            )
            celula_atual = (celula_atual + 1) % (SIMULATION_SIZE**2)

        max_dimension = min(screen_size.x, screen_size.y)

        sidebar_width = max(300, max_dimension * 0.2)

        arena_size = min(screen_size.x - sidebar_width, screen_size.y)

        scaled_surface = pygame.transform.scale(
            simulation_surface,
            (
                arena_size * (1 + zoom * ZOOM_RATIO),
                arena_size * (1 + zoom * ZOOM_RATIO),
            ),
        )

        if drag_start is not None:
            p = Vector2(pygame.mouse.get_pos())
            view_position -= drag_start - p
            drag_start = p

        view_position.y = max(
            screen_size.y - arena_size * (1 + zoom * ZOOM_RATIO),
            min(0, view_position.y),
        )
        view_position.x = max(
            screen_size.x - arena_size * (1 + zoom * ZOOM_RATIO),
            min(sidebar_width, view_position.x),
        )

        screen.fill(WHITE)

        screen.blit(scaled_surface, view_position)

        pygame.draw.rect(
            screen,
            SIDEBAR_COLOR,
            (0, 0, sidebar_width, screen_size.y),
        )
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

"""
3 3 (0, 0, 0, 255)
3 4 (0, 0, 0, 255)
3 5 (0, 0, 0, 255)
4 3 (0, 0, 0, 255)
4 4 (0, 0, 255, 255)
4 5 (0, 0, 0, 255)
5 3 (0, 0, 0, 255)
5 4 (0, 0, 255, 255)
5 5 (0, 0, 255, 255)
4, 4: [0, 0, 0, 0, 1, 0, 0, 1, 1]
"""
