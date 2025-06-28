import hashlib as hs

def hashP(p):
    t = str(p)
    h = hs.sha512()
    h.update(t.encode('utf-8'))
    c = int(h.hexdigest(), 16)  # Convert the hexadecimal digest to an integer
    return c

z = input('Enter a int:  ')
q = 0
p = []
while q < 255:
    q -= 1
    for i in range(32):
        q += 1
        z = hashP(z)
        j = z % 16
        if j < 4:
            break
        p.append(j)
print(p)