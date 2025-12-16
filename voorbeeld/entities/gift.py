import pygame
import random
from settings import WIDTH, HEIGHT

class Gift:
    def __init__(self):
        self.size = 30
        self.x = random.randint(0, WIDTH - self.size)
        self.y = -self.size
        self.speed = random.randint(2, 3)
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.rect)  # groen cadeautje
