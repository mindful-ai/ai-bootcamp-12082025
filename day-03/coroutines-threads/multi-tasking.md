# Multitasking in Computing — A Clear Guide

## 1. What is Multitasking?
Multitasking is the ability of an operating system (OS) to run **multiple tasks (processes or threads) seemingly at the same time**.

💡 **Analogy:** Think of a chef cooking multiple dishes by rapidly switching between them — chopping vegetables, stirring soup, checking the oven — even though the chef can only do one action at any instant.

---

## 2. Types of Multitasking

### a) Preemptive Multitasking
- The **OS scheduler** decides when to switch tasks.
- Each task gets a **time slice** of CPU.
- Example: Windows, Linux, macOS.
- Prevents any single program from monopolizing CPU time.

**Example analogy:** A teacher calling on each student for a few seconds before moving to the next.

---

### b) Cooperative Multitasking
- Each task **voluntarily yields** control so others can run.
- If a task never yields, it can freeze the system.
- Example: Early Mac OS, Windows 3.x.

**Example analogy:** Two people sharing a chess clock — one must hit the clock to let the other play.

---

## 3. How Multitasking Works
1. **Context Switching**  
   - The OS saves the current task's state (registers, memory pointers).
   - Loads the next task's saved state.
2. **Scheduler**  
   - Decides which task gets CPU next.
3. **Concurrency vs Parallelism**
   - **Concurrency:** Multiple tasks *making progress* at once (via switching).
   - **Parallelism:** Tasks *actually running simultaneously* (requires multiple CPU cores).

---

## 4. Types of Workloads
| Workload Type | Description | Best Tool in Python |
|---------------|-------------|---------------------|
| I/O-bound | Waiting on input/output (disk, network, user input) | Threads / Async IO |
| CPU-bound | Heavy computation keeping CPU busy | Processes |

---

## 5. Multitasking in Python

### Example with Threads (I/O-bound simulation)
```python
import threading
import time

def task(name):
    for i in range(3):
        print(f"{name} working...")
        time.sleep(1)

t1 = threading.Thread(target=task, args=("Task 1",))
t2 = threading.Thread(target=task, args=("Task 2",))

t1.start()
t2.start()

t1.join()
t2.join()

print("All tasks done.")
```

### Visual Diagram

Time --->

Task 1: |====|    |====|    |====|
Task 2:    |====|    |====|    |====|

(Each bar represents a time slice of CPU usage.)
