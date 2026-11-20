import pygame
from pathlib import Path


class MusicPlayer:
    def __init__(self, music_folder):
        self.music_folder = Path(music_folder)

        # Find all supported audio files
        self.playlist = []

        for file in self.music_folder.iterdir():
            if file.suffix.lower() in (".mp3", ".wav", ".ogg"):
                self.playlist.append(file)

        # Sort songs alphabetically
        self.playlist.sort()

        self.current_index = 0
        self.playing = False
        self.start_time = 0

    def has_music(self):
        return len(self.playlist) > 0

    def current_track(self):
        if not self.has_music():
            return "No music files found"

        return self.playlist[self.current_index].name

    def play(self):
        if not self.has_music():
            return

        track = self.playlist[self.current_index]

        pygame.mixer.music.load(str(track))
        pygame.mixer.music.play()

        self.playing = True
        self.start_time = pygame.time.get_ticks()

    def stop(self):
        pygame.mixer.music.stop()
        self.playing = False

    def next_track(self):
        if not self.has_music():
            return

        self.current_index += 1

        if self.current_index >= len(self.playlist):
            self.current_index = 0

        self.play()

    def previous_track(self):
        if not self.has_music():
            return

        self.current_index -= 1

        if self.current_index < 0:
            self.current_index = len(self.playlist) - 1

        self.play()

    def position(self):
        if not self.playing:
            return 0

        position_ms = pygame.mixer.music.get_pos()

        if position_ms < 0:
            return 0

        return position_ms // 1000

    def check_finished(self):
        if self.playing and not pygame.mixer.music.get_busy():
            self.next_track()