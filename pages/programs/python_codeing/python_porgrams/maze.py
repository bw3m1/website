import random
import matplotlib.pyplot as plt
import numpy as np
lx = int(input("Enter an integer: "))
if lx % 2 == 0:
    lx += 1
ly = lx
def generate_maze(width, height):
    maze = [['#'] * width for _ in range(height)]
    def carve(cx, cy):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = cx + dx * 2, cy + dy * 2
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == '#':
                if (0 <= cx + dx < width and 0 <= cy + dy < height and maze[cy + dy][cx + dx] == '#'):
                    maze[cy + dy][cx + dx] = ' '
                    maze[ny][nx] = ' '
                    carve(nx, ny)
    maze[1][1] = ' '
    carve(1, 1)
    maze[0][1] = ' '
    maze[height-1][width-2] = ' '
    return maze
def find_path(maze):
    height, width = len(maze), len(maze[0])
    start, end = (1, 0), (height - 2, width - 1)
    stack, visited = [(start, [start])], set()
    while stack:
        (cx, cy), path = stack.pop()
        plot_maze(maze, path)
        if (cx, cy) == end:
            return path
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == ' ' and (nx, ny) not in visited:
                visited.add((nx, ny))
                stack.append(((nx, ny), path + [(nx, ny)]))
    return []
def plot_maze(maze, path):
    height, width = len(maze), len(maze[0])
    maze_array = np.zeros((height, width, 3))
    for y in range(height):
        for x in range(width):
            if maze[y][x] == '#':
                maze_array[y, x] = [0, 0, 0]
            else:
                maze_array[y][x] = [1, 1, 1]
    for (x, y) in path:
        maze_array[y, x] = [0.5, 0.5, 0.5]
    plt.imshow(maze_array)
    plt.xticks([]), plt.yticks([])
    plt.show()
if __name__ == "__main__":
    width, height = lx, ly
    maze = generate_maze(width, height)
    path = find_path(maze)
    plot_maze(maze, path)