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

# == Highscore persistence ==
def load_highscore():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except:
        return 0

def save_highscore(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

highscore = load_highscore()

# == Bullet class ==
class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 6, 12)
        self.speed = -8

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

# == Load background for start screen ==
try:
    start_background = pygame.image.load("voorbeeld/assets/background start.jpg").convert()
    start_background = pygame.transform.scale(start_background, (WIDTH, HEIGHT))
except Exception as e:
    start_background = None
    print(f"[WARN] Background not loaded: {e}")

# == Load skins into a wheel list ==
skin_names = ["santa", "snowman", "elf"]
skin_images = [
    pygame.transform.scale(pygame.image.load("voorbeeld/assets/Santa_Avatar.png").convert_alpha(), (70, 80)),
    pygame.transform.scale(pygame.image.load("voorbeeld/assets/Snowman.png").convert_alpha(), (90, 100)),
    pygame.transform.scale(pygame.image.load("voorbeeld/assets/Elf .png").convert_alpha(), (80, 90))  # fixed typo
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

# == Start Screen ==
def show_front_screen(screen, highscore, last_score=None):
    font_title = pygame.font.SysFont(None, 72)
    font_text = pygame.font.SysFont(None, 48)

    selected_index = 0

    while True:
        if start_background:
            screen.blit(start_background, (0, 0))
        else:
            screen.fill((0, 0, 50))

        # Title
        title = font_title.render("Santa Dodger", True, (0, 0, 0))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//4))

        # Highscore
        hs_text = font_text.render(f"Highscore: {highscore}", True, (130, 5, 24))
        screen.blit(hs_text, (WIDTH//2 - hs_text.get_width()//2, HEIGHT//4 + 80))

        # Last score
        if last_score is not None:
            last_text = font_text.render(f"Last score: {last_score}", True, (0, 0, 0))
            screen.blit(last_text, (WIDTH//2 - last_text.get_width()//2, HEIGHT//4 + 140))

        # Instruction
        instruction = font_text.render("Press SPACE to start", True, (0, 0, 0))
        screen.blit(instruction, (WIDTH//2 - instruction.get_width()//2, HEIGHT//4 + 200))

        # Skin select
        skin_label = font_text.render("Skin Select:", True, (0, 0, 0))
        screen.blit(skin_label, (WIDTH//2 - skin_label.get_width()//2, HEIGHT//4 + 260))

        preview = skin_images[selected_index]
        screen.blit(preview, (WIDTH//2 - preview.get_width()//2, HEIGHT//4 + 320))

        prev_index = (selected_index - 1) % len(skin_images)
        next_index = (selected_index + 1) % len(skin_images)

        small_prev = pygame.transform.scale(skin_images[prev_index], (40, 50))
        small_next = pygame.transform.scale(skin_images[next_index], (40, 50))

        screen.blit(small_prev, (WIDTH//2 - 120, HEIGHT//4 + 330))
        screen.blit(small_next, (WIDTH//2 + 80, HEIGHT//4 + 330))

        pygame.display.update()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return skin_images[selected_index]
                if event.key == pygame.K_RIGHT:
                    selected_index = (selected_index + 1) % len(skin_images)
                if event.key == pygame.K_LEFT:
                    selected_index = (selected_index - 1) % len(skin_images)

# == Main Game Loop ==
last_score = None
running = True

while running:
    chosen_image = show_front_screen(screen, highscore, last_score)
    player = Player(chosen_image)
    obstacles, gifts, bullets = [], [], []
    background = Background()
    score = Score()
    ammo = 10   # NEW: starting ammo
    gift_spawn_timer, spawn_rate, spawn_timer, score_timer = 0, 60, 0, 0
    game_active = True
    paused = False

    while game_active:
        clock.tick(FPS)

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_active = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not paused:
                if ammo > 0:  # only shoot if ammo left
                    bullets.append(Bullet(player.rect.centerx, player.rect.top))
                    ammo -= 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused

        # PAUSE HANDLING
        if paused:
            font = pygame.font.SysFont(None, 64)
            pause_text = font.render("PAUSED - Press P to Resume", True, (255, 255, 0))
            screen.fill((0, 0, 0))
            screen.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, HEIGHT//2))
            pygame.display.update()
            continue

        # INPUT
        keys = pygame.key.get_pressed()
        player.move(keys)

        # UPDATE OBJECTS
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
                ammo += 3  # NEW: gifts reload ammo

        for bullet in bullets[:]:
            for obs in obstacles[:]:
                if bullet.rect.colliderect(obs.rect):
                    obstacles.remove(obs)
                    bullets.remove(bullet)
                    score.add(5)
                    break

        # DRAW
        background.render(screen)
        player.draw(screen, keys)
        score.draw(screen)

        # NEW: draw ammo counter
        font = pygame.font.SysFont(None, 36)
        ammo_text = font.render(f"Ammo: {ammo}", True, (255, 255, 255))
        screen.blit(ammo_text, (10, 40))

        for obs in obstacles: obs.draw(screen)
        for gift in gifts: gift.draw(screen)
        for bullet in bullets: bullet.draw(screen)

        pygame.display.update()

    # GAME OVER SCREEN
    last_score = score.value
    if score.value > highscore:
        highscore = score.value
        save_highscore(highscore)

    font = pygame.font.SysFont(None, 64)
    screen.fill((0, 0, 0))
    text = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))
    pygame.display.update()
    pygame.time.wait(200)
pygame.quit()

