import pygame
from colors import Colors

Colors = Colors()

class Minimap:
    def __init__(self, player, screen, color, offset, dir, map, filename):
        self.player = player
        self.screen = screen
        self.color = color
        self.width = 100
        self.height = 100
        self.x = 5
        self.y = 10
        self.offset = offset
        self.dirX, self.dirY = dir
        self.map = map

        self.disabled = False

        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()

    def getSprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))

        return sprite

    def loadSprites(self):
        sprites = [None]

        for y in range(self.sprite_sheet.get_rect().height // 8):
            for x in range(self.sprite_sheet.get_rect().width // 8):
                sprites.append(self.getSprite(x * 8, y * 8, 8, 8))

        return sprites

    def getPos(self):
        x, y = 0, 0

        if self.dirX == "left":
            x += self.offset
        elif self.dirX == "right":
            x += self.screen.get_width() - self.width - self.offset

        if self.dirY == "up":
            y += self.offset
        elif self.dirY == "down":
            y += self.screen.get_height() - self.height - self.offset

        return x, y

    def getSpritesPos(self, pos):
        a, b = pos
        x, y = self.getPos()
        
        x += self.offset + a
        y += self.offset + b
        
        return x, y

    def render(self):
        if not self.disabled:
            minimapSprites = self.loadSprites()
            rect = minimapSprites[1].get_rect()
            pygame.draw.rect(self.screen, self.color, (*self.getPos(), self.width, self.height))
            
            for layer in self.map["layers"]:
                x, y = 0, 0
                
                for sprite in layer["data"]:
                    if x == rect.width * layer["height"]:
                        x = 0
                        y += rect.height
                    if sprite != 0:
                        self.screen.blit(minimapSprites[sprite], self.getSpritesPos((x, y)))
                    x += rect.width

            self.screen.blit(self.player.minimapSprite, self.getSpritesPos((self.player.x / 4, self.player.y / 4)))
