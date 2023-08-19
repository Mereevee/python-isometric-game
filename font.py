import pygame

class Font:
    def __init__(self, text, color):
        self.text = text
        self.color = color
        self.font = pygame.font.Font("resources/fonts/monogram.ttf", 31)
        self.render = self.font.render(self.text, False, self.color)
        self.width = self.render.get_rect()[2]
        self.height = self.render.get_rect()[3]

    def set_render(self, text):
        self.render = self.font.render(text, False, self.color)
        self.width = self.render.get_rect()[2]
        self.height = self.render.get_rect()[3]
