import pygame
import numpy as np
import sys

# Constants
WIDTH, HEIGHT = 1500, 800  # Window size
GRID_SIZE = 75  # Number of cells along each dimension
CELL_SIZE = WIDTH // GRID_SIZE  # Size of each cell

# Colors
ALIVE_COLOR = (200, 200, 0)
DEAD_COLOR = (5, 5, 5)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life")

# Initialize grid
grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

def update_grid(grid):
    """Applies the rules of Conway's Game of Life to update the grid."""
    new_grid = grid.copy()
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            # Count alive neighbors
            alive_neighbors = np.sum(grid[max(0, row-1):min(GRID_SIZE, row+2), 
                                          max(0, col-1):min(GRID_SIZE, col+2)]) - grid[row, col]
            # Apply the rules of Game of Life
            if grid[row, col] == 1:  # Alive cell
                if alive_neighbors < 2 or alive_neighbors > 3:
                    new_grid[row, col] = 0  # Dies
            else:  # Dead cell
                if alive_neighbors == 3:
                    new_grid[row, col] = 1  # Comes to life
    return new_grid

def draw_grid(screen, grid):
    """Draws the cells on the screen."""
    screen.fill(DEAD_COLOR)  # Fill screen with dead color
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = ALIVE_COLOR if grid[row, col] == 1 else DEAD_COLOR
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Main game loop
running = True
paused = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Pause/unpause with space
                paused = not paused
            elif event.key == pygame.K_c:  # Clear the grid with 'c'
                grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
            elif event.key == pygame.K_r:  # Randomize grid with 'r'
                grid = np.random.randint(2, size=(GRID_SIZE, GRID_SIZE))  # Randomize cells
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle cell state on click
            x, y = pygame.mouse.get_pos()
            col, row = x // CELL_SIZE, y // CELL_SIZE
            grid[row, col] = 1 - grid[row, col]  # Toggle between alive and dead

    if not paused:
        grid = update_grid(grid)

    draw_grid(screen, grid)
    pygame.display.flip()
    clock.tick(10)  # Control the speed of the simulation

pygame.quit()
sys.exit()