import pygame as p
import random

# Initialize Pygame
p.init()

# Game Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 837
COLORS = {
    'SKY': (135, 206, 235),
    'PLAYER': (255, 0, 0),
    'PLATFORM': (0, 128, 0)
}

# Player Settings
PLAYER_START_POS = [200, 675]
PLAYER_SIZE = [16, 16]
PLAYER_SPEED = 10
GRAVITY = 0.5
JUMP_STRENGTH = 14
COYOTE_TIME = 0.1

# Platform Generation Settings
PLATFORM_INTERVAL = 75
MIN_PLATFORM_WIDTH = 100
MAX_PLATFORM_WIDTH = 300
MIN_GAP = 100
MAX_GAP = 200
SCROLL_SPEED = 3
DIFFICULTY_INTERVAL = 300
DIFFICULTY_INCREMENT = 0.1

# Game Setup
WIN = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
p.display.set_caption("game.exe")

# Initialize game state
player_pos = PLAYER_START_POS.copy()
player_velocity = [0, 0]
jumping = False
coyote_timer = 0

# Initial platforms setup
platforms = [
    p.Rect(0, 780, SCREEN_WIDTH / 3, 43),
    p.Rect(SCREEN_WIDTH / 3, 650, SCREEN_WIDTH / 10, 20),
    p.Rect((SCREEN_WIDTH * 13) / 30, 520, SCREEN_WIDTH / 10, 20),
    p.Rect((SCREEN_WIDTH * 15) / 30, 390, SCREEN_WIDTH / 10, 20),
]

# Game variables
initial_platform_x = 900
last_platform_y = 390

while initial_platform_x < SCREEN_WIDTH:
    platform_width = random.randint(150, 300)  # Wider platforms for initial ease
    platform_y = last_platform_y + random.randint(-100, 100)
    platform_y = max(100, min(platform_y, SCREEN_HEIGHT - 100))  # Keep within bounds
    platforms.append(p.Rect(initial_platform_x, platform_y, platform_width, 20))
    initial_platform_x += platform_width + random.randint(50, 150)
    last_platform_y = platform_y

# Game loop variables
clock = p.time.Clock()
running = True
platform_timer = 0
difficulty_timer = 0
scroll_speed = SCROLL_SPEED

while running:
    # Time management
    dt = clock.tick(90) / 1000
    coyote_timer -= dt

    # Event handling
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
        if event.type == p.KEYDOWN:
            if event.key == p.K_a:
                player_velocity[0] = -PLAYER_SPEED
            if event.key == p.K_d:
                player_velocity[0] = PLAYER_SPEED
            if event.key == p.K_SPACE and (not jumping or coyote_timer > 0):
                jumping = True
                coyote_timer = 0
                player_velocity[1] = -JUMP_STRENGTH
        if event.type == p.KEYUP:
            if event.key in [p.K_a, p.K_d]:
                player_velocity[0] = 0

    # Physics update
    player_velocity[1] += GRAVITY
    player_pos[0] += player_velocity[0]
    player_pos[1] += player_velocity[1]
    player_rect = p.Rect(player_pos[0], player_pos[1], *PLAYER_SIZE)

    # Collision detection
    on_ground = False
    for platform in platforms:
        if player_rect.colliderect(platform) and player_velocity[1] > 0:
            player_pos[1] = platform.top - PLAYER_SIZE[1]
            player_velocity[1] = 0
            jumping = False
            on_ground = True
            coyote_timer = COYOTE_TIME
            break

    # World boundaries
    if player_pos[1] > SCREEN_HEIGHT - PLAYER_SIZE[1]:
        player_pos[1] = SCREEN_HEIGHT - PLAYER_SIZE[1]
        player_velocity[1] = 0
        jumping = False
    player_pos[0] = max(0, min(player_pos[0], SCREEN_WIDTH - PLAYER_SIZE[0]))

    # Platform management
    for platform in platforms:
        platform.x -= scroll_speed
    platforms = [platform for platform in platforms if platform.right > 0]

    # Platform generation
    platform_timer += 1
    if platform_timer >= PLATFORM_INTERVAL:
        platform_timer = 0
        difficulty_timer += 1
        
        # Difficulty progression
        if difficulty_timer >= DIFFICULTY_INTERVAL:
            difficulty_timer = 0
            scroll_speed += DIFFICULTY_INCREMENT
            min_gap = max(50, MIN_GAP - 5)
            max_gap = max(100, MAX_GAP - 10)
            MIN_PLATFORM_WIDTH = max(80, MIN_PLATFORM_WIDTH - 5)

        # Generate new platform
        platform_width = random.randint(MIN_PLATFORM_WIDTH, MAX_PLATFORM_WIDTH)
        platform_y = last_platform_y + random.randint(-max_gap, max_gap)
        platform_y = max(100, min(platform_y, SCREEN_HEIGHT - 100))
        platforms.append(p.Rect(SCREEN_WIDTH, platform_y, platform_width, 20))
        last_platform_y = platform_y

    # Rendering
    WIN.fill(COLORS['SKY'])
    for platform in platforms:
        p.draw.rect(WIN, COLORS['PLATFORM'], platform)
    p.draw.rect(WIN, COLORS['PLAYER'], player_rect)
    p.display.flip()

p.quit()
