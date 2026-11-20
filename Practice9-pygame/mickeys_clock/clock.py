import pygame
import math
from datetime import datetime


def create_hand(length, width, color):
    size = (length + 30) * 2
    hand = pygame.Surface((size, size), pygame.SRCALPHA)

    center = size // 2
    end_x = center + length

    """Draw Mickey's arm:
    pygame.draw.line(
    surface,
    color,
    starting_position,
    ending_position,
    width
  )"""
    pygame.draw.line(
        hand,
        color,
        (center, center),
        (end_x, center),
        width
    )

    # Draw Mickey's white glove
    pygame.draw.circle(
        hand,
        (255, 255, 255),
        (end_x, center),
        20
    )

    # Draw glove border
    pygame.draw.circle(
        hand,
        (0, 0, 0),
        (end_x, center),
        20,
        3
    )

    # Draw three simple glove fingers
    pygame.draw.line(
        hand,
        (0, 0, 0),
        (end_x - 5, center - 12),
        (end_x + 5, center - 17),
        2
    )

    pygame.draw.line(
        hand,
        (0, 0, 0),
        (end_x, center - 10),
        (end_x + 12, center - 10),
        2
    )

    return hand


def draw_clock(screen):
    center_x = 350
    center_y = 370
    radius = 250

    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (210, 40, 40)
    yellow = (255, 220, 90)

    current_time = datetime.now()

    minute = current_time.minute
    second = current_time.second

    # Draw Mickey's ears
    pygame.draw.circle(screen, black, (170, 145), 105)
    pygame.draw.circle(screen, black, (530, 145), 105)

    # Draw the outer clock
    pygame.draw.circle(
        screen,
        black,
        (center_x, center_y),
        radius
    )

    # Draw the inner clock face
    pygame.draw.circle(
        screen,
        yellow,
        (center_x, center_y),
        radius - 12
    )

    # Draw 60 clock marks
    for i in range(60):
        angle = math.radians(i * 6 - 90)

        if i % 5 == 0:
            mark_length = 18
            mark_width = 5
        else:
            mark_length = 10
            mark_width = 2

        outer_x = center_x + math.cos(angle) * (radius - 25)
        outer_y = center_y + math.sin(angle) * (radius - 25)

        inner_x = center_x + math.cos(angle) * (
            radius - 25 - mark_length
        )
        inner_y = center_y + math.sin(angle) * (
            radius - 25 - mark_length
        )

        pygame.draw.line(
            screen,
            black,
            (int(inner_x), int(inner_y)),
            (int(outer_x), int(outer_y)),
            mark_width
        )

    # Draw clock numbers
    number_font = pygame.font.Font(None, 38)

    for number in range(1, 13):
        angle = math.radians(number * 30 - 90)

        number_x = center_x + math.cos(angle) * 185
        number_y = center_y + math.sin(angle) * 185

        number_text = number_font.render(
            str(number),
            True,
            black
        )

        number_rect = number_text.get_rect(
            center=(int(number_x), int(number_y))
        )

        screen.blit(number_text, number_rect)

    # Create Mickey's right hand for minutes
    right_hand = create_hand(135, 14, black)

    # Include seconds so the minute hand moves gradually
    minute_value = minute + second / 60
    minute_rotation = 90 - minute_value * 6

    rotated_right_hand = pygame.transform.rotate(
        right_hand,
        minute_rotation
    )

    right_hand_rect = rotated_right_hand.get_rect(
        center=(center_x, center_y)
    )

    screen.blit(rotated_right_hand, right_hand_rect)

    # Create Mickey's left hand for seconds
    left_hand = create_hand(175, 9, red)

    second_rotation = 90 - second * 6

    rotated_left_hand = pygame.transform.rotate(
        left_hand,
        second_rotation
    )

    left_hand_rect = rotated_left_hand.get_rect(
        center=(center_x, center_y)
    )

    screen.blit(rotated_left_hand, left_hand_rect)

    # Draw the center point over both hands
    pygame.draw.circle(
        screen,
        black,
        (center_x, center_y),
        15
    )

    pygame.draw.circle(
        screen,
        red,
        (center_x, center_y),
        7
    )

    # Display minutes and seconds
    time_font = pygame.font.Font(None, 42)

    time_text = time_font.render(
        current_time.strftime("%M:%S"),
        True,
        black
    )

    time_rect = time_text.get_rect(
    center=(center_x, 660)
    )

    screen.blit(time_text, time_rect)

    