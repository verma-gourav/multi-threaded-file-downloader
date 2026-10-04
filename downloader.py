# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///

import random
import threading
import time

stats = {"total": 0, "complete": 0, "failed": 0}
results = []

def download_with_shared_stats(file_name: str, stats: dict, results: list) -> None:
    """Demonstrate unsafe modification of shared mutable data"""

    thread = threading.current_thread().name

    # UNSAFE: Multiple threads can modify stats at the same time
    stats["total"] += 1
    print(f"[{thread}] Starting {file_name}")

    try:
        # Simulate download with random duration failure
        time.sleep(random.uniform(1, 2))
        if random.random() < 0.3:
            raise RuntimeError("Network error")

        # UNSAFE: Race condition when updating shared data
        stats["complete"] += 1
        results.append(f"{file_name} success")
        print(f"[{thread}] Completed {file_name}")

    except RuntimeError as err:
        # UNSAFE: Another race condition
        stats["failed"] += 1
        results.append(f"{file_name} failed: {err}")
        print(f"[{thread}] Failed {file_name}")

def demonstrate_dangerous() -> None:
    """Show how shared mutable data leads to race conditions"""

    print("--- Dangerous: sharing mutable data ---")

    files = ["file1.zip", "file2.zip", "file.mp4"]

    # Create threads that all modify the same shared data
    threads = [
        threading.Thread(target=download_with_shared_stats,
            args=(f, stats, results)) for f in files
    ]

    # Start and wait for all threads
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("\n --- Results (may be corrupted) ---")
    print("Stats:", stats)
    print("Results list length:", len(results))

if __name__ == "__main__":
    demonstrate_dangerous()
