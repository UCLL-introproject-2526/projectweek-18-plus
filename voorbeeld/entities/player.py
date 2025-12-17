import pygame
from settings import WIDTH, HEIGHT

class Player:
    def __init__(self, image):
        self.width = 60
        self.height = 70
        self.speed = 6

        PLAYER_SIZE = (60, 70)
        self.image = pygame.transform.scale(image, PLAYER_SIZE)

        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 10))
        self.hitbox = self.rect.inflate(-20, -15)

    def move(self, keys):
        # Move left (Q or LEFT arrow)
        if keys[pygame.K_q] or keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        # Move right (D or RIGHT arrow)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Keep player inside screen
        self.rect.x = max(0, min(WIDTH - self.width, self.rect.x))
        self.hitbox.center = self.rect.center

    def draw(self, screen, keys):
        # Flip sprite when moving left (Q or LEFT)
        if keys[pygame.K_q] or keys[pygame.K_LEFT]:
            flipped_image = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped_image, self.rect)
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






