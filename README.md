# Multi-Threaded File Downloader Simulation

Implementation of Multithreading in Python **[https://roadmap.sh/python/multithreading]**

---

## Files

- **`downloader.py`**: Iterative core simulation tracking sequential runs, manual `threading.Thread` deployments, custom thread subclassing, error handling, and thread-safety execution parameters using `threading.Lock`.

- **`download_manager_locks.py`**: Demonstration of **Recursive/Reentrant Locks (`threading.RLock`)**.

- **`download_deadlock.py`**: Exploration of thread lock contention and **Dining Philosophers circular deadlocks** resolved using randomized timeout-backoff.

- **`download_monitor.py`**: Implementation of **Daemon Threads** featuring a background monitor and heartbeat mechanism that gracefully exits automatically when primary operational threads complete.

- **`download_queue.py`**: Implementation of the **Producer-Consumer pipeline** utilizing thread-safe `queue.Queue` structures to distribute tasks to persistent workers concurrently.

- **`download_thread_pool.py`**: The final modern implementation refactoring low-level structures into high-level abstract **`ThreadPoolExecutor`** task allocation channels.

---

## Execution

The environment utilizes **`uv`** for lightweight runtime optimization. You can execute any module independently within isolated contexts:

```bash
uv run downloader.py
uv run download_thread_pool.py
```
