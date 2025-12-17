import pygame
import random
from settings import WIDTH, HEIGHT

class Gift:
    def __init__(self):
        self.size = 40
        self.x = random.randint(0, WIDTH - self.size)
        self.y = -self.size
        self.speed = random.randint(2, 4)
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

        gift_images = [
            "voorbeeld/assets/pakje_1.png",
            "voorbeeld/assets/pakje_2.png",
            "voorbeeld/assets/pakje_3.png",
            "voorbeeld/assets/pakje_4.png",
        ]

        image_path = random.choice(gift_images)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

    def update(self, multiplier = 1):
        self.rect.y += self.speed * 1

    def draw(self, screen):
        screen.blit(self.image, self.rect)
