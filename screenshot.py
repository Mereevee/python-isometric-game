from datetime import datetime as dt
from pathlib import Path
import pygame

class Screenshot:
    def __init__(self, folder):
        self.sc = Path(folder)

    def Capture(self, display, size):
        if not self.sc.is_dir():
            self.sc.mkdir()
        name = dt.now().strftime("%Y-%m-%d_%H.%M.%S")
        my_file = self.sc / f"{name}.png"
        num = 1
        while my_file.is_file():
            name = dt.now().strftime("%Y-%m-%d_%H.%M.%S")
            name += f"_{num}"
            my_file = self.sc / f"{name}.png"
            num += 1
        name = f"screenshots/{name}.png"

        image = pygame.Surface(size)
        image.blit(display, (0, 0), ((0, 0), size))
        pygame.image.save(image, name)