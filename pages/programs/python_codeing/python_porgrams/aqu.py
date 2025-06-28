import matplotlib.pyplot as plt

def aqu(s, l, lc):
    def pr(n):
        if n <= 1:
            return []
        d = [1]
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                d.append(i)
                if i != n // i: d.append(n // i)
        return d
    s, se = [s], {}
    for _ in range(l - 1):
        n = sum(pr(s[-1]))
        s.append(n)
        se[n] = se.get(n, 0) + 1
        if se[n] >= lc:
            s[-1] = f"{n}, terminated duw to loop"
            break
        if n == 0:
            s[-1] = f"{n}, terminated"
            break
    sstr = [str(num) for num in s]
    return s, sstr
def plot(s, t):
    plt.figure(figsize=(10, 5))
    plt.plot(s, marker='o')
    plt.title(t)
    plt.xlabel('Term Index')
    plt.ylabel('Term Value')
    plt.grid(True)
    plt.show()

loop_cicles = 3
start_number = 2856
sequence_length = 250
sequence, sequence_str = aqu(start_number, sequence_length, loop_cicles)
print(f"Aliquot({start_number}): [{', '.join(sequence_str)}]\n")
print(f"Sequence length: {len(sequence)}")
mx = max(int(s.split()[0])for s in sequence_str if s.split()[0].isdigit())
print(f"Maximum value in the sequence: {mx}")
plot([int(s.split()[0]) for s in sequence_str if s.split()[0].isdigit()],
     f"Aliquot Sequence Starting from {start_number} with length {len(sequence)}")