import pygame
from settings import *
from entities.player import Player
from entities.obstacle import Obstacle
from entities.gift import Gift
from utils.score import Score

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Santa Dodger")
clock = pygame.time.Clock()

# == highscore ==
highscore = 0

# == Bullet class ==
class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 6, 12)  # small rectangle bullet
        self.speed = -8  # upward movement

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)


# == front screen ==
def show_front_screen(screen, highscore):
    font_title = pygame.font.SysFont(None, 72)
    font_text = pygame.font.SysFont(None, 48)

    title = font_title.render("Santa Dodger", True, (255, 255, 255))
    instruction = font_text.render("Press SPACE to start", True, (200, 200, 200))
    hs_text = font_text.render(f"Highscore: {highscore}", True, (255, 215, 0))

    while True:
        screen.fill((0, 0, 50))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3))
        screen.blit(instruction, (WIDTH//2 - instruction.get_width()//2, HEIGHT//2))
        screen.blit(hs_text, (WIDTH//2 - hs_text.get_width()//2, HEIGHT//2 + 80))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return


# === GAME LOOP ===
running = True

while running:
    # FRONT SCREEN
    show_front_screen(screen, highscore)

    # RESET GAME STATE
    player = Player()
    obstacles = []
    gifts = []
    bullets = []  # NEW: list of bullets
    score = Score()
    gift_spawn_timer = 0
    spawn_rate = 60
    spawn_timer = 0
    score_timer = 0
    game_active = True

    # GAME LOOP
    while game_active:
        clock.tick(FPS)

        # 1. EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_active = False

            # Shooting with left mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left mouse button
                    bullets.append(Bullet(player.rect.centerx, player.rect.top))

        # 2. INPUT
        keys = pygame.key.get_pressed()
        player.move(keys)

        # 3. UPDATE OBJECTS
        if score.value > 100:
            spawn_rate = 40
        elif score.value > 150:
            spawn_rate = 30
        elif score.value > 200:
            spawn_rate = 20
        elif score.value > 250:
            spawn_rate = 10

        spawn_timer += 1
        if spawn_timer > spawn_rate:
            obstacles.append(Obstacle())
            spawn_timer = 0

        for obs in obstacles:
            obs.update()

        gift_spawn_timer += 1
        if gift_spawn_timer > 200:
            gifts.append(Gift())
            gift_spawn_timer = 0

        for gift in gifts:
            gift.update()

        score_timer += 1
        if score_timer >= FPS:
            score.add(1)
            score_timer = 0

        # Update bullets
        for bullet in bullets[:]:
            bullet.update()
            if bullet.rect.bottom < 0:
                bullets.remove(bullet)

        # 4. COLLISIONS
        for obs in obstacles[:]:
            if player.rect.colliderect(obs.rect):
                game_active = False   # GAME OVER

        for gift in gifts[:]:
            if player.rect.colliderect(gift.rect):
                score.add(10)
                gifts.remove(gift)

        # Bullet vs obstacle collisions
        for bullet in bullets[:]:
            for obs in obstacles[:]:
                if bullet.rect.colliderect(obs.rect):
                    obstacles.remove(obs)
                    bullets.remove(bullet)
                    score.add(5)  # reward points
                    break

        # 5. DRAW
        screen.fill(BACKGROUND_COLOR)
        player.draw(screen)
        score.draw(screen)
        for obs in obstacles:
            obs.draw(screen)
        for gift in gifts:
            gift.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)

        pygame.display.update()

    # AFTER GAME LOOP → GAME OVER
    if score.value > highscore:
        highscore = score.value

    font = pygame.font.SysFont(None, 64)
    text = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))
    pygame.display.update()
    pygame.time.wait(2000)

pygame.quit()
