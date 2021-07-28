import sys
import json
import pygame
from pygame.locals import *
from settings import Settings
from minimap import Minimap
from colors import Colors
from spritesheet import Spritesheet
from screenshot import Screenshot

pygame.init()
pygame.font.init()

Settings = Settings(60, 640, 480)
Colors = Colors()
Screenshot = Screenshot()
screen = pygame.display.set_mode((Settings.width, Settings.height))
Minimap = Minimap(screen, Colors.BLUE, 10, ("right", "up"))
Spritesheet = Spritesheet('resources/images/spritesheet.png')

sprites = Spritesheet.loadSprites()

font = pygame.font.Font("resources/fonts/monogram.ttf", 31)
debugText = font.render("Debug mode", False, Colors.WHITE)
debug = False
fpsClock = pygame.time.Clock()

with open("resources/maps/map.json") as mapJson:
    map = json.load(mapJson)
    mapJson.close()

# Game loop.
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYUP:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
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
                if debug:
                    debug = False
                else:
                    debug = True
            elif event.key == Settings.screenshotKey:
                Screenshot.Capture(screen, Settings.size)
    
    # Update.
    fpsText = font.render("%.0f fps" % fpsClock.get_fps(), False, Colors.WHITE)

    ## Draw.
    screen.fill(Colors.BLACK)

    # Isometric Map
    rect = sprites[1].get_rect()
    # for num1 in range(1):
    for layer in map["layers"]:
        a, b = 0, 0
        try:
            offset = layer["offsety"]
        except:
            offset = 0
        for sprite in layer["data"]:
            if a >= rect.width * layer["height"]:
                a = 0
                b += rect.height
            x = (((a / rect.width) * 0.5 * rect.width + (b / rect.height) * -0.5 * rect.width) - rect.width / 2) + Settings.width / 2
            y = ((((a / rect.width) * 0.25 * rect.width + (b / rect.height) * 0.25 * rect.width) - (rect.height / 2) * 5) - (rect.height / 4) + offset) + Settings.height / 2
            if sprite != 0:
                screen.blit(sprites[sprite], (x, y))
            a += rect.width

    # Minimap
    Minimap.render()
    
    #teste fodase
    xteste = 0
    yteste = 0
    if debug:
        #spritesheet
        for sprite in sprites:
            if sprite != None:
                if xteste > Settings.width:
                    yteste += 32
                    xteste = 0
                pygame.draw.rect(screen, Colors.PINKD, (xteste, yteste, 32, 32))
                pygame.draw.rect(screen, Colors.PINK, (xteste + 1, yteste + 1, 30, 30))
                screen.blit(sprite, (xteste, yteste))
                xteste += 32
        #spritesheet
        #debug text
        screen.blit(debugText, (0, Settings.height - debugText.get_rect().height))
        screen.blit(fpsText, (Settings.width - fpsText.get_rect().width, Settings.height - fpsText.get_rect().height))
        #debug text
    
    #teste fodase
    pygame.display.flip()
    fpsClock.tick(Settings.fps)