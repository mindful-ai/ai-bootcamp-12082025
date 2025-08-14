

import time
import asyncio


def is_prime(x):
    return not any([x % i == 0 for i in range(x-1, 1, -1)])


async def highest_prime_below(x):

    print('Highest prime below %d' % x)
    for y in range(x-1, 0, -1):
        if is_prime(y):
            print('→ Highest prime below %d is %d' % (x, y))
            return y
        await asyncio.sleep(0.01)
    return None


async def main():

    t0 = time.time()
    await asyncio.wait( [
        highest_prime_below(700000),
        highest_prime_below(10000),
        highest_prime_below(1000)
        ] )
    t1 = time.time()
    print('Took %.2f ms' % (1000*(t1-t0)))


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
#loop.close()
