import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

# Parameters
grid_size = 150
num_particles = 3500
center = grid_size // 2
sigma = 1  # Standard deviation for Gaussian smoothing

# Initialize grid with a central seed particle
grid = np.zeros((grid_size, grid_size), dtype=bool)
grid[center, center] = True

def biased_random_walk():
    # Start from a random edge
    edge = np.random.choice(["top", "bottom", "left", "right"])
    
    if edge == "top":
        x, y = np.random.randint(0, grid_size), 0
    elif edge == "bottom":
        x, y = np.random.randint(0, grid_size), grid_size - 1
    elif edge == "left":
        x, y = 0, np.random.randint(0, grid_size)
    elif edge == "right":
        x, y = grid_size - 1, np.random.randint(0, grid_size)

    # Random walk until an adjacent cell is occupied
    while True:
        direction = np.random.choice(['up', 'down', 'left', 'right'])
        
        if direction == 'up' and y > 0:
            y -= 1
        elif direction == 'down' and y < grid_size - 1:
            y += 1
        elif direction == 'left' and x > 0:
            x -= 1
        elif direction == 'right' and x < grid_size - 1:
            x += 1

        # Check if particle is adjacent to an occupied cell
        if (grid[max(0, x-1):min(grid_size, x+2), max(0, y-1):min(grid_size, y+2)].any()):
            grid[x, y] = True
            break

# Run simulation
plt.figure(figsize=(8, 8))
for i in range(num_particles):
    biased_random_walk()
    if i % 5 == 0:
        modified_grid = grid.astype(float) * 2  # Multiply by 2
        smoothed_grid = gaussian_filter(modified_grid, sigma=2)  # Apply Gaussian filter
        plt.imshow(smoothed_grid, cmap='magma', interpolation='nearest')
        plt.axis('off')
        plt.pause(0.1 / 20)  # Smoother updates

# Final visualization after all particles have been added
modified_grid = grid.astype(float) * 2  # Multiply by 2 for final display
smoothed_grid = gaussian_filter(modified_grid, sigma=2)  # Apply Gaussian filter
plt.imshow(smoothed_grid, cmap='magma', interpolation='nearest')
plt.axis('off')
plt.show()
