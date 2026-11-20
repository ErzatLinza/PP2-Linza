import pygame


class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.radius = 25
        self.step = 20
        self.color = (255, 0, 0)

    def move_up(self):
        new_y = self.y - self.step

        if new_y - self.radius >= 0:
            self.y = new_y

    def move_down(self, screen_height):
        new_y = self.y + self.step

        if new_y + self.radius <= screen_height:
            self.y = new_y

    def move_left(self):
        new_x = self.x - self.step

        if new_x - self.radius >= 0:
            self.x = new_x

    def move_right(self, screen_width):
        new_x = self.x + self.step

        if new_x + self.radius <= screen_width:
            self.x = new_x

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            self.color,
            (self.x, self.y),
            self.radius
        )