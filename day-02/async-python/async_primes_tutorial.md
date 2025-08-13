# Async in Python: Prime Number Example

## 1. What is Async?
In Python, **async** and **await** are used for asynchronous programming — a way to run tasks without blocking each other while waiting for something slow to happen.

Async is ideal for **I/O-bound** tasks (network requests, file I/O, database queries), not **CPU-bound** work.

---

## 2. Example — Without Async (Sequential)
```python
import time

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def count_primes(limit):
    print(f"Counting primes up to {limit}...")
    start = time.time()
    primes = [n for n in range(limit) if is_prime(n)]
    end = time.time()
    print(f"Found {len(primes)} primes in {end - start:.2f} seconds.")

def main():
    start = time.time()
    count_primes(100_000)
    count_primes(100_500)
    count_primes(101_000)
    end = time.time()
    print(f"Total time: {end - start:.2f} seconds")

main()
```

**Behavior:**  
- Runs one after the other.  
- Total time ≈ sum of all runs.

---

## 3. Example — With Async (Still CPU-bound)
```python
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
        count_primes(100_000),
        count_primes(100_500),
        count_primes(101_000)
    )
    end = time.time()
    print(f"Total time: {end - start:.2f} seconds")

asyncio.run(main())
```

**Behavior:**  
- Even with `asyncio.gather`, total time ≈ sequential.  
- Why? CPU-bound work doesn’t yield to the event loop.

---

## 4. Fix for CPU-bound Work — Thread Pool
```python
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
            count_primes_async(executor, 100_000),
            count_primes_async(executor, 100_500),
            count_primes_async(executor, 101_000)
        )
    end = time.time()
    print(f"Total time: {end - start:.2f} seconds")

asyncio.run(main())
```

**Behavior:**  
- Now tasks run in parallel threads.  
- Total time ≈ the longest single task.

---

## 5. Key Teaching Point
| Work type | Async helps? | Why? |
|-----------|--------------|------|
| I/O-bound | ✅ Yes | Can switch tasks while waiting for I/O |
| CPU-bound | ❌ No* | CPU keeps working, never yields control |
| CPU-bound with threads/processes | ✅ Yes | Real parallelism avoids blocking |
