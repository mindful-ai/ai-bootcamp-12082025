# ThreadPoolExecutor in Python — Detailed Guide

## 1. What is ThreadPoolExecutor?
`ThreadPoolExecutor` is part of Python’s `concurrent.futures` module and provides a **high-level interface** for running functions in multiple threads.

Instead of manually managing threads (`threading.Thread`), you can submit tasks to a **pool of worker threads** and retrieve their results easily.

---

## 2. Purpose
- Run **blocking or I/O-bound** code concurrently without freezing the main program.
- Limit the number of concurrent threads (`max_workers`).
- Retrieve results using **Future objects**.
- Integrates well with **asyncio** to run blocking functions in threads.

---

## 3. When to Use
- ✅ **I/O-bound** tasks: file operations, HTTP requests, database queries.
- ❌ **CPU-bound** tasks: prefer `ProcessPoolExecutor` due to Python’s GIL.

---

## 4. Basic Example

```python
from concurrent.futures import ThreadPoolExecutor
import time

def task(name):
    print(f"Starting {name}")
    time.sleep(2)  # Simulate blocking I/O
    print(f"Finished {name}")
    return f"Result from {name}"

# Create a pool with 3 worker threads
with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(task, f"Task-{i}") for i in range(5)]

    for future in futures:
        print(future.result())  # Wait for completion and get result
```

**How it works:**
- `max_workers=3` → at most 3 tasks run at the same time.
- `executor.submit(func, *args)` schedules a function to run in a thread.
- Returns a **Future** object, whose `.result()` blocks until the function finishes.

---

## 5. Using `map()` for Simpler Syntax

```python
with ThreadPoolExecutor(max_workers=3) as executor:
    results = executor.map(task, [f"Task-{i}" for i in range(5)])
    for result in results:
        print(result)
```

`map()` runs tasks in parallel and returns results in the same order as the input.

---

## 6. With Asyncio

`asyncio` is single-threaded by default. Use `ThreadPoolExecutor` to run blocking code without freezing the event loop.

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time

def blocking_task():
    time.sleep(2)  # Blocking I/O
    return "Done"

async def main():
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, blocking_task)
        print(result)

asyncio.run(main())
```

---

## 7. Key Points
- **Thread-safety**: Functions you run must be safe to call from multiple threads.
- **Task Queuing**: Extra tasks wait until a worker thread is free.
- **Graceful Shutdown**: Using `with ThreadPoolExecutor()` ensures threads are cleaned up.

---

## 8. Summary Table

| Feature | ThreadPoolExecutor | ProcessPoolExecutor |
|---------|-------------------|---------------------|
| Best for | I/O-bound | CPU-bound |
| Uses threads? | ✅ Yes | ❌ No — uses processes |
| Avoids GIL? | ❌ No | ✅ Yes |
| Startup cost | Low | Higher |
