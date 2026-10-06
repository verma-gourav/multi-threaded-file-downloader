# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///

import random
import threading
import time

# Three shared resource locks
bandwidth_lock = threading.Lock()
connection_lock = threading.Lock()
storage_lock = threading.Lock()


def download_task1(file_name: str) -> None:
    """Grabs bandwidth first, then waits for connection (Safe with timeouts)"""

    while True:
        print(f"[Taks1]: Starting Download of {file_name}")
        print("[Task1]: Acquiring bandwidth lock...")

        with bandwidth_lock:
            print("[Task1]: Got bandwidth lock, checking available bandwidth...")
            time.sleep(0.1)  # force context switch to allow others to grab locks

            print("[Task1]: Trying to aquiring connection lock with timeout...")

            # Try to grab the second lock, waiting a maximum of 1.0 second
            got_connection = connection_lock.acquire(timeout=1.0)

            if got_connection:
                try:
                    print(f"[Task1]: Successfully downloaded {file_name}")
                    return  # download completed, exit loop
                finally:
                    connection_lock.release()

            # Back-off phase if the second lock was blocked
            print(
                "[Task1]: BLOCKED on connection lock. Releasing bandwidth and backing off..."
            )

        # Sleep a randomized interval to break perfect synchronization (prevents livelock)
        time.sleep(random.uniform(0.1, 0.4))


def download_task2(file_name: str) -> None:
    """Grabs the connection first, then waits for storage"""

    while True:
        print(f"[Task2]: Starting Download of {file_name}")
        print("[Task2]: Acquiring connection lock...")

        with connection_lock:
            print("[Task2]: Got connection lock, establishing connection...")
            time.sleep(0.1)

            print("Task2: Trying to aquiring storage lock with timeout...")
            got_storage = storage_lock.acquire(timeout=1.0)

            if got_storage:
                try:
                    print(f"[Task2]: Successfully downloaded {file_name}")
                    return
                finally:
                    storage_lock.release()

            print(
                "[Task2]: BLOCKED on storage lock. Releasing connection and backing off..."
            )

        time.sleep(random.uniform(0.1, 0.4))


def downloader_task3(file_name: str) -> None:
    """Grabs the storage first, then waits for bandwidth - CLOSES THE CIRCLE"""

    while True:
        print(f"[Task3]: Starting Download of {file_name}")
        print("[Task3]: Acquiring storage lock...")

        with storage_lock:
            print("[Task3]: Got storage lock, establishing connection...")
            time.sleep(0.1)

            print("[Task3]: Trying to aquiring bandwidth lock with timeout...")
            got_bandwith = bandwidth_lock.acquire(timeout=1.0)

            if got_bandwith:
                try:
                    print(f"[Task3]: Successfully downloaded {file_name}")
                    return
                finally:
                    bandwidth_lock.release()

            print(
                "[Task3]: BLOCKED on bandwidth lock. Releasing storage lock and backing off..."
            )

        time.sleep(random.uniform(0.1, 0.4))


def demonstrate_safe_resolution() -> None:
    """Demonstrate safe resolution for circular deadlock using timeout and radomized backoff time to prevent livelock"""

    print("--- Timeout With Randomized Backoff Demo ---")

    # Create and start threads
    t1 = threading.Thread(
        target=download_task1, args=("video.mp4",), name="Safe-Downloader-1"
    )
    t2 = threading.Thread(
        target=download_task2, args=("music.mp3",), name="Safe-Downloader-2"
    )
    t3 = threading.Thread(
        target=downloader_task3, args=("image.jpg",), name="Safe-Downloader-3"
    )

    print("Starting download threads - SAFE")
    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    print("\n All safe donwload threads completed.")


if __name__ == "__main__":
    demonstrate_safe_resolution()
