import pygame

class Player:
    def __init__(self, map, screen):
        self.map = map
        self.mapWidth = self.map["width"]
        self.mapHeight = self.map["height"]
        self.tileWidth = self.map["properties"][0]["value"]
        self.tileHeight = self.map["properties"][1]["value"]

        self.screen = screen
        self.screenWidth = screen.get_size()[0]
        self.screenHeight = screen.get_size()[1]

        self.sprite = pygame.image.load("resources/images/player.png").convert()
        self.sprite.set_colorkey((255, 0, 255))
        self.rect = self.sprite.get_rect()
        self.minimapSprite = pygame.image.load("resources/images/minimapPlayer.png").convert()

        self.x = 0
        self.y = 0
        self.vel = 2

        self.right = False
        self.left = False
        self.up = False
        self.down = False

        self.last = "RIGHT"

    def render(self):
            x = (self.x - self.y) / 2 - (self.rect.width / 2) + (self.screenWidth / 2)
            y = (((self.x + self.y) / 2) / 2) - ((self.rect.height / 2) * (10 / 2)) + (self.screenHeight / 2) - (self.rect.height / 4) - 16 
            self.screen.blit(self.sprite, (x, y))

    def update(self):
        if self.right:
            self.x += self.vel
            if self.last == "LEFT":
                self.sprite = pygame.transform.flip(self.sprite, True, False)
            self.last = "RIGHT"
            
        elif self.left:
            self.x -= self.vel
            if self.last == "RIGHT":
                self.sprite = pygame.transform.flip(self.sprite, True, False)
            self.last = "LEFT"

        if self.up:
            self.y -= self.vel
            if self.last == "LEFT":
                self.sprite = pygame.transform.flip(self.sprite, True, False)
            self.last = "RIGHT"
        elif self.down:
            self.y += self.vel
            if self.last == "RIGHT":
                self.sprite = pygame.transform.flip(self.sprite, True, False)
            self.last = "LEFT"

        if self.x > (self.mapWidth * self.tileWidth) - self.rect.width:
            self.x = (self.mapWidth * self.tileWidth) - self.rect.width
        elif self.x < 0:
            self.x = 0
        
        if self.y < 0:
            self.y = 0
        elif self.y > (self.mapHeight * self.tileHeight) - self.rect.height:
            self.y = (self.mapHeight * self.tileHeight) - self.rect.height
