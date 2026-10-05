# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///

import random
import threading
import time

# Global download statistics shared by all threads
download_counter = 0
bytes_downloaded = 0

def download_with_tracking(file_name: str, size_mb: int) -> None:
    """Download file and track statistics - UNSAFE"""

    global download_counter, bytes_downloaded

    print(f"Starting download: {file_name}")

    # Simulate downlaoding in small chunks
    chunks = size_mb * 100  # 100 chunks per MB
    for _ in range(chunks):
        # These lines are NOT atomic - each is actually multiple operations:
        # 1. Read current value of counter
        # 2. Add 1 to that value
        # 3. Store the results back to counter
        # Othr threads can interfere b/w these steps

        current_counter = download_counter
        current_bytes = bytes_downloaded

        # Small delay to make race condition more likely
        time.sleep(0.0001)

        download_counter = current_counter + 1
        bytes_downloaded = current_bytes + 10240  # 10KB per chunk

    print(f"Completed: {file_name}")


def demonstrate_download_race() -> None:
    """Show how race conditions corrupt download statistics"""

    global download_counter, bytes_downloaded
    download_counter = 0
    bytes_downloaded = 0

    print("--- Download Race Condition Demo ---")

    files = [
        ("video.mp4", 20),
        ("document.pdf", 5),
        ("music.mp3", 10)
    ]

    # Calculate expected totals
    expected_chunks = sum(size * 100 for _, size in files)
    expected_bytes = expected_chunks * 10240

    threads = []
    start_time = time.time()

    # Create threads for each donwload
    for file_name, size_mb in files:
        thread = threading.Thread(
            target=download_with_tracking,
            args=(file_name, size_mb),
            name=f"Downloader-{file_name.split(".")[0]}"
        )
        threads.append(thread)

    # Start and wait for all threads
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    total_time = time.time() - start_time

    print("\n--- Results (likely corrupted due to race conditions) ---")
    print(f"Expected chunks: {expected_chunks:,}")
    print(f"Actual chunks: {download_counter:,}")
    print(f"Lost chunks: {expected_chunks - download_counter:,}")
    print(f"Expected bytes: {expected_bytes:,}")
    print(f"Actual bytes: {bytes_downloaded:,}")
    print(f"Lost bytes: {expected_bytes - bytes_downloaded:,}")
    print(f"Accuracy: {(download_counter/expected_chunks)*100:.1f}%")
    print(f"Time taken: {total_time:.2f} seconds")


if __name__ == "__main__":
    demonstrate_download_race()
