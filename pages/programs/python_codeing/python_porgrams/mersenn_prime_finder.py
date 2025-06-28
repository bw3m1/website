from sympy import primerange
from time import time

def LLT(p):
    if p == 2: return True
    s = 4
    M_p = (1 << p) - 1
    for _ in range(p - 2): s = (s * s - 2) % M_p
    return s == 0

def M_p(limit):
    for p in primerange(2, limit):
        t_0 = time()
        if LLT(p):
            num_digits = len(str((2**p)-1))
            t = time() - t_0
            print(f"New Mersenne Prime Found: 2^{p} - 1, which has {num_digits} digits")
            print(f"this prime tuck {t} seconds of computation time \n")
            

limit = 10000
M_p(limit) 