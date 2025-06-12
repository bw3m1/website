import hashlib as n

def h(string): return int(n.sha256(str(string).encode('utf-8')).hexdigest(), 16)
def w(sizes): return {chr(32 + i): bin(h(chr(32 + i)))[2:].zfill(sizes[i % len(sizes)])[:sizes[i % len(sizes)]] for i in range(95)}
def t(lookup, text): return ''.join(lookup.get(c, '?') for c in text)
def y(binary_string): return ''.join([{f'{i:08b}': chr(i) for i in range(32, 127)}.get(binary_string[i:i + 8], '?') for i in range(0, len(binary_string) - (len(binary_string) % 8), 8)]) + ('§' + binary_string[-(len(binary_string) % 8):] if len(binary_string) % 8 != 0 else '')

z, x = input('Enter your encryption key: '), []
while len(x) < 95: j = h(z) % 16; x.append(j) if j >= 5 else None; z = h(z)
print(y(t(w(x), input("Enter the string you want to hash: "))))
