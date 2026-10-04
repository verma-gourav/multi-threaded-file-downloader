# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///

import random
import threading
import time


def download_with_options(file_id: int, file_name: str, size_mb: int = 1, priority: str = "normal", max_retries: int = 3) -> None:
    """Simulate downloading a file with various options and retry logic"""

    thread = threading.current_thread().name
    print(f"[{thread}] Download {file_id}: {file_name} ({size_mb}MB, {priority})")

    # Calculate download time based on size and priority
    base_time = size_mb * 0.3
    if priority == "high":
        base_time *= 0.7  # higher priority downloads faster
    if priority == "low":
        base_time *= 1.3  # lowe priority downloads slower

    # Retry logic with simulated failures
    for attempt in range(1, max_retries + 1):
        try:
            print(f"[{thread}] Attempt {attempt} for {file_name}")
            time.sleep(base_time)  # simulate download time

            # Simulate random network failure on first attempt
            if attempt == 0 and random.random() < 0.2:
                raise RuntimeError("Network timeout")

            print(f"[{thread}] Downloaded {file_name} successfully")
            return

        except RuntimeError as err:
            print(f"[{thread}] Failed attempt {attempt}: {err}")
            time.sleep(0.5)  # wait before retry

def demonstrate_safe() -> None:
    """Show how immutable arguments are safely passed to threads"""

    print("--- Safe argument passing ---")

    # Create threads with different argument combinations
    t1 = threading.Thread(target=download_with_options, args=(1, "video.mp4"))
    t2 = threading.Thread(
        target=download_with_options,
        args=(2, "document.pdf"),
        kwargs={"size_mb": 5, "priority": "high"}
    )
    t3 = threading.Thread(
        target=download_with_options,
        args=(3, "music.mp3"),
        kwargs={"priority": "low"}
    )

    # Start all threads
    for t in [t1, t2, t3]:
        t.start()

    # Wait for all threads to complete
    for t in [t1, t2, t3]:
        t.join()

if __name__ == "__main__":
    demonstrate_safe()
