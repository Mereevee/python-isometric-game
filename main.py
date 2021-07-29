import sys
import json
import pygame
from pygame.locals import *
from settings import Settings
from isometric import Isometric
from minimap import Minimap
from colors import Colors
from spritesheet import Spritesheet
from screenshot import Screenshot

with open("resources/maps/map.json") as mapJson:
    map = json.load(mapJson)
    mapJson.close()

pygame.init()
pygame.font.init()

Settings = Settings(60, 640, 480)
Colors = Colors()
Screenshot = Screenshot()
screen = pygame.display.set_mode((Settings.width, Settings.height))
Minimap = Minimap(screen, Colors.BLUE, 10, ("right", "up"), map, "resources/images/minimapSpritesheet.png")
Spritesheet = Spritesheet("resources/images/spritesheet.png")
Isometric = Isometric(screen, Settings, map)

running = True
sprites = Spritesheet.loadSprites()
font = pygame.font.Font("resources/fonts/monogram.ttf", 31)
debugText = font.render("Debug mode", False, Colors.WHITE)
fpsClock = pygame.time.Clock()

# Game loop.
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYUP:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_b:
                if not Minimap.disabled:
                    if Minimap.dirX == "right":
                        Minimap.dirX = "left"
                    else:
                        Minimap.dirX = "right"
            elif event.key == pygame.K_c:
                if not Minimap.disabled:
                    if Minimap.dirY == "up":
                        Minimap.dirY = "down"
                    else:
                        Minimap.dirY = "up"
            elif event.key == pygame.K_F1:
                if Minimap.disabled:
                    Minimap.disabled = False
                else:
                    Minimap.disabled = True
            elif event.key == Settings.debugKey:
                if Settings.debug:
                    Settings.debug = False
                else:
                    Settings.debug = True
            elif event.key == Settings.screenshotKey:
                Screenshot.Capture(screen, Settings.size)
    
    # Update.
    fpsText = font.render("%.0f fps" % fpsClock.get_fps(), False, Colors.WHITE)

    ## Draw.
    screen.fill(Colors.BLACK)

    Isometric.render()
    Minimap.render()

    if Settings.debug:
        x, y = 0, 0
        for sprite in sprites:
            if sprite != None:
                if x > Settings.width:
                    y += 32
                    x = 0
                pygame.draw.rect(screen, Colors.PINKD, (x, y, 32, 32))
                pygame.draw.rect(screen, Colors.PINK, (x + 1, y + 1, 30, 30))
                screen.blit(sprite, (x, y))
                x += 32
        screen.blit(debugText, (0, Settings.height - debugText.get_rect().height))
        screen.blit(fpsText, (Settings.width - fpsText.get_rect().width, Settings.height - fpsText.get_rect().height))
    
    pygame.display.flip()
    fpsClock.tick(Settings.fps)

pygame.quit()
sys.exit()