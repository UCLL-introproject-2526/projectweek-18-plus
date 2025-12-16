import pygame
from settings import WIDTH, HEIGHT

class Background:
    def __init__(self):
        # Laad de originele afbeelding

        img = pygame.image.load("voorbeeld/assets/background_game.png").convert_alpha()

        # Maak de afbeelding iets breder en langer
        new_width = int(WIDTH * 1.1)   # 10% breder
        new_height = int(HEIGHT * 1.1) # 10% langer
        self.image = pygame.transform.scale(img, (new_width, new_height))

        # Offset om boven links te beginnen
        self.offset_x = (new_width - WIDTH) // 2
        self.offset_y = (new_height - HEIGHT) // 2

    def render(self, screen):
        # Teken de achtergrond met de offset zodat het scherm gevuld is
        screen.blit(self.image, (-self.offset_x, -self.offset_y))



#class Snow:
   # def __init__(self, image_path, speed, screen_height):
        #img = pygame.image.load(image_path).convert_alpha()
        
        # Pixel effect: eerst verkleinen, dan terug vergroten
       # small_size = (img.get_width() // 8, img.get_height() // 8)
       # img_small = pygame.transform.scale(img, small_size)
       # self.image = pygame.transform.scale(img_small, (img.get_width(), img.get_height()))
        
       # self.speed = speed
       # self.y = 0
       # self.screen_height = screen_height

   # def update(self):
       # self.y += self.speed
       # if self.y >= self.screen_height:
           # self.y = 0

   # def render(self, screen):
       # screen.blit(self.image, (0, self.y))
        # screen.blit(self.image, (0, self.y - self.screen_height))
