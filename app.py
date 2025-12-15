import pygame
from pygame.display import flip

def main():
    pygame.init()

    i = 100

    def create_main_surface():
        screen_size = (1024, 768)
        surface = pygame.display.set_mode(screen_size)
        return surface

    surface = create_main_surface()

    def render_frame(surface, x):
        pygame.draw.circle(surface=surface, color="blue", center=(x,300), radius=50)
    


    while True:
        render_frame(surface, i)
        i += 1
        flip()

    
main()

