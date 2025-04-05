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


def main():
    pygame.init()

    screen_size = Vector2(1000, 700)
    print(screen_size)

    screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)

    simulation_surface = pygame.Surface(
        (SIMULATION_SIZE, SIMULATION_SIZE), pygame.RESIZABLE
    )
    for x in range(SIMULATION_SIZE):
        for y in range(SIMULATION_SIZE):
            color = LIVE_COLOR if (x + y) % 2 == 0 else DEAD_COLOR  # Checker pattern
            simulation_surface.set_at((x, y), color)

    zoom = 0.1
    view_position = Vector2(0, 0)
    drag_start = None

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
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drag_start = None

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

        screen.fill(DEAD_COLOR)

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
