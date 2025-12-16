import pygame
import random
from settings import WIDTH, HEIGHT

class Obstacle:
    def __init__(self):
        self.size = 30
        self.x = random.randint(0, WIDTH - self.size)
        self.y = -self.size
        self.speed = random.randint(3, 6)

        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

        self.image = pygame.image.load("voorbeeld/assets/sneeuwbal.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (55, self.size))

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)
