from spritesheet import Spritesheet

class Isometric:
    def __init__(self, screen, Settings, map):
        self.screen = screen
        self.Settings = Settings
        self.map = map

        self.Spritesheet = Spritesheet("resources/images/spritesheet.png")
        self.sprites = self.Spritesheet.loadSprites()
        self.rect = self.sprites[1].get_rect()

    def render(self):
        for layer in self.map["layers"]:
            a, b = 0, 0

            try:
                offset = layer["offsety"]
            except:
                offset = 0

            for sprite in layer["data"]:
                if a == self.rect.width * layer["height"]:
                    a = 0
                    b += self.rect.height

                x = (a - b) / 2 - (self.rect.width / 2) + (self.Settings.width / 2)
                y = (((a + b) / 2) / 2) - ((self.rect.height / 2) * (layer["height"] / 2)) + (self.Settings.height / 2) - (self.rect.height / 4) + offset

                if sprite != 0:
                    self.screen.blit(self.sprites[sprite], (x, y))
                a += self.rect.width
