# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///

import random
import threading
import time


# def download_file(url: str, file_name: str) -> str:
#     """Download a single file"""
#
#     thread_name = threading.current_thread().name
#     print(f"[{thread_name}] Starting: {file_name}")
#     time.sleep(random.uniform(2, 6))  # simulate download time [random time for each thread]
#     print(f"[{thread_name}] Completed: {file_name}")
#     return file_name

class DownloadThread(threading.Thread):
    """Custom thread class for downloading files with buit-in retry logic"""

    def __init__(self, url: str, file_name: str, max_retries: int = 3) -> None:
        super().__init__(name=f"Downloader-{file_name.split(".")[0]}")
        self.url = url
        self.file_name = file_name
        self.max_retries = max_retries
        self.result = None
        self.download_time = None
        self.attemps = 0

    def run(self) -> None:
        """Called when thread.start() runs"""
        print(f"[{self.name}] Starting Download: {self.file_name}")
        start_time = time.time()

        for attempt in range(1, self.max_retries + 1):
            self.attemps = attempt
            try:
                print(f"[{self.name}] Attemp {attempt} for {self.file_name}")
                time.sleep(random.uniform(2, 6))  # simulate download time

                if attempt == 1 and random.random() < 0.2:  # 20% chance of failure
                  raise Exception("Network timeout")

                self.download_time = time.time() - start_time
                self.result = "success"
                print(f"[{self.name}] {self.file_name} downloaded in {self.download_time:.1f}s")
                return

            except Exception as err:
                print(f"[{self.name}] Attempt {attempt} failed: {err}")
                if attempt < self.max_retries:
                    time.sleep(0.5)  # brief pause before retry
                else:
                    self.result = "failed"
                    self.download_time = time.time() - start_time
                    print(f"[{self.name}] Permanently failed after {attempt} attemps")

def demonstrate_custom_threads() -> None:
    files = [
        ("https://example.com/video.mp4", "video.mp4"),
        ("https://example.com/document.pdf", "document.pdf"),
        ("https://example.com/music.mp3", "music.mp3"),
        ("https://example.com/word.doc", "word.doc"),
    ]

    print("--- Custom Thread Class Downloads ---")
    download_threads = [DownloadThread(url, file_name) for url, file_name in files]

    start_time = time.time()
    for t in download_threads: t.start()
    for t in download_threads: t.join()
    total_time = time.time() - start_time

    print("\n--- Download Results ---")
    successful = 0
    for t in download_threads:
        status = "Success" if t.result == "success" else "Failed"
        print(f"{status} - {t.file_name}: {t.result} ({t.attemps} attempts, {t.download_time:.1f}s)")
        if t.result == "success": successful += 1

    print(f"Total time: {total_time:.1f} seconds")
    print(f"Success rate: {successful}/{len(download_threads)}")

if __name__ == "__main__":
    demonstrate_custom_threads()
