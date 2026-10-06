# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///

import threading
import time

# Three shared resource locks
bandwidth_lock = threading.Lock()
connection_lock = threading.Lock()
storage_lock = threading.Lock()


def download_task1(file_name: str) -> None:
    """Grabs bandwidth first, then waits for connection"""

    print(f"Taks1: Starting Download of {file_name}")
    print("Task1: Acquiring bandwidth lock...")

    with bandwidth_lock:
        print("Task1: Got bandwidth lock, checking available bandwidth...")
        time.sleep(0.1)  # force context switch to allow others to grab locks

        print("Task1: Now aquiring connection lock...")
        with (
            connection_lock
        ):  # this will wait forever if other task holds connection_lock
            print(f"Task1: Successfully downloaded {file_name}")


def download_task2(file_name: str) -> None:
    """Grabs the connection first, then waits for storage"""

    print(f"Task2: Starting Download of {file_name}")
    print("Task2: Acquiring connection lock...")

    with connection_lock:
        print("Task2: Got connection lock, establishing connection...")
        time.sleep(0.1)

        print("Task2: Now aquiring storage lock...")
        with storage_lock:
            print(f"Task2: Successfully downloaded {file_name}")


def downloader_task3(file_name: str) -> None:
    """Grabs the storage first, then waits for bandwidth - CLOSES THE CIRCLE"""

    print(f"Task3: Starting Download of {file_name}")
    print("Task3: Acquiring storage lock...")

    with storage_lock:
        print("Task3: Got storage lock, establishing connection...")
        time.sleep(0.1)

        print("Task3: Now aquiring bandwidth lock...")
        with bandwidth_lock:
            print(f"Task3: Successfully downloaded {file_name}")


def demonstrate_circular_deadlock() -> None:
    """Demonstrate circular deadlock in download resource management"""

    print("--- Circular Deadlock [Dining Philosophers] Demo ---")

    # Create and start threads
    t1 = threading.Thread(
        target=download_task1, args=("video.mp4",), name="Downloader-1"
    )
    t2 = threading.Thread(
        target=download_task2, args=("music.mp3",), name="Downloader-2"
    )
    t3 = threading.Thread(
        target=downloader_task3, args=("image.jpg",), name="Downloader-3"
    )

    print("Starting download threads - this may deadlock...")
    t1.start()
    t2.start()
    t3.start()

    # These joins may wait forever if deadlock occurs
    try:
        t1.join(timeout=5)  # wait max 5 seconds
        t2.join(timeout=0.5)
        t3.join(timeout=0.5)

        if t1.is_alive() or t2.is_alive() or t3.is_alive():
            print("DEADLOCK DETECTED! Threads are still running after timeout.")
            print("In a real application, we need to handle this situation.")
        else:
            print("Both downloads complete successfully")
    except KeyboardInterrupt:
        print("Donwload interrupted by user")


if __name__ == "__main__":
    demonstrate_circular_deadlock()
