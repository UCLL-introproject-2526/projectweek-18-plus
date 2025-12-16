import pygame
from pygame.display import flip
import time

class Background:
    def __init__(self):
        self._image = self._create_image()
        self._y = 430

    def _create_image(self):
        return pygame.image.load("background.png")

    def render(self, surface):
        h = self._image.get_height() 

        surface.blit(self._image, (0, self._y))
        surface.blit(self._image, (0, self._y - h))
    
    def update(self, elapsed_seconds):
        speed = 50
        self._y += elapsed_seconds* speed

class State:
    def __init__(self):
        self._background = Background()

    def render(self, surface):
        self._background.render(surface)
    
    def update(self, elapsed_seconds):
        self._background.update(elapsed_seconds)

def main():
    pygame.init()

    i = 0
    state = State()

    def create_main_surface():
        screen_size = (1024, 768)
        surface = pygame.display.set_mode(screen_size)
        return surface

    surface = create_main_surface()

    def clear_surface(surface):
        surface.fill("black")

    man = pygame.image.load("rsz_kerstman.png")

    def render_frame(surface, x):
        clear_surface(surface)
        pygame.draw.circle(surface=surface, color="blue", center=(x,300), radius=50)
        state.update(elapsed_sec)
        state.render(surface)
        surface.blit(man, (x, 300))
        flip()

    
    clock = pygame.time.Clock()



    while True:

        elapsed_ms = clock.tick(60)
        elapsed_sec = elapsed_ms / 1000  

        render_frame(surface, i)
        i += elapsed_sec*50
    
main()

