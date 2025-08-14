import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def count_primes_sync(limit):
    print(f"Counting primes up to {limit}...")
    primes = [n for n in range(limit) if is_prime(n)]
    print(f"Found {len(primes)} primes.")

async def count_primes_async(executor, limit):
    await asyncio.get_running_loop().run_in_executor(executor, count_primes_sync, limit)

async def main():
    start = time.time()
    with ThreadPoolExecutor() as executor:
        await asyncio.gather(
            
            count_primes_async(executor, 50000),
            count_primes_async(executor, 100000),
            count_primes_async(executor, 10000)
        )
    end = time.time()
    print(f"Total time: {end - start:.2f} seconds")

asyncio.run(main())