# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///

import threading
import time

# Regular lock and reentrant lock for comparison
connection_lock = threading.Lock()
reentrant_connection_lock = threading.RLock()

active_downloads = 0


class DownloadManager:
    """Example showing practical use of RLock for download management"""

    active_downloads: int
    completed_downloads: int
    total_bytes: int
    lock: threading.RLock

    def __init__(self) -> None:
        self.active_downloads = 0
        self.completed_downloads = 0
        self.total_bytes = 0
        self.lock = threading.RLock()  # use RLock for methods that call each other

    def start_download(self, file_name: str, size_mb: int) -> None:
        """Begin a download"""

        with self.lock:
            self.active_downloads += 1
            print(f"Starting download: {file_name} {size_mb}MB")
            self._log_activity("started", file_name, size_mb)
            time.sleep(0.1)  # simulate initail setup

    def complete_download(self, file_name: str, size_mb: int) -> bool:
        """Complete a download"""

        with self.lock:
            if self.active_downloads > 0:
                self.active_downloads -= 1
                self.completed_downloads += 1
                self.total_bytes += size_mb * 1024 * 1024
                print(f"Complete download: {file_name}")
                self._log_activity("completed", file_name, size_mb)
                return True
            return False

    def _log_activity(self, action: str, file_name: str, size_mb: int) -> None:
        """Log download activity - also needs the lock"""

        with self.lock:  # same thread can acquire RLock again
            print(
                f" LOG: {action} {file_name} ({size_mb}MB) - Active: {self.active_downloads}"
            )

    def transfer_and_clenup(self, file_name: str, size_mb: int) -> None:
        """Transfer file and cleanup - calls multiple methods needing lock"""

        with self.lock:
            if self.complete_download(file_name, size_mb):  # This also needs the lock
                print(f" Cleaned up {file_name}")


def demonstrate_download_manager() -> None:
    """Show Rlock in a practical download scenario"""

    print("--- Download Manager with RLock ---")

    manager = DownloadManager()

    # These operations work because RLock allows the same thread
    # to acquire the lock multiple tmes
    manager.start_download("video.mp4", 25)
    manager.start_download("music.mp3", 5)
    manager.complete_download("video.mp4", 25)
    manager.transfer_and_clenup("music.mp3", 5)

    print(
        f"Final Stats: {manager.completed_downloads} completed, {manager.total_bytes // 1024 // 1024}MB total"
    )


if __name__ == "__main__":
    demonstrate_download_manager()
