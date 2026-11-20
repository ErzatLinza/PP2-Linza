import pygame
from pathlib import Path
from player import MusicPlayer

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((700, 450))
pygame.display.set_caption("Pygame Music Player")

font = pygame.font.Font(None, 38)
small_font = pygame.font.Font(None, 28)

music_folder = Path(__file__).parent / "music"
player = MusicPlayer(music_folder)

done = False
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()

            if event.key == pygame.K_s:
                player.stop()

            if event.key == pygame.K_n:
                player.next_track()

            if event.key == pygame.K_b:
                player.previous_track()

            if event.key == pygame.K_q:
                done = True

    player.check_finished()

    screen.fill((30, 30, 40))

    title = font.render(
        "Pygame Music Player",
        True,
        (255, 255, 255)
    )
    title_rect = title.get_rect(center=(350, 60))
    screen.blit(title, title_rect)

    track_text = small_font.render(
        "Track: " + player.current_track(),
        True,
        (255, 220, 100)
    )
    track_rect = track_text.get_rect(center=(350, 140))
    screen.blit(track_text, track_rect)

    position_text = small_font.render(
        "Position: " + str(player.position()) + " seconds",
        True,
        (200, 200, 200)
    )
    position_rect = position_text.get_rect(center=(350, 190))
    screen.blit(position_text, position_rect)

    controls = [
        "P = Play",
        "S = Stop",
        "N = Next track",
        "B = Previous track",
        "Q = Quit"
    ]

    y = 250

    for control in controls:
        text = small_font.render(
            control,
            True,
            (230, 230, 230)
        )

        text_rect = text.get_rect(center=(350, y))
        screen.blit(text, text_rect)

        y += 32

    pygame.display.flip()
    clock.tick(60)

pygame.mixer.music.stop()
pygame.quit()