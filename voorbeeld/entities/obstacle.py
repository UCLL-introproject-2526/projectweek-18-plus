import pygame
import random
from settings import WIDTH, HEIGHT

class Obstacle:
    def __init__(self, level_index=0):

        if level_index == 0:
            image_path = "voorbeeld/assets/sneeuwbal.png"
            self.breedte = 30
            self.hoogte = 30
            self.state = "snowball"
        elif level_index == 1:
            image_path = "voorbeeld/assets/cryingbaby.png" 
            self.breedte = 50
            self.hoogte = 50
            self.state = "child"
        else:
            image_path = "voorbeeld/assets/sneeuwbal.png"
            self.breedte = 30
            self.hoogte = 30
            self.state = "snowball"

        self.x = random.randint(0, WIDTH - self.breedte)
        self.y = -self.hoogte
        self.speed = random.randint(2, 5)
        self.rect = pygame.Rect(self.x, self.y, self.breedte, self.hoogte)

        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.breedte, self.hoogte))
    
    def transform_to_crying_child(self):
        if self.state == "snowball":
            center = self.rect.center

            self.state = "child"
            self.breedte = 50
            self.hoogte = 50

            self.image = pygame.image.load("voorbeeld/assets/cryingbaby.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.breedte, self.hoogte))

            self.rect = pygame.Rect(0, 0, self.breedte, self.hoogte)
            self.rect.center = center
    
    def transform_to_snowball(self):
        if self.state == "child":
            center = self.rect.center

            self.state = "snowball"
            self.breedte = 30
            self.hoogte = 30

            self.image = pygame.image.load("voorbeeld/assets/sneeuwbal.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.breedte, self.hoogte))

            self.rect = pygame.Rect(0, 0, self.breedte, self.hoogte)
            self.rect.center = center

    def update(self, multiplier=1):
        self.rect.y += self.speed * multiplier

    def draw(self, screen):
        screen.blit(self.image, self.rect)
