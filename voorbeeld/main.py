import pygame
from settings import WIDTH, HEIGHT, FPS, BACKGROUND_COLOR
from entities.obstacle import Obstacle
from entities.gift import Gift
from utils.score import Score
from background import Background

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
# == Load background for start screen ==
try:
    background = pygame.image.load("voorbeeld/assets/background.png").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
except Exception as e:
    background = None
    print(f"[WARN] Background not loaded: {e}")

# == Load skins into a wheel list ==
skin_names = ["santa", "snowman", "elf"]
skin_images = [
    pygame.transform.scale(pygame.image.load("voorbeeld/assets/Santa_Avatar.png").convert_alpha(), (70, 80)),
    pygame.transform.scale(pygame.image.load("voorbeeld/assets/Snowman.png").convert_alpha(), (90, 100)),
    pygame.transform.scale(pygame.image.load("voorbeeld/assets/Elf .png").convert_alpha(), (80, 90))
]

# == Player class ==
class Player:
    def __init__(self, image):
        self.width = 60
        self.height = 70
        self.x = WIDTH // 2
        self.y = HEIGHT - 80
        self.speed = 6
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.image = image

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        self.rect.x = max(0, min(WIDTH - self.width, self.rect.x))

    def draw(self, screen, keys):
        if keys[pygame.K_LEFT]:
            screen.blit(pygame.transform.flip(self.image, True, False), self.rect)
        else:
            screen.blit(self.image, self.rect)

# == Bullet class ==
class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 6, 12)
        self.speed = -8

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

# == Start Screen with new text layout ==
def show_front_screen(screen, highscore, last_score=None):
    font_title = pygame.font.SysFont(None, 72)
    font_text = pygame.font.SysFont(None, 48)

    selected_index = 0  # start with santa

    while True:
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((0, 0, 50))

        # 1. Title
        title = font_title.render("Santa Dodger", True, (255, 255, 255))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//4))

        # 2. Highscore
        hs_text = font_text.render(f"Highscore: {highscore}", True, (255, 215, 0))
        screen.blit(hs_text, (WIDTH//2 - hs_text.get_width()//2, HEIGHT//4 + 80))

        # 3. Last score
        if last_score is not None:
            last_text = font_text.render(f"Last score: {last_score}", True, (200, 200, 200))
            screen.blit(last_text, (WIDTH//2 - last_text.get_width()//2, HEIGHT//4 + 140))

        # 4. Press SPACE to start
        instruction = font_text.render("Press SPACE to start", True, (200, 200, 200))
        screen.blit(instruction, (WIDTH//2 - instruction.get_width()//2, HEIGHT//4 + 200))

        # 5. Skin select label
        skin_label = font_text.render("Skin Select:", True, (255, 255, 255))
        screen.blit(skin_label, (WIDTH//2 - skin_label.get_width()//2, HEIGHT//4 + 260))

        # 6. Skins (wheel selector)
        preview = skin_images[selected_index]
        screen.blit(preview, (WIDTH//2 - preview.get_width()//2, HEIGHT//4 + 320))

        prev_index = (selected_index - 1) % len(skin_images)
        next_index = (selected_index + 1) % len(skin_images)

        small_prev = pygame.transform.scale(skin_images[prev_index], (40, 50))
        small_next = pygame.transform.scale(skin_images[next_index], (40, 50))

        screen.blit(small_prev, (WIDTH//2 - 80, HEIGHT//4 + 380))
        screen.blit(small_next, (WIDTH//2 + 40, HEIGHT//4 + 380))

        pygame.display.update()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return skin_images[selected_index]  # return the chosen image
                if event.key == pygame.K_RIGHT:
                    selected_index = (selected_index + 1) % len(skin_images)
                if event.key == pygame.K_LEFT:
                    selected_index = (selected_index - 1) % len(skin_images)

# == Main Game Loop ==
highscore = 0
last_score = None
running = True

while running:
    chosen_image = show_front_screen(screen, highscore, last_score)
    player = Player(chosen_image)
    obstacles = []
    gifts = []
    bullets = [] 
    background = Background()
    score = Score()
    gift_spawn_timer = 0
    spawn_rate = 60
    spawn_timer = 0
    score_timer = 0
    game_active = True

    while game_active:
        clock.tick(FPS)

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_active = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                bullets.append(Bullet(player.rect.centerx, player.rect.top))

            # Shooting with left mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left mouse button
                    bullets.append(Bullet(player.rect.centerx, player.rect.top))

        # 2. INPUT
        keys = pygame.key.get_pressed()
        player.move(keys)

        # UPDATE OBJECTS (fixed ordering)
        if score.value > 250:
            spawn_rate = 10
        elif score.value > 200:
            spawn_rate = 20
        elif score.value > 150:
            spawn_rate = 30
        elif score.value > 100:
            spawn_rate = 40
        else:
            spawn_rate = 60

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

        for bullet in bullets[:]:
            bullet.update()
            if bullet.rect.bottom < 0:
                bullets.remove(bullet)

        # COLLISIONS
        for obs in obstacles[:]:
            if player.rect.colliderect(obs.rect):
                game_active = False

        for gift in gifts[:]:
            if player.rect.colliderect(gift.rect):
                score.add(10)
                gifts.remove(gift)

        for bullet in bullets[:]:
            for obs in obstacles[:]:
                if bullet.rect.colliderect(obs.rect):
                    obstacles.remove(obs)
                    bullets.remove(bullet)
                    score.add(5)
                    break

        # 5. DRAW
        background.render(screen)
        player.draw(screen, keys)
        score.draw(screen)
        for obs in obstacles:
            obs.draw(screen)
        for gift in gifts:
            gift.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)

        pygame.display.update()

    # GAME OVER SCREEN
    last_score = score.value
    if score.value > highscore:
        highscore = score.value

    font = pygame.font.SysFont(None, 64)
    text = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))
    pygame.display.update()
    pygame.time.wait(2000)

pygame.quit()
