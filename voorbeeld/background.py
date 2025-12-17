import pygame
from settings import WIDTH, HEIGHT

class Background:
    def __init__(self):
        self.background_files = [
            "voorbeeld/assets/background_game.png",
            "voorbeeld/assets/secondbackground_game.png"
        ]
        self.current_index = 0
        self.images = []

        for file in self.background_files:
            try:
                img = pygame.image.load(file).convert_alpha()
                self.images.append(pygame.transform.scale(img, (WIDTH, HEIGHT)))
                print(f"Succes: {file} geladen") 
            except Exception as e:
                print(f"Fout: Kan {file} niet laden. Error: {e}")
                surf = pygame.Surface((WIDTH, HEIGHT))
                surf.fill((255, 0, 0))
                self.images.append(surf)

    def next_level(self):
        self.current_index = (self.current_index + 1) % len(self.images)

    def render(self, screen):
        screen.blit(self.images[self.current_index], (0, 0))


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
