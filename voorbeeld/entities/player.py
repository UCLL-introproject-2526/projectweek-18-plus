import pygame
from settings import WIDTH, HEIGHT
from pygame.display import flip

class Player:
    def __init__(self, image, controls="arrows", start_x=None,  allow_wrap=True):
        self.width = 60
        self.height = 70
        self.speed = 4
        self.controls = controls
        self.allow_wrap = allow_wrap

        PLAYER_SIZE = (60, 70)
        self.image = pygame.transform.scale(image, PLAYER_SIZE)

        if start_x is None:
            start_x = WIDTH // 2
        
        self.rect = self.image.get_rect(midbottom=(WIDTH//2, HEIGHT - 10))
        self.hitbox = self.rect.inflate(-20, -15)

    def move(self, keys):
        if self.controls == "arrows":
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.speed
            if keys[pygame.K_RIGHT]:
                self.rect.x += self.speed

        elif self.controls == "qd":
            if keys[pygame.K_q]:
                self.rect.x -= self.speed
            if keys[pygame.K_d]:
                self.rect.x += self.speed
                
        if not self.allow_wrap:
            # alleen in multiplayer
            self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))

        self.hitbox.center = self.rect.center

    def draw(self, screen, keys):
        flipped = False

        if self.controls == "arrows" and keys[pygame.K_LEFT]:
            flipped = True
        if self.controls == "qd" and keys[pygame.K_q]:
            flipped = True

        if flipped:
            screen.blit(pygame.transform.flip(self.image, True, False), self.rect)
        else:
            screen.blit(self.image, self.rect)

# class Player:
#     def __init__(self):
#         self.width = 50
#         self.height = 60
#         self.x = WIDTH // 2
#         self.y = HEIGHT - 80
#         self.speed = 6

#         self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

#         self.image = pygame.image.load("voorbeeld/assets/Santa_Avatar.png").convert_alpha()
#         self.image = pygame.transform.scale(self.image, (70, 80))

#     def move(self, keys):
#         if keys[pygame.K_LEFT]:
#             self.rect.x -= self.speed
#         if keys[pygame.K_RIGHT]:
#             self.rect.x += self.speed

#         self.rect.x = max(0, min(WIDTH - self.width, self.rect.x))

#     def draw(self, screen, keys):
#         if keys[pygame.K_LEFT]:
#             screen.blit(pygame.transform.flip(self.image, True, False), self.rect)
#         elif keys[pygame.K_RIGHT]:
#             screen.blit(self.image, self.rect)
#         else:
#             screen.blit(self.image, self.rect)






