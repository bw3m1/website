import random as r
from matplotlib import pyplot as plt
import math
from time import time 

def serch_attractors(n):
    
    found = 0
    while found < n:
        
        # random starting point
        x = r.uniform(-0.5,0.5)
        y = r.uniform(-0.5,0.5)
        
        # random alternative point nerby
        xe = x + r.uniform(-0.5,0.5) / 1000
        ye = y + r.uniform(-0.5,0.5) / 1000
        
        # distance between the two points
        dx = xe - x
        dy = ye - y
        d0 = math.sqrt(dx * dx + dy * dy)
        
        # random parameter vector
        a = [r.uniform(-2,2) for i in range(12)]
        
        # lists to store the entier path
        x_list = [x]
        y_list = [y]
        
        # initialize convergence boolean and lyapunov exponent
        converging = False
        lyapunov = 0
        
        # itarativle pass (x,y) into the quadratic map
        for i in range(10000):
            
            # compute next point (using the quadratic map)
            xnew = a[0] + a[1]*x + a[2]*x*x + a[3]*y + a[4]*y*y + a[5]*x*y
            ynew = a[6] + a[7]*x + a[8]*x*x + a[9]*y + a[10]*y*y + a[11]*x*y
            
            # check if we diverg to infinaty
            if abs(xnew) > 1e10 or abs(ynew) > 1e10:
                converging = True
                break
            
            # check if we converg to a single point
            if abs(x-xnew) < 1e-10 and abs(y-ynew) < 1e-10:
                converging = True
                break
            
            #check for chaotic behavior
            if i > 1000:
                
                # compute next alternative point
                xenew = a[0] + a[1]*xe + a[2]*xe*xe + a[3]*ye + a[4]*ye*ye + a[5]*xe*ye
                # comput the distins between the new points
                yenew = a[6] + a[7]*xe + a[8]*xe*xe + a[9]*ye + a[10]*ye*ye + a[11]*xe*ye
                
                dx = xenew - xnew
                dy = yenew - ynew
                d = math.sqrt(dx * dx + dy * dy)
                
                # lyapunov exponent
                lyapunov += math.log(abs(d/d0))
            
                # rescale the alternative point
                xe = xnew + d0*dx/d
                ye = ynew + d0*dy/d
            
            # update (x,y)
            x = xnew
            y = ynew
        
            # stor (x,y) in our path lists
            x_list.append(x)
            y_list.append(y)
        
        # if chaotic behavior has been found
        if (not converging) and lyapunov >= 50:
            found += 1

            # clear figur
            plt.clf()
            
            # plot design
            plt.style.use("dark_background")
            plt.axis("off")
            
            # create the plot
            plt.scatter(x_list[100:], y_list[100:], s= 0.1, c = "white", linewidth = 0)
            
            # save the imig
            folder = 'C:\\Users\\Bryson\\Desktop\\atractors\\'
            t = str(time())
            plt.savefig(folder + str(t) + 'e' + ".png", dpi=250)
            
            # save the parameters
            parameters = (x_list[0], y_list[0], a)
            file = open(folder + str(t) + 'e' + ".txt", "w+")
            file.write(str(parameters))

serch_attractors(50)