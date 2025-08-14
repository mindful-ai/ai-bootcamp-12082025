# Asyncio in Python — Detailed Guide

## 1. What Async Actually Means
In Python, `async`/`await` allows **concurrent execution** without multiple threads, by **cooperatively multitasking** between coroutines.

- **Normal (sync) execution**: Function runs start-to-finish; nothing else runs until it returns.
- **Async execution**: Functions (`coroutines`) *yield control* when they reach an `await`, letting other coroutines run.
- **Event loop**: A scheduler that runs and switches between these coroutines.

It’s not *parallelism* (unless you mix in threads/processes), but **concurrency**: tasks *overlap* in time, often during I/O waits.

---

## 2. Key Terms
| Term | Meaning |
|------|---------|
| **Coroutine** | A special function defined with `async def` that can be paused/resumed. |
| **Awaitable** | Something you can `await` (coroutines, asyncio Tasks, or objects with `__await__`). |
| **Event loop** | The core engine that schedules and runs coroutines. |
| **Task** | A coroutine wrapped in a way that it can run concurrently with others. |
| **Future** | Low-level object representing a result that will be available later. |

---

## 3. Timing — How Async Saves Time
Imagine you have three tasks:
- **Task A**: Wait 2 seconds (API request)
- **Task B**: Wait 3 seconds (Database query)
- **Task C**: Wait 1 second (File read)

### Synchronous
```python
import time

def blocking_task(t):
    time.sleep(t)
    return f"Done after {t}s"

start = time.time()
blocking_task(2)
blocking_task(3)
blocking_task(1)
end = time.time()

print(f"Total time: {end - start:.2f} seconds")
```
**Total time ≈ 2 + 3 + 1 = 6s**

---

### Asynchronous
```python
import asyncio

async def async_task(t):
    await asyncio.sleep(t)
    return f"Done after {t}s"

async def main():
    start = asyncio.get_event_loop().time()
    results = await asyncio.gather(
        async_task(2),
        async_task(3),
        async_task(1)
    )
    end = asyncio.get_event_loop().time()

    print(results)
    print(f"Total time: {end - start:.2f} seconds")

asyncio.run(main())
```
**Total time ≈ max(2, 3, 1) = 3s**

---

## 4. Measuring Time Properly in Async
- **`time.time()`** — wall-clock time, affected by system clock changes.
- **`asyncio.get_event_loop().time()`** — monotonic time, unaffected by clock adjustments.

---

## 5. Important Aspects

### I/O-bound vs CPU-bound
- Async **shines** for I/O waits — HTTP requests, reading files, database queries.
- For CPU-heavy work (e.g., prime number crunching), async alone doesn’t help — use threads or multiprocessing.

### Concurrency Control
```python
semaphore = asyncio.Semaphore(5)

async def limited_task(i):
    async with semaphore:
        await asyncio.sleep(2)
        print(f"Task {i} done")
```

### Error Handling
```python
try:
    await async_task(2)
except Exception as e:
    print("Error:", e)
```

### Cancellation
```python
task = asyncio.create_task(async_task(10))
await asyncio.sleep(2)
task.cancel()
```

---

## 6. Common Pitfalls
- **Mixing sync blocking calls** (`time.sleep`) inside async functions freezes everything.
- **Forgetting to await** means coroutine never runs.
- **Expecting parallel CPU work** — needs threads/processes.

---

## 7. Summary Table

| Work type | Async helps? | Why? |
|-----------|--------------|------|
| I/O-bound | ✅ Yes | Can switch tasks while waiting for I/O |
| CPU-bound | ❌ No* | CPU keeps working, never yields control |
| CPU-bound with threads/processes | ✅ Yes | Real parallelism avoids blocking |
