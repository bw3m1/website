import hashlib

def h(s): 
    return ''.join(format(byte, '08b') for byte in hashlib.sha256(s.encode()).digest())

def ByC(Ptxt): 
    return ''.join(format(ord(char), '08b') for char in Ptxt)

def ToString(binary_data):
    return ''.join(chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8))

def XOR(A, B):
    if len(A) < len(B): 
        A = A.ljust(len(B), '0')
    return ''.join(str(int(a) ^ int(b)) for a, b in zip(A, B))

def crypt(T, K, E=True):
    if E:
        keys = [K]
        for _ in range(2):
            K = h(K)
            keys.append(K)
        X = T
        for key in keys:
            X = XOR(X, key)
        return X, keys
    elif not E:
        X = T
        for key in reversed(keys):
            X = XOR(X, key)
        return X

Ptxt = ByC(input("Input the plaintext: "))
Key = ByC(input("Input the key: "))
Cipher, Keys = crypt(Ptxt, Key)
print("Cipher (Binary):", Cipher)
print("Decrypted (Text):", ToString(crypt(Cipher, Key, False)))
