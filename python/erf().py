from mpmath import erf as urf
from mpmath import mp

def erf(x, d):
    mp.dps = d
    result = urf(x)
    print(f"erf({x}) = {str(result)}")

