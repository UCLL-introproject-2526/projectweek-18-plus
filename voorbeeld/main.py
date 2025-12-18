import pygame
from settings import WIDTH, HEIGHT, FPS, BACKGROUND_COLOR
import math
from entities.obstacle import Obstacle
from entities.gift import Gift
from entities.player import Player
from utils.score import Score
from utils.reindeer import ReindeerEvent
from background import Background
from saveload import SaveManager, ScoreHistory
import os
import random

pygame.init()
pygame.mixer.init()

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

# == Santa hat ==
SANTA_HAT = pygame.image.load("voorbeeld/assets/santa_hat.png").convert_alpha()
SANTA_HAT = pygame.transform.scale(SANTA_HAT, (48, 36))

GAME_OVER_BG = pygame.image.load("voorbeeld/assets/background start.jpg").convert()
GAME_OVER_BG = pygame.transform.scale(GAME_OVER_BG, (WIDTH, HEIGHT))

# == OBJECTS EXPLOSION ==
EXPLOSION_IMAGE = pygame.image.load("voorbeeld/assets/ontploft.png").convert_alpha()
EXPLOSION_IMAGE = pygame.transform.scale(EXPLOSION_IMAGE, (90, 90))
explosions = []

# == Fonts ==
FONT_TITLE = pygame.font.Font("voorbeeld/assets/fonts/PressStart2P-Regular.ttf", 48)
FONT_TEXT = pygame.font.Font("voorbeeld/assets/fonts/Montserrat-Bold.ttf", 32)
FONT_SMALL = pygame.font.Font("voorbeeld/assets/fonts/Montserrat-Bold.ttf", 24)

title_time = 0

def draw_title(surface, text, font, center_x, y):
    global title_time
    title_time += 0.05

    bob = int(math.sin(title_time) * 4)

    TITLE_COLOR = (220, 20, 60)   # Santa red
    OUTLINE_COLOR = (20, 40, 80)  # Winter blue

    text_surf = font.render(text, True, TITLE_COLOR)
    rect = text_surf.get_rect(center=(center_x, y + bob))

    # Shadow
    shadow = font.render(text, True, (0, 0, 0))
    surface.blit(shadow, (rect.x + 4, rect.y + 4))

    # Outline
    for ox, oy in [(-3,0),(3,0),(0,-3),(0,3),(-3,-3),(3,3),(-3,3),(3,-3)]:
        outline = font.render(text, True, OUTLINE_COLOR)
        surface.blit(outline, (rect.x + ox, rect.y + oy))

    # Main text
    surface.blit(text_surf, rect)

#== santa hat O == 
    target_char = "O"

    if target_char in text:
        index = text.index(target_char)

        # Width of text before the "O"
        prefix = text[:index]
        prefix_width = font.size(prefix)[0]

        # Position of the "O"
        o_x = rect.x + prefix_width
        o_y = rect.y

        # Center hat on top of the letter
        hat_x = o_x + font.size(target_char)[0] // 2 - SANTA_HAT.get_width() // 2
        hat_y = o_y - SANTA_HAT.get_height() + 8

        surface.blit(SANTA_HAT, (hat_x, hat_y))


# === SOUND PATH ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOUND_PATH = os.path.join(BASE_DIR, "sounds")

try:
    sound_intro = pygame.mixer.Sound(os.path.join(SOUND_PATH, "ho-ho-ho-merry-christmas-439603.wav"))
    sound_intro.set_volume(0.70)
    sound_game_over = pygame.mixer.Sound(os.path.join(SOUND_PATH, "game-over-417465.wav"))
    sound_game_over.set_volume(1.0)
    sound_catch = pygame.mixer.Sound(os.path.join(SOUND_PATH, "festive-chime-439612.wav"))
    sound_catch.set_volume(0.80)
    sound_throw = pygame.mixer.Sound(os.path.join(SOUND_PATH, "snowball-throw-hit_4-278172.wav"))
    sound_level_up = pygame.mixer.Sound(os.path.join(SOUND_PATH, "fairy-sparkle-451414.wav"))
    sound_level_up.set_volume(1.0)
    sound_pause = pygame.mixer.Sound(os.path.join(SOUND_PATH, "bell-98033.wav"))
    sound_pause.set_volume(0.9)
    pygame.mixer.music.load(os.path.join(SOUND_PATH, "christmas-holiday-short-1-450314.wav"))
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

    print("All sounds loaded successfully!")

