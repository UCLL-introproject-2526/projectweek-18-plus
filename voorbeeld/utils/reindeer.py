import pygame
from settings import WIDTH, HEIGHT
from pygame.display import flip

class ReindeerEvent:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect(midleft=(-20, 150))  # start linksboven
        self.speed = 4
        self.active = True
        self.start_time = pygame.time.get_ticks()
        self.duration = 4000

    def update(self):
        self.rect.x += self.speed
        if pygame.time.get_ticks() - self.start_time > self.duration:
            self.active = False


    def draw(self, screen):
        screen.blit(self.image, self.rect)