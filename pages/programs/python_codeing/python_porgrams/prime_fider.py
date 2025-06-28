import time

def is_prime(number, primes):
    for prime in primes:
        if prime * prime > number:
            break
        if number % prime == 0:
            return False
    return True

def prime_list(limit):
    if limit < 2:
        return []
    primes = [2, 3, 5, 7]
    for num in range(11, limit + 1, 2):
        if num % 10 in [1, 3, 7, 9] and is_prime(num, primes):
            primes.append(num)
            
    return [p for p in primes if p <= limit]

limit = 5000

start_time = time.time()
primes = prime_list(limit)
end_time = time.time()

print(f"Prime numbers up to {limit}:")
print(primes)
print(f"Time taken: {end_time - start_time:.6f} seconds")
