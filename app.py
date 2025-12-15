import pygame
from pygame.display import flip
import time

def main():
    pygame.init()

    i = 0

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
        surface.blit(man, (x, 300))
        flip()

    
    clock = pygame.time.Clock()


    while True:

        elapsed_ms = clock.tick(60)
        elapsed_sec = elapsed_ms / 1000  

        render_frame(surface, i)
        i += elapsed_sec*10

    
main()

