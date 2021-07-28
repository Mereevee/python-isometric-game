import pygame
from colors import Colors

Colors = Colors()

class Minimap:

    def __init__(self, screen, color, offset, dir):
        self.screen = screen
        self.color = color
        self.width = 100
        self.height = 100
        self.x = 5
        self.y = 10
        self.offset = offset
        self.dirX, self.dirY = dir

        self.disabled = False

    def getPos(self):
        posX, posY = 0, 0
        if self.dirX == "left":
            posX += self.offset
        elif self.dirX == "right":
            posX += self.screen.get_width() - self.width - self.offset

        if self.dirY == "up":
            posY += self.offset
        elif self.dirY == "down":
            posY += self.screen.get_height() - self.height - self.offset

        return posX, posY

    def render(self):
        if not self.disabled:
            pygame.draw.rect(self.screen, self.color, (*self.getPos(), self.width, self.height))