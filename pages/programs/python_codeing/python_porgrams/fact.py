
def fact(x):
    flist = [1]
    for i in range(x):
        a = flist[i] * (i+1)
        flist.append(a)
    return flist[x]

for x in range(1560):
    print(f"{x}! = {fact(x)}")