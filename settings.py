import pygame

class Settings:
    def __init__(self, fps, width, height):
        self.fps = fps
        self.width = width
        self.height = height
        self.size = (self.width, self.height)
        self.debugKey = pygame.K_F3
        self.screenshotKey = pygame.K_F2