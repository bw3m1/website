from matplotlib import pyplot as plt
from time import time 

def draw(parameters):
        
    # unpack the parameters
    x, y, a = parameters
    
    # lists to store the entier path
    x_list = [x]
    y_list = [y]

    # itarativle pass (x,y) into the quadratic map
    for i in range(500000):
        
        # compute next point (using the quadratic map)
        xnew = a[0] + a[1]*x + a[2]*x*x + a[3]*y + a[4]*y*y + a[5]*x*y
        ynew = a[6] + a[7]*x + a[8]*x*x + a[9]*y + a[10]*y*y + a[11]*x*y
        x = xnew
        y = ynew
        x_list.append(x)
        y_list.append(y)


    # clear figur
    plt.clf()
    
    # plot design
    plt.style.use("dark_background")
    plt.axis("off")
    
    # create the plot
    plt.scatter(x_list[100:], y_list[100:], s= 0.01, c = "blue", linewidth = 0)
    
    # save the imig
    folder = 'C:\\Users\\Bryson\\Desktop\\atractor gallery'
    t = str(time())
    plt.savefig(folder + t + ".png", dpi=2500)

draw()