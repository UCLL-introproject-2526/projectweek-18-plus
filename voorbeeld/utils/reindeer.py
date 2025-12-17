import pygame
from settings import WIDTH, HEIGHT
from pygame.display import flip

class ReindeerEvent:
    def __init__(self):
        self.image = pygame.image.load("voorbeeld/assets/reindeer_sleigh.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width()//10, self.image.get_height()//10))
        self.rect = self.image.get_rect(midleft=(0, 150))  # start linksboven
        self.speed = 6
        self.active = True
        self.start_time = pygame.time.get_ticks()
        self.duration = 20000

    def update(self):
        self.rect.x += self.speed
        if pygame.time.get_ticks() - self.start_time > self.duration:
            self.active = False


    def draw(self, screen):
        screen.blit(self.image, self.rect)