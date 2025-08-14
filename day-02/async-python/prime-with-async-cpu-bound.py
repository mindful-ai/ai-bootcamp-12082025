import asyncio
import time

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

async def count_primes(limit):
    print(f"Counting primes up to {limit}...")
    start = time.time()
    primes = [n for n in range(limit) if is_prime(n)]
    end = time.time()
    print(f"Found {len(primes)} primes in {end - start:.2f} seconds.")

async def main():
    start = time.time()
    await asyncio.gather(
        
        count_primes(50000),
        count_primes(100000),
        count_primes(10000)
    )
    end = time.time()
    print(f"Total time: {end - start:.2f} seconds")

asyncio.run(main())