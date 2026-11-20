import pygame
from ball import Ball

pygame.init()

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode(
    (screen_width, screen_height)
)

pygame.display.set_caption("Moving Ball")

# Create the ball in the center of the screen
ball = Ball(
    screen_width // 2,
    screen_height // 2
)

done = False
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                ball.move_up()

            if event.key == pygame.K_DOWN:
                ball.move_down(screen_height)

            if event.key == pygame.K_LEFT:
                ball.move_left()

            if event.key == pygame.K_RIGHT:
                ball.move_right(screen_width)

    # Clear the previous frame with white
    screen.fill((255, 255, 255))

    # Draw the ball at its current position
    ball.draw(screen)

    # Display the completed frame
    pygame.display.flip()

    # Limit the application to 60 frames per second
    clock.tick(60)

pygame.quit()