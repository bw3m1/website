import numpy as np
import time as t
from matplotlib import pyplot as plt

xL = 65
yL = 65
grid = np.zeros([xL,yL])
start_1 = int(0.30*xL*yL)
for i in range(start_1):
    x = np.random.randint(0,xL)
    y = np.random.randint(0,yL)
    grid[x,y]=1
plt.imshow(grid, cmap='binary')
def num_neighbors(x,y,grid):
    n=0
    for i in range(x-1,x+2):
        for j in range(y-1,y+2):
            if i>=0 and j>=0 and i < np.shape(grid)[0] and j < np.shape(grid)[1]:
                if grid[i,j]==1:
                    if not(i==x and j==y): n=n+1
    return n
def update_grid(grid):
    new_grid=0*grid
    for y in range(yL):
        for x in range(xL):
            num = num_neighbors(x,y,grid)
            if num == 2 : new_grid[x,y]=grid[x,y]
            elif num == 3: new_grid[x,y]=1
            else: new_grid[x,y]=0
    return new_grid

time_fraktion=80
seconds=5

for i in range((seconds*time_fraktion)):
    grid = update_grid(grid)
    plt.imshow(grid, cmap='binary')
    plt.show()
    t.sleep(1/time_fraktion)