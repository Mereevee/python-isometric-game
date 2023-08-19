import sys
import json
import pygame
from pathlib import Path
from pygame.locals import *
from settings import Settings
from isometric import Isometric
from minimap import Minimap
from spritesheet import Spritesheet
from screenshot import Screenshot
from font import Font
from player import Player

with open("resources/maps/map.json") as mapJson:
    map = json.load(mapJson)
    mapJson.close()

pygame.init()
pygame.font.init()

Settings = Settings(60, 640, 480)
Screenshot = Screenshot("screenshots")
screen = pygame.display.set_mode((Settings.width, Settings.height), pygame.SCALED)
Spritesheet = Spritesheet("resources/images/spritesheet.png")
Isometric = Isometric(screen, Settings, map)
Player = Player(map, screen)
Minimap = Minimap(Player, screen, "BLUE", 10, ("right", "up"), map, "resources/images/minimapSpritesheet.png")

running = True
sprites = Spritesheet.loadSprites()
debugText = Font("Debug mode", "WHITE")
fpsClock = pygame.time.Clock()

maps = []
for map in Path("resources/maps").glob("*.json"):
    maps.append(str(map.name))
mapIndex = 0
mapText = Font(maps[mapIndex], "WHITE")

# Game loop.
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYUP:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_0 and pygame.key.get_mods() & pygame.KMOD_CTRL:
                mapIndex += 1
                if mapIndex + 1 > len(maps):
                    mapIndex = 0                
                with open(f"resources/maps/{maps[mapIndex]}") as mapJson:
                    map = json.load(mapJson)
                    mapJson.close()
                Isometric.map = map
                Minimap.map = map
                mapText.set_render(maps[mapIndex])
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
            elif event.key == pygame.K_RIGHT:
                Player.right = False
            elif event.key == pygame.K_LEFT:
                Player.left = False
            elif event.key == pygame.K_UP:
                Player.up = False
            elif event.key == pygame.K_DOWN:
                Player.down = False
        elif event.type == KEYDOWN:
            if event.key == pygame.K_RIGHT:
                Player.right = True
            elif event.key == pygame.K_LEFT:
                Player.left = True
            elif event.key == pygame.K_UP:
                Player.up = True
            elif event.key == pygame.K_DOWN:
                Player.down = True

    # Update.
    Player.update()
    fpsText = Font(f"{fpsClock.get_fps():.0f} fps", "WHITE")

    # Draw.
    screen.fill("BLACK")

    Isometric.render()
    Player.render()
    Minimap.render()

    if Settings.debug:
        x, y = 0, 0
        for sprite in sprites:
            if sprite is not None:
                if x > Settings.width:
                    y += 32
                    x = 0
                pygame.draw.rect(screen, (194, 13 , 255), (x, y, 32, 32))
                pygame.draw.rect(screen, (255, 0, 255), (x + 1, y + 1, 30, 30))
                screen.blit(sprite, (x, y))
                x += 32
        screen.blit(debugText.render, (0, Settings.height - debugText.height))
        screen.blit(fpsText.render, (0, Settings.height - fpsText.height - debugText.height))
        screen.blit(mapText.render, (0, Settings.height - mapText.height - fpsText.height - debugText.height))

    pygame.display.flip()
    fpsClock.tick(Settings.fps)

pygame.quit()
sys.exit()
