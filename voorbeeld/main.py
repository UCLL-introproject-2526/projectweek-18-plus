import pygame
from settings import WIDTH, HEIGHT, FPS, BACKGROUND_COLOR
from entities.obstacle import Obstacle
from entities.gift import Gift
from entities.player import Player
from utils.score import Score
from utils.reindeer import ReindeerEvent
from background import Background

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Santa Dodger")
clock = pygame.time.Clock()

# == Loading screen == 
screen.fill((30, 30, 60))

loading_font = pygame.font.SysFont(None, 40)
loading_text = loading_font.render("Loading...", True, (255, 255, 255))
screen.blit(loading_text, loading_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
pygame.display.update()


# == Rendeir event ==
REINDEER_IMAGE = pygame.image.load("voorbeeld/assets/reindeer_sleigh.png").convert_alpha()
REINDEER_IMAGE = pygame.transform.scale(REINDEER_IMAGE, (REINDEER_IMAGE.get_width() // 8, REINDEER_IMAGE.get_height() // 8))

# == Fonts ==
FONT_TITLE = pygame.font.Font("voorbeeld/assets/fonts/PressStart2P-Regular.ttf", 48)
FONT_TEXT = pygame.font.Font("voorbeeld/assets/fonts/Montserrat-Bold.ttf", 32)
FONT_SMALL = pygame.font.Font("voorbeeld/assets/fonts/Montserrat-Bold.ttf", 24)

# == highscore ==
highscore = 0


# == Load background for start screen ==
try:
    start_background = pygame.image.load("voorbeeld/assets/background start.jpg").convert()
    start_background = pygame.transform.scale(start_background, (WIDTH, HEIGHT))
except Exception as e:
    background = None
    print(f"[WARN] Background not loaded {e}")


# == Load skins into a wheel list ==
def crop_surface(surface):
    rect = surface.get_bounding_rect()
    return surface.subsurface(rect).copy()

skins = [
    crop_surface(pygame.image.load("voorbeeld/assets/Santa_Avatar.png").convert_alpha()),
    crop_surface(pygame.image.load("voorbeeld/assets/Snowman.png").convert_alpha()),
    crop_surface(pygame.image.load("voorbeeld/assets/Elf .png").convert_alpha())
]

PREVIEW_SIZE = (90, 100)   #geselecteerde skin
SMALL_SIZE = (50, 60)       #linksrechts preview

# == Bullet class ==
class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 6, 12)
        self.speed = -8

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

# == Start Screen ==
def show_front_screen(screen, start_background, highscore, last_score=None):
    selected_index = 0  # start with santa

    while True:
        if start_background:
            screen.blit(start_background, (0, 0))
        else:
            screen.fill((0, 0, 50))

        title = FONT_TITLE.render("Santa Dodger", True, (0, 0, 0))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))

        hs_text = FONT_TEXT.render(f"Highscore: {highscore}", True, (130, 5, 24))
        screen.blit(hs_text, (WIDTH // 2 - hs_text.get_width() // 2, HEIGHT // 4 + 90))

        instruction = FONT_SMALL.render("Press SPACE to start", True, (0, 0, 0))
        screen.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, HEIGHT // 4 + 200))

        # Last score
        if last_score is not None:
            last_text = FONT_SMALL.render(f"Last score: {last_score}", True, (0, 0, 0))
            screen.blit(last_text, (WIDTH // 2 - last_text.get_width() // 2, HEIGHT // 4 + 140))


        # Skin select label
        skin_label = FONT_SMALL.render("Skin Select:", True, (0, 0, 0))
        screen.blit(skin_label, (WIDTH // 2 - skin_label.get_width() // 2, HEIGHT // 4 + 260))

        # Skins (wheel selector)
        preview = pygame.transform.scale(skins[selected_index], PREVIEW_SIZE)
        screen.blit(preview, (WIDTH // 2 - PREVIEW_SIZE[0] // 2, HEIGHT // 4 + 320))

        prev_index = (selected_index - 1) % len(skins)
        next_index = (selected_index + 1) % len(skins)

        small_prev = pygame.transform.scale(skins[prev_index], SMALL_SIZE)
        small_next = pygame.transform.scale(skins[next_index], SMALL_SIZE)

        CENTER_X = WIDTH // 2
        Y_POS = HEIGHT // 4 + 380
        SPACING = 100

        screen.blit(preview, (CENTER_X - preview.get_width() // 2, HEIGHT // 4 + 320))
        screen.blit(small_prev, (CENTER_X - SPACING - small_prev.get_width(), Y_POS))
        screen.blit(small_next, (CENTER_X + SPACING, Y_POS))

        pygame.display.update()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return skins[selected_index]  # return the chosen image
                if event.key == pygame.K_RIGHT:
                    selected_index = (selected_index + 1) % len(skins)
                if event.key == pygame.K_LEFT:
                    selected_index = (selected_index - 1) % len(skins)


# == End Screen ==

def draw_text_outline(font, text, color, outline, x, y):
    text_surf = font.render(text, True, color)
    outline_surf = font.render(text, True, outline)
    text_rect = text_surf.get_rect(center=(x, y))

    for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
        screen.blit(outline_surf, text_rect.move(dx, dy))

    screen.blit(text_surf, text_rect)


def show_game_over(screen, score_value):
    draw_text_outline(FONT_TITLE, "GAME OVER", (200,0,0), (0,0,0), WIDTH // 2, HEIGHT // 2)
    score_text = FONT_TEXT.render(f"Score: {score_value}", True, (0, 0, 0))
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
    screen.blit(score_text, score_rect)
    pygame.display.update()
    pygame.time.wait(2000)

# == Main Game Loop ==
highscore = 0
last_score = None
running = True
reindeer_event = None

while running:

    # 1. Start screen
    chosen_image = show_front_screen(screen, start_background,  highscore, last_score)

    #2. Initialize game    
    player = Player(chosen_image)
    obstacles = []
    gifts = []
    bullets = [] 
    background = Background()
    score = Score()
    gift_spawn_timer = 0
    spawn_rate = 60
    span_rate_base = 60
    ammo = 10
    spawn_timer = 0
    score_timer = 0
    speed_multiplier = 1
    paused = False
    reindeer_spawned = False

    # 3. Main game loop
    game_active = True

    while game_active:
        clock.tick(FPS)

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_active = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not paused:
                if ammo > 0: 
                    bullets.append(Bullet(player.rect.centerx, player.rect.top))
                    ammo -= 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused

        # PAUSED
        if paused:
            font = pygame.font.SysFont(None, 64)
            pause_text = font.render("PAUSED - Press P to Resume", True, (255, 255, 0))
            screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2))
            pygame.display.update()
            continue  # skip updates while paused

        # INPUT
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
        elif score.value > 50:
            spawn_rate = 50
        else:
            spawn_rate = span_rate_base

        spawn_timer += 1
        if spawn_timer >= spawn_rate:
            obstacles.append(Obstacle())
            spawn_timer = 0

        if reindeer_event is not None and reindeer_event.active:
            speed_multiplier = 2
        else:
            speed_multiplier = 1

        for obs in obstacles:
            obs.update(speed_multiplier)

        gift_spawn_timer += 1
        if gift_spawn_timer >= 200:
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
            if player.hitbox.colliderect(obs.rect):
                game_active = False

        for gift in gifts[:]:
            if player.hitbox.colliderect(gift.rect):
                score.add(10)
                ammo += 3
                gifts.remove(gift)

        for bullet in bullets[:]:
            for obs in obstacles[:]:
                if bullet.rect.colliderect(obs.rect):
                    obstacles.remove(obs)
                    bullets.remove(bullet)
                    score.add(5)
                    break

        if score.value >= 50 and score.value <= 215 and reindeer_event is None:
            reindeer_event = ReindeerEvent(REINDEER_IMAGE)

        if reindeer_event is not None and reindeer_event.active:
            spawn_rate = 5
        else:
            spawn_rate = span_rate_base
        
        if reindeer_event is not None and not reindeer_event.active:
            reindeer_event = None

        # DRAW
        background.render(screen)
        player.draw(screen, keys)
        score.draw(screen)

        font = pygame.font.SysFont(None, 36)
        ammo_text = font.render(f"Ammo: {ammo}", True, (255, 255, 255))
        screen.blit(ammo_text, (10, 40))

        for obs in obstacles:
            obs.draw(screen)
        for gift in gifts:
            gift.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)

        if reindeer_event is not None and reindeer_event.active: 
            reindeer_event.update() 
            reindeer_event.draw(screen)


        pygame.display.update()

    # 4. Game Over 
    last_score = score.value
    if score.value > highscore:
        highscore = score.value
    show_game_over(screen, score.value)


pygame.quit()
