import time
import asyncio


def is_prime(x):
    return not any([x % i == 0 for i in range(x-1, 1, -1)])


async def highest_prime_below(x):
    print(f'Highest prime below {x}')
    for y in range(x-1, 0, -1):
        if is_prime(y):
            print(f'→ Highest prime below {x} is {y}')
            return y
        await asyncio.sleep(0.01)
    return None


async def main():
    t0 = time.time()
    
    tasks = [
        asyncio.create_task(highest_prime_below(700000)),
        asyncio.create_task(highest_prime_below(1000)),
        asyncio.create_task(highest_prime_below(10000))
        
    ]
    
    await asyncio.wait(tasks)
    
    t1 = time.time()
    print(f'Took {1000*(t1-t0):.2f} ms')


# Modern Python 3.7+ way
asyncio.run(main())
