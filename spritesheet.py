import pygame

class Spritesheet:
    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()

    def getSprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((255, 0, 255))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return sprite

    def loadSprites(self):
        sprites = [None]
        for y in range(self.sprite_sheet.get_rect().height // 32):
            for x in range(self.sprite_sheet.get_rect().width // 32):
                sprites.append(self.getSprite(x * 32, y * 32, 32, 32))
        return sprites
