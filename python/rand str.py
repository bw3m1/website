import hashlib as h
import decimal as dc

def pi(seed, lanth):
    dc.getcontext().prec = lanth + 100
    y = []
    for i in range(lanth):
        try:
            seed = int.from_bytes(h.sha256(str(seed).encode()).digest(), byteorder='big')
            hex_digest = hex(seed)[2:]
            if len(hex_digest) < lanth:
                hex_digest = hex_digest.zfill(lanth)
            decimal_value = sum(dc.Decimal(int(hex_digit, 16)) / dc.Decimal(16 ** (i + 1)) for i, hex_digit in enumerate(hex_digest[:lanth]))
            y.append(decimal_value)
        except Exception as e:
            print(f"Error in iteration {i}: {e}")
            break
    final_value = sum(y) * 10**(622 + lanth)
    return final_value


v = pi(5, 500)  # Use a seed of 5, and iterate 500 times
print("Decimal Value:", v)