except pygame.error as e:
    print("Error loading sounds:", e)

# == SNOWFLAKES ==
snowflakes = []
for i in range(150):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    speed = random.uniform(1, 3)
    snowflakes.append([x, y, speed])

# == highscore ==
save_manager = SaveManager()
score_history = ScoreHistory()

highscore = save_manager.get_highscore()
selected_skin_index = save_manager.get_skin()

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

selected_skin_index = 0

PREVIEW_SIZE = (90, 100)   #geselecteerde skin
SMALL_SIZE = (50, 60)       #linksrechts preview

# == Bullet class ==
class Bullet:
    def __init__(self, x, y, owner):
        self.rect = pygame.Rect(x-5, y, 16, 22)
        self.speed = -8
        self.owner = owner

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.rect.x + 5, self.rect.y, 6, 12))

# == SKIN WHEEL ==
def draw_skin_wheel(screen, center_x, center_y, skins, index):
    preview = pygame.transform.scale(skins[index], PREVIEW_SIZE)

    prev_index = (index - 1) % len(skins)
    next_index = (index + 1) % len(skins)

    small_prev = pygame.transform.scale(skins[prev_index], SMALL_SIZE)
    small_next = pygame.transform.scale(skins[next_index], SMALL_SIZE)

    # main
    screen.blit(preview,preview.get_rect(center=(center_x, center_y)))

    # left
    screen.blit(small_prev,small_prev.get_rect(center=(center_x - 120, center_y)))

    # right
    screen.blit(small_next,small_next.get_rect(center=(center_x + 120, center_y)))

