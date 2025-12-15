import pygame
def main():
        
    i=2

    if i > 1:
        i += 1

    # Initialize Pygame
    pygame.init()

    def create_main_surface():
        # Tuple representing width and height in pixels
        screen_size = (1024, 768)

        # Create window with given size
        pygame.display.set_mode(screen_size)

    create_main_surface()

main()


