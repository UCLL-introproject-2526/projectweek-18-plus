import pygame
from settings import WIDTH, HEIGHT

class Player:
    def __init__(self):
        self.width = 50
        self.height = 60
        self.x = WIDTH // 2
        self.y = HEIGHT - 80
        self.speed = 6
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        self.rect.x = max(0, min(WIDTH - self.width, self.rect.x))

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 0, 0), self.rect)
