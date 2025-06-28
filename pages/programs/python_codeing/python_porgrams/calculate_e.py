import decimal as dc
import time as t_

precision = int(input("Enter the number of digits of e: ")) + 1
dc.getcontext().prec = precision

def e():
    e_approx = dc.Decimal(1)
    term = dc.Decimal(1)
    t = 1
    convergence_threshold = dc.Decimal(1) / (10 ** (precision + 1))
    while True:
        term /= t
        e_approx += term
        if abs(term) < convergence_threshold: break
        t += 1
    return e_approx, t
st = t_.time()
e, f = e()
et = t_.time() - st
print(f"n/Approximation of e: {e}")
print(f"Number of terms used: {f}")
print(f"Execution time: {et:.10f} seconds")
