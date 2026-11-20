import pygame
from datetime import datetime
from pathlib import Path

from tools import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    TOOLBAR_HEIGHT,
    WHITE,
    BLACK,
    LIGHT_GRAY,
    DARK_GRAY,
    draw_button,
    draw_shape,
    flood_fill
)


pygame.init()

screen = pygame.display.set_mode(
    (WINDOW_WIDTH, WINDOW_HEIGHT)
)

pygame.display.set_caption("TSIS 2 Paint Application")

canvas_width = WINDOW_WIDTH
canvas_height = WINDOW_HEIGHT - TOOLBAR_HEIGHT

canvas = pygame.Surface(
    (canvas_width, canvas_height)
)

canvas.fill(WHITE)

font = pygame.font.Font(None, 20)
text_font = pygame.font.SysFont("Arial", 30)

# Drawing-tool buttons
pencil_button = pygame.Rect(10, 8, 75, 35)
line_button = pygame.Rect(90, 8, 65, 35)
rectangle_button = pygame.Rect(160, 8, 95, 35)
circle_button = pygame.Rect(260, 8, 70, 35)
square_button = pygame.Rect(335, 8, 75, 35)
right_triangle_button = pygame.Rect(415, 8, 100, 35)
equilateral_button = pygame.Rect(520, 8, 100, 35)
rhombus_button = pygame.Rect(625, 8, 85, 35)
eraser_button = pygame.Rect(715, 8, 75, 35)
fill_button = pygame.Rect(795, 8, 65, 35)
text_button = pygame.Rect(865, 8, 65, 35)
clear_button = pygame.Rect(935, 8, 70, 35)

# Brush-size buttons
small_button = pygame.Rect(10, 55, 80, 35)
medium_button = pygame.Rect(95, 55, 90, 35)
large_button = pygame.Rect(190, 55, 80, 35)

# Color-picker buttons
color_buttons = [
    (pygame.Rect(310, 55, 35, 35), BLACK),
    (pygame.Rect(350, 55, 35, 35), (255, 0, 0)),
    (pygame.Rect(390, 55, 35, 35), (0, 180, 0)),
    (pygame.Rect(430, 55, 35, 35), (0, 100, 255)),
    (pygame.Rect(470, 55, 35, 35), (255, 220, 0)),
    (pygame.Rect(510, 55, 35, 35), (160, 50, 200)),
    (pygame.Rect(550, 55, 35, 35), (255, 120, 0)),
    (pygame.Rect(590, 55, 35, 35), (255, 100, 180))
]

tool_buttons = [
    (pencil_button, "pencil"),
    (line_button, "line"),
    (rectangle_button, "rectangle"),
    (circle_button, "circle"),
    (square_button, "square"),
    (right_triangle_button, "right_triangle"),
    (equilateral_button, "equilateral_triangle"),
    (rhombus_button, "rhombus"),
    (eraser_button, "eraser"),
    (fill_button, "fill"),
    (text_button, "text")
]

tool_labels = {
    "pencil": "Pencil",
    "line": "Line",
    "rectangle": "Rectangle",
    "circle": "Circle",
    "square": "Square",
    "right_triangle": "Right Tri.",
    "equilateral_triangle": "Equil. Tri.",
    "rhombus": "Rhombus",
    "eraser": "Eraser",
    "fill": "Fill",
    "text": "Text"
}

shape_tools = (
    "line",
    "rectangle",
    "circle",
    "square",
    "right_triangle",
    "equilateral_triangle",
    "rhombus"
)

current_tool = "pencil"
current_color = BLACK
brush_size = 2

drawing = False
start_position = None
previous_position = None

text_active = False
text_position = None
text_input = ""

status_message = "Ctrl+S: Save canvas"

