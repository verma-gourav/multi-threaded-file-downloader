# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///

import threading
import time

# Global download statistics and lock to protect them
download_counter = 0
bytes_downloaded = 0
completed_files = 0
stats_lock = threading.Lock()


def download_with_tracking(file_name: str, size_mb: int) -> None:
    """Safely download file and track statistics using a lock"""

    global download_counter, bytes_downloaded, completed_files

    print(f"Starting download: {file_name}")

    # Simulate downlaoding in small chunks
    chunks = size_mb * 100  # 100 chunks per MB
    for _ in range(chunks):
        # The 'with' statement acts as a context manager for lock
        with stats_lock:
            # Only one thread can execute these lines at a time
            # This prevents race conditions

            current_counter = download_counter
            current_bytes = bytes_downloaded

            # Small delay to make race condition more likely
            time.sleep(0.0001)

            download_counter = current_counter + 1
            bytes_downloaded = current_bytes + 10240  # 10KB per chunk

        # Safely update completion count
        with stats_lock:
            completed_files += 1

    print(f"Completed: {file_name}")


def demonstrate_safe_downloads() -> None:
    """Show how locks prevent race conditions in download tracking"""

    global download_counter, bytes_downloaded, completed_files
    download_counter = 0
    bytes_downloaded = 0
    completed_files = 0

    print("--- Safe Download Statistics with Lock ---")

    files = [
        ("video.mp4", 20),
        ("document.pdf", 5),
        ("music.mp3", 10),
        ("image.jpg", 3),
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
            name=f"Downloader-{file_name.split('.')[0]}",
        )
        threads.append(thread)

    # Start and wait for all threads
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    total_time = time.time() - start_time

    print("\n--- Results (now accurate with locks) ---")
    print(f"Expected chunks: {expected_chunks:,}")
    print(f"Actual chunks: {download_counter:,}")
    print(f"Lost chunks: {expected_chunks - download_counter:,}")
    print(f"Expected bytes: {expected_bytes:,}")
    print(f"Actual bytes: {bytes_downloaded:,}")
    print(f"Lost bytes: {expected_bytes - bytes_downloaded:,}")
    print(f"Accuracy: {(download_counter / expected_chunks) * 100:.1f}%")
    print(f"Time taken: {total_time:.2f} seconds")


if __name__ == "__main__":
    demonstrate_safe_downloads()
