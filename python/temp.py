import pygame as p
import random

p.init()

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 837
WIN = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
p.display.set_caption("Infinite Platformer")

# Colors
background_color = (135, 206, 235)  # Sky blue
player_color = (255, 0, 0)  # Red
platform_color = (0, 128, 0)  # Green

# Player settings
player_pos = [400, 500]
player_size = [16, 16]
player_velocity = [0, 0]
speed = 20
gravity = 0.3
jump_strength = 12
jumping = False

# Platforms
platforms = [p.Rect(0, 700, SCREEN_WIDTH + 100, 129)]  # Start with a ground platform
scroll_speed = 2  # Speed at which platforms scroll left
platform_timer = 0  # Timer to regulate platform generation
platform_interval = 100

# Game loop
running = True
clock = p.time.Clock()

while running:
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
        if event.type == p.KEYDOWN:
            if event.key == p.K_a:  # Move left
                player_velocity[0] = -speed
            if event.key == p.K_d:  # Move right
                player_velocity[0] = speed
            if event.key == p.K_SPACE and not jumping:  # Jump
                jumping = True
                player_velocity[1] = -jump_strength
        if event.type == p.KEYUP:
            if event.key in [p.K_a, p.K_d]:
                player_velocity[0] = 0

    # Apply gravity
    player_velocity[1] += gravity

    # Update player position
    player_pos[0] += player_velocity[0]
    player_pos[1] += player_velocity[1]

    # Collision detection
    player_rect = p.Rect(player_pos[0], player_pos[1], *player_size)
    on_ground = False
    for platform in platforms:
        if player_rect.colliderect(platform) and player_velocity[1] > 0:
            player_pos[1] = platform.top - player_size[1]
            player_velocity[1] = 0
            jumping = False
            on_ground = True
            break

    # Prevent player from falling below screen
    if not on_ground and player_pos[1] > SCREEN_HEIGHT - player_size[1]:
        player_pos[1] = SCREEN_HEIGHT - player_size[1]
        player_velocity[1] = 0
        jumping = False

    # Prevent player from moving off-screen horizontally
    player_pos[0] = max(50, min(player_pos[0], SCREEN_WIDTH - player_size[0]))

    # Scroll platforms left
    for platform in platforms:
        platform.x -= scroll_speed

    # Remove platforms that go off-screen
    platforms = [platform for platform in platforms if platform.right > 0]

    # Generate new platforms
    ferst_p = True
    platform_timer += 1
    platform_y = 100
    if platform_timer >= platform_interval:
        platform_timer = 0
        platform_width = random.randint(100, 200)
        platform_height = 20
        platform_x = SCREEN_WIDTH
        platform_y += random.randint(300, 600)
        platforms.append(p.Rect(platform_x, platform_y, platform_width, platform_height))

    # Draw everything
    WIN.fill(background_color)
    p.draw.rect(WIN, player_color, player_rect)
    for platform in platforms:
        p.draw.rect(WIN, platform_color, platform)

    # Update display
    p.display.flip()
    clock.tick(60)

p.quit()
