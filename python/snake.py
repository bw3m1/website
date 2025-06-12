import pygame
import random
from heapq import heappop, heappush
from collections import deque

pygame.init()
display_width, display_height = 1500, 800
snake_speed = 7500
snake_block = 10
dis = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake Game')

def draw_snake(snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, (0, 255, 0), [x[0], x[1], snake_block, snake_block])

def a_star(start, goal, snake_list):
    directions = [(snake_block, 0), (-snake_block, 0), (0, snake_block), (0, -snake_block)]
    open_set, g_score, visited = [(0, start, [])], {start: 0}, {start}
    
    while open_set:
        _, current, path = heappop(open_set)
        if current == goal: 
            return path
        for dx, dy in directions:
            new_pos = (current[0] + dx, current[1] + dy)
            # Check if new position is in bounds and not occupied by the snake
            if (0 <= new_pos[0] < display_width and 0 <= new_pos[1] < display_height and
                new_pos not in visited and new_pos not in snake_list):
                new_g = g_score[current] + 1
                if new_pos not in g_score or new_g < g_score[new_pos]:
                    g_score[new_pos] = new_g
                    f_score = new_g + abs(goal[0] - new_pos[0]) + abs(goal[1] - new_pos[1])
                    heappush(open_set, (f_score, new_pos, path + [(dx, dy)]))
                    visited.add(new_pos)
    return None

def flood_fill(start, snake_list):
    directions = [(snake_block, 0), (-snake_block, 0), (0, snake_block), (0, -snake_block)]
    queue, visited = deque([start]), {start}
    while queue:
        x, y = queue.popleft()
        for dx, dy in directions:
            new_pos = (x + dx, y + dy)
            if (0 <= new_pos[0] < display_width and 0 <= new_pos[1] < display_height and
                new_pos not in visited and new_pos not in snake_list):
                queue.append(new_pos)
                visited.add(new_pos)
    return len(visited)

def auto_play(x, y, foodx, foody, snake_list):
    path = a_star((x, y), (foodx, foody), set(tuple(pos) for pos in snake_list))
    if path:
        next_pos = (x + path[0][0], y + path[0][1])
        if flood_fill(next_pos, snake_list) > len(snake_list): return path[0]
    return 0, 0

def gameLoop():
    x, y = display_width // 2, display_height // 2
    snake_list, length_of_snake, score, moves = [], 1, 0, 0
    foodx, foody = random_food(snake_list)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                return
        
        x_change, y_change = auto_play(x, y, foodx, foody, snake_list)
        next_x, next_y = x + x_change, y + y_change
        
        # Check if the next position is within bounds
        if not (0 <= next_x < display_width and 0 <= next_y < display_height):
            break
        
        x, y = next_x, next_y
        
        # Check for collision with boundaries or self
        if (x, y) in snake_list:
            break  # End the game if there's a collision
        
        dis.fill((5, 5, 5))
        pygame.draw.rect(dis, (255, 0, 0), [foodx, foody, snake_block, snake_block])
        snake_head = [x, y]
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Check if the snake has eaten the food
        if (x, y) == (foodx, foody):
            length_of_snake += 1
            score += 1
            foodx, foody = random_food(snake_list)  # Respawn food

        draw_snake(snake_list)
        
        # Display score and moves
        font = pygame.font.SysFont("arial", 20)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        moves_text = font.render(f"Moves: {moves}", True, (255, 255, 255))
        dis.blit(score_text, (10, 10))
        dis.blit(moves_text, (10, 40))
        
        pygame.display.update()
        pygame.time.Clock().tick(snake_speed)

    print(f'Score: {score}, Moves: {moves}')
    pygame.quit()

def random_food(snake_list):
    while True:
        foodx = round(random.randrange(0, display_width) / 10.0) * 10.0
        foody = round(random.randrange(0, display_height) / 10.0) * 10.0
        if (foodx, foody) not in snake_list:
            return foodx, foody

gameLoop()
