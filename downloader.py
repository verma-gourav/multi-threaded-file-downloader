# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///

import threading
import time


def download_file(url: str, file_name: str) -> str:
    """Download a single file"""

    thread_name = threading.current_thread().name
    print(f"[{thread_name}] Starting: {file_name}")
    time.sleep(2)  # simulate download time
    print(f"[{thread_name}] Completed: {file_name}")
    return file_name

def threaded_downloads() -> None:
    """Download files one by one (sequential)"""

    files = [
        ("https://example.com/video.mp4", "video.mp4"),
        ("https://example.com/document.pdf", "document.pdf"),
        ("https://example.com/music.mp3", "music.mp3"),
        ("https://example.com/word.doc", "word.doc"),
    ]

    print("--- Multi-Threaded Downloads ---")
    start_time = time.time()

    threads = []

    # Step 1: Create threads
    for url, file_name in files:
        thread = threading.Thread(
            target=download_file,
            args=(url, file_name),
            name=f"Downloader-{file_name.split(".")[0]}"
        )
        threads.append(thread)

    # Step 2: Start all threads
    for thread in threads:
        thread.start()

    # Step 3: Wait for all threads to complete
    for thread in threads:
        thread.join()

    total_time = time.time() - start_time
    print(f"Threaded time: {total_time:.1f} seconds")

if __name__ == "__main__":
    threaded_downloads()
