# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///

import threading
import time

# Two locks that willcause problems if acquired in different orders
bandwidth_lock = threading.Lock()
connection_lock = threading.Lock()


def download_task1(file_name: str) -> None:
    """Download using bandwidth lock first, then the connection lock"""

    print(f"Taks1: Starting Download of {file_name}")
    print("Task1: Acquiring bandwidth lock...")

    with bandwidth_lock:
        print("Task1: Got bandwidth lock, checking available bandwidth...")
        time.sleep(0.1)  # give task2 time to aquire connection_lock

        print("Task1: Now aquiring connection lock...")
        with connection_lock:  # this will wait forever if task2 holds connection_lock
            print(f"Task1: Successfully downloaded {file_name}")


def download_task2(file_name: str) -> None:
    """Download using connection lock, then bandwidth lock - DANGEROUS"""

    print(f"Task2: Starting Download of {file_name}")
    print("Task2: Acquiring connection lock...")

    with connection_lock:
        print("Task2: Got connection lock, establishing connection...")
        time.sleep(0.1)  # give task1 time to aquire bandwidth_lock

        print("Task2: Now aquiring bandwidth lock...")
        with bandwidth_lock:
            print(f"Task2: Successfully downloaded {file_name}")


def demonstrate_download_deadlock() -> None:
    """Demonstrate deadlock in download resource management"""

    print("--- Download Deadlock Demo ---")

    # Create and start threads
    t1 = threading.Thread(
        target=download_task1, args=("video.mp4",), name="Downloader-1"
    )
    t2 = threading.Thread(
        target=download_task2, args=("music.mp3",), name="Downloader-2"
    )

    print("Starting download threads - this may deadlock...")
    t1.start()
    t2.start()

    # These joins may wait forever if deadlock occurs
    try:
        t1.join(timeout=5)  # wait max 5 seconds
        t2.join(timeout=0.5)

        if t1.is_alive() or t2.is_alive():
            print("DEADLOCK DETECTED! Threads are still running after timeout.")
            print("In a real application, we need to handle this situation.")
        else:
            print("Both downloads complete successfully")
    except KeyboardInterrupt:
        print("Donwload interrupted by user")


if __name__ == "__main__":
    demonstrate_download_deadlock()
