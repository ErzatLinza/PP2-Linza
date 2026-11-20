import pygame
from clock import draw_clock

pygame.init()

screen = pygame.display.set_mode((800, 850))
pygame.display.set_caption("Mickey's Clock")

done = False
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill((240, 240, 240))

    draw_clock(screen)

    pygame.display.flip()

    # Update once every second
    clock.tick(1)

pygame.quit()