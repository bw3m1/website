import sys

k = [0, 1]
o = int(input(f"wich fibanochi number do you wont to comput:\n\n"))
for i in range(o-1):
    g = k[i] + k[i+1]
    k.append(g)
sys.set_int_max_str_digits(o+640)

print(f"\n{k[o]}")
