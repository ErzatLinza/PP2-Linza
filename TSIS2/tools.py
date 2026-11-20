import pygame
import math


WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
TOOLBAR_HEIGHT = 100

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (80, 80, 80)
BLUE = (60, 120, 220)


def draw_button(screen, rectangle, text, font, active=False):
    if active:
        color = BLUE
        text_color = WHITE
    else:
        color = LIGHT_GRAY
        text_color = BLACK

    pygame.draw.rect(screen, color, rectangle)
    pygame.draw.rect(screen, DARK_GRAY, rectangle, 2)

    text_surface = font.render(text, True, text_color)
    text_rectangle = text_surface.get_rect(
        center=rectangle.center
    )

    screen.blit(text_surface, text_rectangle)


def draw_shape(
    surface,
    tool,
    start_position,
    end_position,
    color,
    brush_size
):
    start_x, start_y = start_position
    end_x, end_y = end_position

    if tool == "line":
        pygame.draw.line(
            surface,
            color,
            start_position,
            end_position,
            brush_size
        )

    elif tool == "rectangle":
        left = min(start_x, end_x)
        top = min(start_y, end_y)
        width = abs(end_x - start_x)
        height = abs(end_y - start_y)

        rectangle = pygame.Rect(
            left,
            top,
            width,
            height
        )

        pygame.draw.rect(
            surface,
            color,
            rectangle,
            brush_size
        )

    elif tool == "circle":
        distance_x = end_x - start_x
        distance_y = end_y - start_y

        radius = int(
            math.sqrt(
                distance_x ** 2 + distance_y ** 2
            )
        )

        if radius > 0:
            pygame.draw.circle(
                surface,
                color,
                start_position,
                radius,
                brush_size
            )

    elif tool == "square":
        distance_x = end_x - start_x
        distance_y = end_y - start_y

        side = max(
            abs(distance_x),
            abs(distance_y)
        )

        if distance_x < 0:
            left = start_x - side
        else:
            left = start_x

        if distance_y < 0:
            top = start_y - side
        else:
            top = start_y

        square = pygame.Rect(
            left,
            top,
            side,
            side
        )

        pygame.draw.rect(
            surface,
            color,
            square,
            brush_size
        )

    elif tool == "right_triangle":
        points = [
            start_position,
            (start_x, end_y),
            end_position
        ]

        pygame.draw.polygon(
            surface,
            color,
            points,
            brush_size
        )

    elif tool == "equilateral_triangle":
        base_width = end_x - start_x
        height = abs(base_width) * math.sqrt(3) / 2
        middle_x = (start_x + end_x) // 2

        if end_y < start_y:
            top_y = start_y - height
        else:
            top_y = start_y + height

        points = [
            start_position,
            (end_x, start_y),
            (middle_x, int(top_y))
        ]

        pygame.draw.polygon(
            surface,
            color,
            points,
            brush_size
        )

    elif tool == "rhombus":
        left = min(start_x, end_x)
        right = max(start_x, end_x)
        top = min(start_y, end_y)
        bottom = max(start_y, end_y)

        middle_x = (left + right) // 2
        middle_y = (top + bottom) // 2

        points = [
            (middle_x, top),
            (right, middle_y),
            (middle_x, bottom),
            (left, middle_y)
        ]

        pygame.draw.polygon(
            surface,
            color,
            points,
            brush_size
        )


def flood_fill(surface, start_position, new_color):
    width = surface.get_width()
    height = surface.get_height()

    start_x, start_y = start_position

    if not (
        0 <= start_x < width
        and 0 <= start_y < height
    ):
        return

    old_color = surface.get_at(start_position)
    new_color = pygame.Color(new_color)

    if old_color == new_color:
        return

    pixels_to_check = [start_position]

    while pixels_to_check:
        x, y = pixels_to_check.pop()

        if not (
            0 <= x < width
            and 0 <= y < height
        ):
            continue

        if surface.get_at((x, y)) != old_color:
            continue

        surface.set_at((x, y), new_color)

        pixels_to_check.append((x + 1, y))
        pixels_to_check.append((x - 1, y))
        pixels_to_check.append((x, y + 1))
        pixels_to_check.append((x, y - 1))