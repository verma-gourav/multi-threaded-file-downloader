# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///


import queue
import random
import threading
import time

# Thread-safe queue for download jobs
download_queue = queue.Queue()


def download_producer() -> None:
    """Generate download jobs and put them in queue"""

    download_jobs = [
        ("video1.mp4", 20),
        ("video2.mp4", 15),
        ("document1.pdf", 3),
        ("document2.pdf", 5),
        ("music.mp3", 8),
        ("music.mp3", 12),
    ]

    print("[Producer]: Adding download jobs in queue...")
    for i, (file_name, size_mb) in enumerate(download_jobs, 1):
        job = {"id": i, "file_name": file_name, "size_mb": size_mb}
        download_queue.put(job)  # thread-safe operation
        print(f"Added job {i}: {file_name} ({size_mb}MB)")
        time.sleep(0.3)  # simulate time b/w job creation

    # Signal end of work with sentinel values for consumers
    for _ in range(2):  # we'll have 2 consumer thread
        download_queue.put(None)
    print("[Producer]: All jobs queued, sent stop signals")


def download_consumer(consumer_id: int) -> None:
    """Take download jobs from the queue and process them"""
    download_files = []

    print(f"[Consumer-{consumer_id}]: Starting download worker")

    while True:
        job = download_queue.get()  # thread-safe operation, blocks if queue is empty

        if job is None:
            # Sentinel value means no more work
            print(f"[Consumer-{consumer_id}]: Recieved stop signal, shutting down")
            break

        # Process the download job
        file_name = job["file_name"]
        size_mb = job["size_mb"]

        print(f"[Consumer-{consumer_id}]: Starting download {file_name}")

        # Simulate download time
        download_time = size_mb * 0.15 + random.uniform(0, 0.5)
        time.sleep(download_time)

        download_files.append(file_name)
        print(
            f"[Consumer-{consumer_id}]: Completed {file_name} in {download_time:.1f}s"
        )

        download_queue.task_done()  # mark job as completed

    print(f"[Consumer-{consumer_id}]: Downloaded {len(download_files)} files")


def demonstrate_download_queue() -> None:
    """Show producer-consumer pattern for download management"""

    print("--- Producer-Consumer Download Queue ---")

    # Create producer thread
    producer = threading.Thread(target=download_producer, name="Producer")

    # Create multiple consumer threads
    consumers = []
    for i in range(1, 3):
        consumer = threading.Thread(
            target=download_consumer, args=(i,), name=f"Consumer-{i}"
        )
        consumers.append(consumer)

    start_time = time.time()

    # Start all threads
    producer.start()
    for consumer in consumers:
        consumer.start()

    # Wait for all to complete
    producer.join()
    for consumer in consumers:
        consumer.join()

    total_time = time.time() - start_time
    print(f"\nAll downloads completed in {total_time:.1f} seconds")


if __name__ == "__main__":
    demonstrate_download_queue()