done = False
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            # Save using Ctrl+S
            if (
                event.key == pygame.K_s
                and event.mod & pygame.KMOD_CTRL
            ):
                timestamp = datetime.now().strftime(
                    "%Y%m%d_%H%M%S"
                )

                filename = (
                    Path(__file__).parent
                    / f"painting_{timestamp}.png"
                )

                pygame.image.save(
                    canvas,
                    str(filename)
                )

                status_message = (
                    "Saved: " + filename.name
                )

            # Text input
            elif text_active:
                if event.key == pygame.K_RETURN:
                    if text_input:
                        permanent_text = text_font.render(
                            text_input,
                            True,
                            current_color
                        )

                        canvas.blit(
                            permanent_text,
                            text_position
                        )

                    text_active = False
                    text_position = None
                    text_input = ""
                    status_message = "Text added"

                elif event.key == pygame.K_ESCAPE:
                    text_active = False
                    text_position = None
                    text_input = ""
                    status_message = "Text cancelled"

                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]

                elif event.unicode.isprintable():
                    text_input += event.unicode

            # Brush-size keyboard shortcuts
            else:
                if event.key == pygame.K_1:
                    brush_size = 2

                if event.key == pygame.K_2:
                    brush_size = 5

                if event.key == pygame.K_3:
                    brush_size = 10

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                button_clicked = False

                # Select drawing tool
                for button, tool_name in tool_buttons:
                    if button.collidepoint(event.pos):
                        current_tool = tool_name
                        text_active = False
                        text_input = ""
                        button_clicked = True

                # Clear canvas
                if clear_button.collidepoint(event.pos):
                    canvas.fill(WHITE)
                    text_active = False
                    text_input = ""
                    status_message = "Canvas cleared"
                    button_clicked = True

                # Select brush size
                if small_button.collidepoint(event.pos):
                    brush_size = 2
                    button_clicked = True

                elif medium_button.collidepoint(event.pos):
                    brush_size = 5
                    button_clicked = True

                elif large_button.collidepoint(event.pos):
                    brush_size = 10
                    button_clicked = True

                # Select color
                for button, color in color_buttons:
                    if button.collidepoint(event.pos):
                        current_color = color
                        button_clicked = True

                # Click inside the canvas
                if (
                    not button_clicked
                    and event.pos[1] >= TOOLBAR_HEIGHT
                ):
                    canvas_position = (
                        event.pos[0],
                        event.pos[1] - TOOLBAR_HEIGHT
                    )

                    # Flood-fill tool
                    if current_tool == "fill":
                        flood_fill(
                            canvas,
                            canvas_position,
                            current_color
                        )

                        status_message = "Area filled"

                    # Text-placement tool
                    elif current_tool == "text":
                        text_active = True
                        text_position = canvas_position
                        text_input = ""
                        status_message = (
                            "Type text: Enter confirms, "
                            "Escape cancels"
                        )

                    # Start pencil, eraser or shape
                    else:
                        drawing = True
                        start_position = canvas_position
                        previous_position = canvas_position

                        if current_tool == "pencil":
                            pygame.draw.circle(
                                canvas,
                                current_color,
                                canvas_position,
                                max(1, brush_size // 2)
                            )

                        elif current_tool == "eraser":
                            pygame.draw.circle(
                                canvas,
                                WHITE,
                                canvas_position,
                                max(1, brush_size // 2)
                            )

        if event.type == pygame.MOUSEMOTION:
            if (
                drawing
                and event.pos[1] >= TOOLBAR_HEIGHT
            ):
                current_position = (
                    event.pos[0],
                    event.pos[1] - TOOLBAR_HEIGHT
                )

                if current_tool == "pencil":
                    pygame.draw.line(
                        canvas,
                        current_color,
                        previous_position,
                        current_position,
                        brush_size
                    )

                    previous_position = current_position

                elif current_tool == "eraser":
                    pygame.draw.line(
                        canvas,
                        WHITE,
                        previous_position,
                        current_position,
                        brush_size
                    )

                    previous_position = current_position

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                if event.pos[1] >= TOOLBAR_HEIGHT:
                    end_position = (
                        event.pos[0],
                        event.pos[1] - TOOLBAR_HEIGHT
                    )

                    if current_tool in shape_tools:
                        draw_shape(
                            canvas,
                            current_tool,
                            start_position,
                            end_position,
                            current_color,
                            brush_size
                        )

                drawing = False
                start_position = None
                previous_position = None

    # Draw toolbar and canvas
    screen.fill(LIGHT_GRAY)
    screen.blit(canvas, (0, TOOLBAR_HEIGHT))

    # Live preview for shapes
    if drawing and current_tool in shape_tools:
        mouse_position = pygame.mouse.get_pos()

        if mouse_position[1] >= TOOLBAR_HEIGHT:
            screen_start = (
                start_position[0],
                start_position[1] + TOOLBAR_HEIGHT
            )

            draw_shape(
                screen,
                current_tool,
                screen_start,
                mouse_position,
                current_color,
                brush_size
            )

    # Live text preview
    if text_active and text_position is not None:
        preview_text = text_font.render(
            text_input + "|",
            True,
            current_color
        )

        screen.blit(
            preview_text,
            (
                text_position[0],
                text_position[1] + TOOLBAR_HEIGHT
            )
        )

    # Draw tool buttons
    for button, tool_name in tool_buttons:
        draw_button(
            screen,
            button,
            tool_labels[tool_name],
            font,
            current_tool == tool_name
        )

    draw_button(
        screen,
        clear_button,
        "Clear",
        font,
        False
    )

    # Draw brush-size buttons
    draw_button(
        screen,
        small_button,
        "Small (1)",
        font,
        brush_size == 2
    )

    draw_button(
        screen,
        medium_button,
        "Medium (2)",
        font,
        brush_size == 5
    )

    draw_button(
        screen,
        large_button,
        "Large (3)",
        font,
        brush_size == 10
    )

    # Draw color buttons
    for button, color in color_buttons:
        pygame.draw.rect(screen, color, button)

        if color == current_color:
            border_color = WHITE
            border_width = 4
        else:
            border_color = DARK_GRAY
            border_width = 2

        pygame.draw.rect(
            screen,
            border_color,
            button,
            border_width
        )

    # Status message
    status_surface = font.render(
        status_message,
        True,
        BLACK
    )

    screen.blit(status_surface, (650, 64))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()