import sys
import json
import pygame
from numpy import random
from pygame.locals import *
from settings import Settings
from isometric import Isometric
from minimap import Minimap
from colors import Colors
from spritesheet import Spritesheet
from screenshot import Screenshot
from font import Font

with open("resources/maps/map.json") as mapJson:
    map = json.load(mapJson)
    mapJson.close()

pygame.init()
pygame.font.init()

Settings = Settings(60, 640, 480)
Colors = Colors()
Screenshot = Screenshot("screenshots")
screen = pygame.display.set_mode((Settings.width, Settings.height), pygame.SCALED)
Minimap = Minimap(screen, Colors.BLUE, 10, ("right", "up"), map, "resources/images/minimapSpritesheet.png")
Spritesheet = Spritesheet("resources/images/spritesheet.png")
Isometric = Isometric(screen, Settings, map)

running = True
sprites = Spritesheet.loadSprites()
debugText = Font("Debug mode", Colors.WHITE)
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
    fpsText = Font(f"{fpsClock.get_fps():.0f} fps", Colors.WHITE)

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
        screen.blit(debugText.render, (0, Settings.height - debugText.height))
        screen.blit(fpsText.render, (0, Settings.height - fpsText.height - debugText.height))
        screen.blit(mapText.render, (0, Settings.height - mapText.height - fpsText.height - debugText.height))

    pygame.display.flip()
    fpsClock.tick(Settings.fps)

pygame.quit()
sys.exit()