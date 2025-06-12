
from matplotlib import pyplot as plt


for i in range(26):
    x = i+1
    data_list= []

    if not (x == 2 or x == 4 or x == 1):
        while not (x == 1):
            
            data_list.append(x)
            
            if x %2 == 1:
                x = (3*x) + 1
            else: x = x/2
            data_list.append(1)
    
        print (data_list)
    
        plt.plot(data_list)
        plt.show()