# == Start Screen ==
def show_front_screen(screen, start_background, highscore, last_score=None, new_highscore=False):
    game_mode = None
    global selected_skin_index
    selected_index = selected_skin_index
    sound_intro.play()

    while True:
        if start_background:
            screen.blit(start_background, (0, 0))
        else:
            screen.fill((0, 0, 50))

        draw_title(screen,"SANTA DODGER",FONT_TITLE,WIDTH // 2,HEIGHT // 4)

        hs_text = FONT_TEXT.render(f"Highscore: {highscore}", True, (130, 5, 24))
        screen.blit(hs_text, (WIDTH // 2 - hs_text.get_width() // 2, HEIGHT // 4 + 90))

        if new_highscore:
            new_text = FONT_SMALL.render("New Highscore!", True,(22,101,190))
            screen.blit(new_text, (WIDTH // 2 - new_text.get_width() // 2, HEIGHT // 4 + 60))

        instruction = FONT_SMALL.render("Select GAME MODE to start", True, (0, 0, 0))
        screen.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, HEIGHT // 4 + 200))

        # Last score
        if last_score is not None:
            last_text = FONT_SMALL.render(f"Last score: {last_score}", True, (0, 0, 0))
            screen.blit(last_text, (WIDTH // 2 - last_text.get_width() // 2, HEIGHT // 4 + 140))

        # === Buttons ===
        button_width = 250
        button_height = 50
        button_spacing = 50

        single_btn = pygame.Rect(WIDTH // 2 - button_width - button_spacing // 2, HEIGHT // 4 + 450,button_width,button_height)

        multi_btn = pygame.Rect(WIDTH // 2 + button_spacing // 2,HEIGHT // 4 + 450,button_width,button_height)

        mouse_pos = pygame.mouse.get_pos()

        # Hover effect
        single_color = (100, 106, 128) if single_btn.collidepoint(mouse_pos) else (33, 42, 73)
        multi_color  = (100, 106, 128) if multi_btn.collidepoint(mouse_pos) else (33, 42, 73)

        pygame.draw.rect(screen, single_color, single_btn, border_radius=8)
        pygame.draw.rect(screen, multi_color, multi_btn, border_radius=8)

        single_text = FONT_SMALL.render("SINGLEPLAYER", True, (255, 255, 255))
        multi_text  = FONT_SMALL.render("MULTIPLAYER", True, (255, 255, 255))

        screen.blit(single_text,single_text.get_rect(center=single_btn.center))
        screen.blit(multi_text,multi_text.get_rect(center=multi_btn.center))

        # # Skin select label
        # skin_label = FONT_SMALL.render("Skin Select: (<- ->)", True, (0, 0, 0))
        # screen.blit(skin_label, (WIDTH // 2 - skin_label.get_width() // 2, HEIGHT // 4 + 260))

        # # Skins (wheel selector)
        # preview = pygame.transform.scale(skins[selected_index], PREVIEW_SIZE)
        # screen.blit(preview, (WIDTH // 2 - PREVIEW_SIZE[0] // 2, HEIGHT // 4 + 320))

        # prev_index = (selected_index - 1) % len(skins)
        # next_index = (selected_index + 1) % len(skins)

        # small_prev = pygame.transform.scale(skins[prev_index], SMALL_SIZE)
        # small_next = pygame.transform.scale(skins[next_index], SMALL_SIZE)

        # CENTER_X = WIDTH // 2
        # Y_POS = HEIGHT // 4 + 380
        # SPACING = 100

        # screen.blit(preview, (CENTER_X - preview.get_width() // 2, HEIGHT // 4 + 320))
        # screen.blit(small_prev, (CENTER_X - SPACING - small_prev.get_width(), Y_POS))
        # screen.blit(small_next, (CENTER_X + SPACING, Y_POS))

        pygame.display.update()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if single_btn.collidepoint(event.pos):
                    sound_intro.stop()
                    selected_skin_index = selected_index
                    return skins[selected_index], "single"

                if multi_btn.collidepoint(event.pos):
                    sound_intro.stop()
                    selected_skin_index = selected_index
                    return skins[selected_index],"multi"

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE:
            #         sound_intro.stop()
            #         return skins[selected_index], "single"

            #     if event.key == pygame.K_RIGHT:
            #         selected_index = (selected_index + 1) % len(skins)

            #     if event.key == pygame.K_LEFT:
            #         selected_index = (selected_index - 1) % len(skins)

def show_single_avatar_select(screen):
    selected_index = 0

    while True:
        screen.blit(start_background,(0,0))

        title = FONT_TEXT.render("Choose your avatar", True, (0, 0, 0))
        screen.blit(title, title.get_rect(center=(WIDTH//2,80)))
        
        prev_index = (selected_index - 1) % len(skins)
        next_index = (selected_index + 1) % len(skins)
        small_prev = pygame.transform.scale(skins[prev_index], SMALL_SIZE)
        small_next = pygame.transform.scale(skins[next_index], SMALL_SIZE)
        

        draw_skin_wheel(screen, WIDTH//2,HEIGHT//2,skins,selected_index)
        
        hint = FONT_SMALL.render("SPACE to confirm", True, (0, 0, 0))
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT - 100)))

        choose = FONT_SMALL.render("(<- ->)", True, (0,0,0))
        screen.blit(choose, choose.get_rect(center=(WIDTH//2,200)))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    selected_index = (selected_index + 1) % len(skins)
                if event.key == pygame.K_LEFT:
                    selected_index = (selected_index - 1) % len(skins)
                if event.key == pygame.K_SPACE:
                    return skins[selected_index]
              
                

def show_multi_avatar_select(screen):
    index_p1 = 0
    index_p2 = 1

    choosing = True

    while True:
        screen.blit(start_background,(0,0))

        title = FONT_TEXT.render(f"Choose avatars", True, (0, 0, 0))
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 60)))

        p1_text = FONT_SMALL.render("Player 1 (Q / D)", True, (0, 0, 0))
        p2_text = FONT_SMALL.render("Player 2 (<- ->)", True, (0, 0, 0))

        screen.blit(p1_text, p1_text.get_rect(center=(WIDTH // 4, 120)))
        screen.blit(p2_text, p2_text.get_rect(center=(WIDTH * 3 // 4, 120)))

        prev_p1 = (index_p1 - 1) % len(skins)
        next_p1 = (index_p1 + 1) % len(skins)
        small_prev_p1 = pygame.transform.scale(skins[prev_p1], SMALL_SIZE)
        small_next_p1 = pygame.transform.scale(skins[next_p1], SMALL_SIZE)

        prev_p2 = (index_p2 - 1) % len(skins)
        next_p2 = (index_p2 + 1) % len(skins)
        small_prev_p2 = pygame.transform.scale(skins[prev_p2], SMALL_SIZE)
        small_next_p2 = pygame.transform.scale(skins[next_p2], SMALL_SIZE)

        draw_skin_wheel(screen,WIDTH // 4,HEIGHT // 2,skins, index_p1)
        draw_skin_wheel(screen,WIDTH * 3 // 4, HEIGHT // 2, skins, index_p2)

        hint = FONT_SMALL.render("SPACE confirm", True, (0, 0, 0))
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT - 80)))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN: #player1
                if event.key == pygame.K_d:
                    index_p1 = (index_p1 +1) % len(skins)
                    if index_p1 == index_p2:
                        index_p1 = (index_p1 +1)%len(skins)
                if event.key == pygame.K_q:
                    index_p1 = (index_p1 - 1) % len(skins)
                    if index_p1 == index_p2:
                        index_p1 = (index_p1 - 1) % len(skins)

                if event.key == pygame.K_LEFT: #player2
                    index_p2 = (index_p2 - 1) % len(skins)
                    if index_p2 == index_p1:
                        index_p2 = (index_p2 - 1) % len(skins)
                if event.key == pygame.K_RIGHT:
                    index_p2 = (index_p2 + 1) % len(skins)
                    if index_p2 == index_p1:
                        index_p2 = (index_p2 + 1) % len(skins)  

                
                if event.key == pygame.K_SPACE:
                    return skins[index_p1], skins[index_p2]

# == End Screen ==

def draw_text_outline(font, text, color, outline, x, y):
    text_surf = font.render(text, True, color)
    outline_surf = font.render(text, True, outline)
    text_rect = text_surf.get_rect(center=(x, y))

    for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
        screen.blit(outline_surf, text_rect.move(dx, dy))

    screen.blit(text_surf, text_rect)


def show_game_over(screen, score_value = None , winner = None, loser = None):
    duration_ms = 2000
    start_time = pygame.time.get_ticks()

    while pygame.time.get_ticks() - start_time < duration_ms:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        t = (pygame.time.get_ticks() - start_time) / 1000.0

        screen.blit(GAME_OVER_BG, (0, 0))

        shake_x = int(math.sin(t * 40) * 6)
        shake_y = int(math.sin(t * 55) * 3)

        draw_text_outline(FONT_TITLE,"GAME OVER",(200, 0, 0),(0, 0, 0),WIDTH // 2 + shake_x,HEIGHT // 2 - 60 + shake_y)

        if game_mode == "single":
            score_text = FONT_TEXT.render(f"Score: {score_value}", True, (0, 0, 0))
            screen.blit(score_text, score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40)))

        pygame.display.flip()
        clock.tick(FPS)

# == SHOOTING ==
def shoot(player):
    if player_ammo[player] > 0:
        bullets.append(Bullet(player.rect.centerx, player.rect.top, player))
        player_ammo[player] -= 1
        sound_throw.play()

# == Main Game Loop ==
last_score = None
running = True
new_highscore = False
reindeer_event = None


while running:

    # 1. Start screen
    chosen_image, game_mode = show_front_screen(screen, start_background, highscore, last_score, new_highscore)
    if game_mode == "single":
        avatar = show_single_avatar_select(screen)
    elif game_mode == "multi":
        avatar1, avatar2 = show_multi_avatar_select(screen)
    
    #uitleg scherm
    how_to_play_single = pygame.image.load("voorbeeld/assets/how_to_play_single.png").convert()
    how_to_play_single = pygame.transform.scale(how_to_play_single,(WIDTH,HEIGHT))

    how_to_play_multi = pygame.image.load("voorbeeld/assets/how_to_play_multi.png").convert()
    how_to_play_multi = pygame.transform.scale(how_to_play_multi,(WIDTH,HEIGHT))

    waiting_for_start = True

    while waiting_for_start:
        if game_mode =="single":
            screen.blit(how_to_play_single,(0,0))
            pygame.display.update()
        
        if game_mode == "multi":
            screen.blit(how_to_play_multi,(0,0))
            pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                waiting_for_start = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting_for_start = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                 waiting_for_start = False

    #  pygame.event.clear()

    #2. Initialize game    
    
    # player(s)
    players = []
    if game_mode == "single":
        players.append(Player(avatar, controls="arrows", start_x=WIDTH // 2 - 80))

    elif game_mode == "multi":
        players.append(Player(avatar1, controls="qd", start_x=WIDTH // 2 + 80, allow_wrap=False))
        players.append(Player(avatar2, controls="arrows", start_x=WIDTH // 2 - 80, allow_wrap=False))


    obstacles = []
    gifts = []
    bullets = [] 
    background = Background()
    scores = {}
    for player in players:
        scores[player] = Score()
    
    # ammo = 10
    player_ammo = {player: 10 for player in players}


    gift_spawn_timer = 0
    spawn_rate = 80
    span_rate_base = 80
    spawn_timer = 0
    score_timer = 0
    speed_multiplier = 1
    paused = False
    reindeer_spawned = False
    next_reindeer_score = 200
    level = 0
    level_threshold = 50
    LEVEL_UP_DURATION = 60
    show_level_up = False
    current_screen = 1

    dead_player = None

    # TIMER (alleen voor multiplayer)
    use_timer = (game_mode == "multi")
    game_time = 60  # seconden
    timer_counter = game_time * FPS

    # 3. Main game loop
    game_active = True

    while game_active:
        clock.tick(FPS)

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_active = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                    sound_pause.play()
                    if paused:
                        pygame.mixer.music.set_volume(0.1)
                    else:
                        pygame.mixer.music.set_volume(0.25)

            # SINGLEPLAYER: schieten met muis of spatie
            if game_mode == "single" and not paused:
                if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                    shoot(player)

            # MULTIPLAYER: elke speler eigen toets
            if game_mode == "multi" and not paused and event.type == pygame.KEYDOWN:
                for player in players: 
                    if player.controls == 'qd' and event.key == pygame.K_z:
                        shoot(player)
                    elif player.controls == 'arrows' and event.key == pygame.K_UP:
                        shoot(player)

        # TIMER UPDATE (alleen multiplayer)
        if use_timer and not paused:
            timer_counter -= 1
            if timer_counter <= 0:
                game_active = False        

        # PAUSED
        if paused:
            font = pygame.font.SysFont(None, 64)
            pause_text = font.render("PAUSED - Press P to Resume", True, (255, 255, 0))
            screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2))
            pygame.display.update()
            continue  # skip updates while paused
        
        # NEW BACKGROUNDS
        keys = pygame.key.get_pressed()

        def transform_falling_objects(screen):
            if (screen % 2) ==  1:
                for obs in obstacles:
                    obs.transform_to_snowball()
            else:
                for obs in obstacles:
                    obs.transform_to_crying_child()

        for player in players:
            player.move(keys)
    
        if player.rect.left > WIDTH:
            background.next_level() 
            current_screen += 1 
            player.rect.right = 0
            transform_falling_objects(current_screen)    

        elif player.rect.right < 0:
            background.next_level()
            current_screen +=1
            player.rect.left = WIDTH
            transform_falling_objects(current_screen)

        # SCORES UPDATEN
        score_timer += 1
        if score_timer >= FPS:
            for player in players:
                scores[player].add(1)
            score_timer = 0
        total_score = sum(scores[player].value for player in players)

        # LEVELS
        new_level = total_score // level_threshold + 1
        if new_level != level:
            level = new_level
            sound_level_up.play()
            show_level_up = True
            level_up_timer = LEVEL_UP_DURATION

        spawn_rate = max(10, span_rate_base - (level - 1) * 5)

        # INPUT
        keys = pygame.key.get_pressed()
        for player in players:
            player.move(keys)

        # UPDATE OBJECTS 
        spawn_timer += 1
        if spawn_timer >= spawn_rate:
            obstacles.append(Obstacle(background.current_index))
            spawn_timer = 0

        gift_spawn_timer += 1
        if gift_spawn_timer >= 3 * spawn_rate:
            gifts.append(Gift())
            gift_spawn_timer = 0

        # for gift in gifts[:]:   -> zorgen dat er iets gebeurd (wenend kind) als je het pakje niet vangt
        #     if gift.rect.top > HEIGHT and game_mode == "single":
        #         font = pygame.font.SysFont(None, 64)
        #         pause_text = font.render("crying baby", True, (255, 255, 0))
        #         screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2))
        #         gifts.remove(gift)

        level_speed_multiplier = 1 + (level - 1) * 0.5

        reindeer_speed_multiplier = 1

        if reindeer_event is not None and reindeer_event.active:
            reindeer_speed_multiplier = 2
            gift_spawn_timer += spawn_rate * 0.1 
            spawn_timer += spawn_rate * 0.05

        total_speed_multiplier = level_speed_multiplier * reindeer_speed_multiplier

        for obs in obstacles:
            obs.update(total_speed_multiplier)

        gift_speed_multiplier = 1 + (level - 1) * 0.5
        for gift in gifts:
            gift.update(gift_speed_multiplier)


        for bullet in bullets[:]:
            bullet.update()
            if bullet.rect.bottom < 0:
                bullets.remove(bullet)

        # COLLISIONS
        for obs in obstacles[:]:
            for player in players:
                if player.hitbox.colliderect(obs.rect):
                    sound_game_over.play()
                    explosions.append({"pos": obs.rect.center,"timer": 10})
                    dead_player = player
                    game_active = False
                    break

        for gift in gifts[:]:
            for player in players:
                if player.hitbox.colliderect(gift.rect):
                    sound_catch.play()
                    scores[player].add(10)
                    player_ammo[player] += 3
                    gifts.remove(gift)
                    break

        for bullet in bullets[:]:
            for obs in obstacles[:]:
                if bullet.rect.colliderect(obs.rect):
                    obstacles.remove(obs)
                    bullets.remove(bullet)
                    scores[bullet.owner].add(3)
                    explosions.append({"pos": obs.rect.center,"timer": 15})
                    break
        
        # REINDEER-EVENT
        if total_score >= next_reindeer_score:
            reindeer_event = ReindeerEvent(REINDEER_IMAGE)
            next_reindeer_score += 200

        if reindeer_event is not None and reindeer_event.active:
            spawn_rate = 5

        else:
            spawn_rate = span_rate_base

        
        if reindeer_event is not None and not reindeer_event.active:
            reindeer_event = None
        
        # SNOW FALLING
        if background.current_index == 0 and not paused:
            for flake in snowflakes:
                flake[1] += flake[2]
                if flake[1] > HEIGHT:
                    flake[1] = -5
                    flake[0] = random.randint(0, WIDTH)

        # DRAW
        background.render(screen)
        for player in players:
            player.draw(screen, keys)
        
        font = pygame.font.SysFont(None, 36)
        
        if game_mode == "single":
            score = scores[players[0]].value
            text = font.render(f"Score: {score}",True,(255, 255, 255))
            screen.blit(text, (10, 10))

            ammo_text = font.render(f"Ammo: {player_ammo[players[0]]}", True, (255, 255, 255))
            screen.blit(ammo_text, (10, 40))

        else:
            x = 10
            for i, player in enumerate(players):
                text = font.render(f"Player {i+1} score: {scores[player].value}",True,(255, 255, 255))
                screen.blit(text, (x, 10))
                
                ammo_text = font.render(f"Ammo: {player_ammo[player]}", True, (255, 255, 255))
                screen.blit(ammo_text, (x, 40))

                x += WIDTH - 240


        if show_level_up and game_mode == "single":
            x = WIDTH // 2
            y = HEIGHT // 2
            draw_text_outline(FONT_TITLE, f"LEVEL {level}!", (255, 255, 0), "white", x, y)

            level_up_timer -= 1
            if level_up_timer <= 0:
                show_level_up = False

        if background.current_index == 0:
            for flake in snowflakes:
                pygame.draw.rect(screen, (255, 255, 255), (flake[0], flake[1], 2, 2))


        for obs in obstacles:
            obs.draw(screen)
        for gift in gifts:
            gift.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)
        
        for explosion in explosions[:]:
            rect = EXPLOSION_IMAGE.get_rect(center=explosion["pos"])
            screen.blit(EXPLOSION_IMAGE, rect)

            explosion["timer"] -= 1
            if explosion["timer"] <= 0:
                explosions.remove(explosion)

        if reindeer_event is not None and reindeer_event.active: 
            reindeer_event.update() 
            reindeer_event.draw(screen)

        dark_overlay = pygame.Surface((WIDTH, HEIGHT))
        dark_overlay.set_alpha(200) 
        dark_overlay.fill((0, 0, 0)) 

        if  500 <= total_score <= 600: 
            screen.blit(dark_overlay, (0, 0))
        
        if use_timer:
            seconds_left = timer_counter // FPS
            font = pygame.font.SysFont(None, 45)
            timer_text = font.render(f"Time: {seconds_left}", True, (33, 42, 73))
            text_rect = timer_text.get_rect(center=(WIDTH // 2, 10 + timer_text.get_height() // 2))
            screen.blit(timer_text, text_rect)

        pygame.display.update()

    # 4. Game Over 

    score_for_highscore = None
    score_winner = None
    score_loser = None

    new_highscore = False

    winner_text = None

    if game_mode == "single":
        last_score = scores[players[0]].value
        score_history.add_score(last_score)

        if last_score > highscore:
            highscore = last_score
            new_highscore = True
            save_manager.set_highscore(highscore)

    else:  # multiplayer
        if dead_player is not None:
            loser = dead_player
            winner = players[0] if players[1] == loser else players[1]

            score_winner = scores[winner].value
            score_loser = scores[loser].value

            if winner == players[0]:
                winner_text = "Player 1 wins!"
            else:
                winner_text = "Player 2 wins!"

        else:
            p1, p2 = players
            s1 = scores[p1].value
            s2 = scores[p2].value

            if s1 > s2:
                winner = p1
                loser = p2
                winner_text = "Player 1 wins!"
            elif s2 > s1:
                winner = p2
                loser = p1
                winner_text = "Player 2 wins!"
            else:
                winner = None
                loser = None
                winner_text = "It's a draw!"

            score_winner = max(s1, s2)
            score_loser = min(s1, s2)

    show_game_over(screen, last_score, score_winner, score_loser)

    if winner_text:
        font = pygame.font.Font(None, 48)
        text_surf = FONT_TEXT.render(winner_text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=(WIDTH//2, HEIGHT//2 + 140))
        screen.blit(text_surf, text_rect)
        pygame.display.update()
        pygame.time.wait(1000)


pygame.quit()
