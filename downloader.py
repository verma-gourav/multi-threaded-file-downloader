# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///

import time


def download_file(url: str, file_name: str) -> str:
    """Simulate downloading filename"""

    print(f"Starting Download: {file_name}")
    time.sleep(2)  # simulate download time
    print(f"Completed: {file_name}")
    return file_name

def main() -> None:
    """Download files one by one (sequential)"""

    files = [
        ("https://example.com/video.mp4", "video.mp4"),
        ("https://example.com/document.pdf", "document.pdf"),
        ("https://example.com/music.mp3", "music.mp3"),
        ("https://example.com/word.doc", "word.doc"),
    ]

    print("--- Sequential Downloads ---")
    start_time = time.time()

    for url, file_name in files:
        download_file(url, file_name)

    total_time = time.time() - start_time
    print(f"Total time: {total_time:.1f} seconds")

if __name__ == "__main__":
    main()
