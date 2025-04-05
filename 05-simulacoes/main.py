import pygame
from pygame import Vector2


DEAD_COLOR = (0, 0, 0)
LIVE_COLOR = (0, 0, 255)
WHITE = (255, 255, 255)
SIDEBAR_COLOR = (200, 200, 200)

SIMULATION_SIZE = 120
HEADER_SIZE = 0.1
ZOOM_SPEED = 0.01
ZOOM_RATIO = 10

# prefab name, pattern
PREFABS = [
    ("beacon - 3", "beacon"),
    ("glider", "glider"),
    ("glider-gun", "glider-gun"),
    ("pulsar", "pulsar"),
    ("toad", "toad"),
    ("spaceship", "spaceship"),
]


def getPixelLife(frame, x, y):
    w, h = frame.get_size()
    if x > 0 and x < w and y > 0 and y < h and frame.get_at((x, y)) == LIVE_COLOR:
        return 1
    return 0


def countNeighbours(frame, x, y):
    v = [
        getPixelLife(frame, i, j)
        for i in range(x - 1, x + 2)
        for j in range(y - 1, y + 2)
    ]
    return sum(v)


def get_new_state(frame, coord):
    count = countNeighbours(frame, *coord)
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
                    frame.set_at((x, y), LIVE_COLOR)
            x += 1


def main():
    pygame.init()

    screen_size = Vector2(1000, 700)

    screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)

    simulation_surface = pygame.Surface((SIMULATION_SIZE, SIMULATION_SIZE))
    auxiliary_surface = pygame.Surface((SIMULATION_SIZE, SIMULATION_SIZE))

    load_pattern("glider-gun", simulation_surface)

    zoom = 0.1
    view_position = Vector2(0, 0)
    drag_start = None

    sync = False

    header_font = pygame.font.SysFont("Futura", 30)

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

                    for rect, pattern in prefab_buttons:
                        if rect.collidepoint(event.pos):
                            load_pattern(pattern, simulation_surface)
                            break

                elif event.button == 3:
                    pass

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drag_start = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    sync = not sync

        if sync:
            for i in range(SIMULATION_SIZE):
                for j in range(SIMULATION_SIZE):
                    coord_celula = (i, j)
                    simulation_surface.set_at(
                        coord_celula,
                        (
                            LIVE_COLOR
                            if get_new_state(simulation_surface, coord_celula)
                            else DEAD_COLOR
                        ),
                    )
        else:
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

        header_font_size = int(sidebar_width // 10)
        header_font = pygame.font.SysFont("Futura", header_font_size)
        screen.blit(
            header_font.render(
                "Game of Life " + ("sync" if sync else ""), True, (0, 0, 0)
            ),
            (sidebar_width // 30, sidebar_width // 30),
        )

        # Create and draw prefab buttons
        button_height = int(sidebar_width // 8)
        button_font = pygame.font.SysFont("Futura", int(button_height * 0.5))
        button_y = sidebar_width // 15 + button_height  # Leave space after header

        prefab_buttons = []
        for name, pattern in PREFABS:
            rect = pygame.Rect(10, button_y, sidebar_width - 20, button_height)
            pygame.draw.rect(screen, (180, 180, 180), rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)  # border

            text_surf = button_font.render(name, True, (0, 0, 0))
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

            prefab_buttons.append((rect, pattern))
            button_y += button_height + 10

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
