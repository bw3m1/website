import numpy as np
import matplotlib.pyplot as plt
D = np.random.randint(0,10,[10,10])

def avr(D):
    A = np.copy(D)
    for x in range(np.shape(D)[0]):
        for y in range(np.shape(D)[1]):
            
            if x ==0:
                xind = [0,1]
            elif x == np.shape(D)[0]-1:
                xind = [-1,0]
            else:
                xind = [-1,0,1]
           
            if y ==0:
                 yind = [0,1]
            elif y == np.shape(D)[0]-1:
                 yind = [-1,0]
            else:
                yind = [-1,0,1]

            for xi in xind:
                for yi in yind:
                    A[x,y] += D[xi+x,yi+y]
                    
            A[x,y] =A[x,y]/(len(xind)*len(yind))
            
    return A



#retern valus
x = np.arange(0,np.shape(D)[0])
y = np.arange(0,np.shape(D)[0])
X,Y = np.meshgrid(x,y)



ax1 = plt.axes(projection ='3d')
ax1.plot_surface(X, Y, D)

A = avr(D)
ax1 = plt.axes(projection ='3d')
ax1.plot_surface(X, Y, A)

