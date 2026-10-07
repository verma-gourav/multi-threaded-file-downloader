# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///

import threading
import time


def download_monitor() -> None:
    """A daemond task that monitors download progress indefinitely"""

    while True:
        print("Monitoring download queue...")
        time.sleep(2)


def download_heartbeat() -> None:
    """A daemon task that sends keep-alive signals"""

    while True:
        print("Download service heartbeat - keeping connections alive")
        time.sleep(3)


def actual_download(file_name: str, size_mb: int) -> None:
    """Simulate an actual download task"""

    print(f"Downloading {file_name} ({size_mb}MB)...")
    download_time = size_mb * 0.3
    time.sleep(download_time)
    print(f"{file_name} download complete!")


def demonstrate_daemon_downloads() -> None:
    """Show how daemon threads work with download monitoring"""
    print("--- Daemon Thread Download Demo ---")

    # Create daemon threads for background monitoring
    monitor_thread = threading.Thread(
        target=download_monitor, daemon=True, name="Monitor"
    )
    heartbeat_thread = threading.Thread(
        target=download_heartbeat, daemon=True, name="Heartbeat"
    )

    # Start daemon threads
    monitor_thread.start()
    heartbeat_thread.start()

    # Do some actual downloads (non-daemon threads)
    download_threads = []
    files = [("video.mp4", 4), ("document.pdf", 2), ("music.mp3", 3)]

    for file_name, size_mb in files:
        t = threading.Thread(
            target=actual_download,
            args=(file_name, size_mb),
            name=f"Download-{file_name}",
        )
        download_threads.append(t)
        t.start()

    # Wait for actual downloads to complete
    for t in download_threads:
        t.join()

    print("All downloads completed!")
    print("Main program ending - daemon threads will stop automatically")

    # Program exits here - daemon threads stop automatically
    # If daemon=False, program would wait for monitor and heartbeat to finish


if __name__ == "__main__":
    demonstrate_daemon_downloads()
