# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///


import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


def download_files_with_retry(file_info: tuple[str, int]) -> dict:  # type: ignore
    """Simulate downloadiing a file with retry logic"""

    file_name, size_mb = file_info

    print(f"Starting download: {file_name} ({size_mb}MB)")

    # Simulate variable donwload time
    base_time = size_mb * 0.15
    download_time = base_time + random.uniform(0, base_time * 0.3)

    # Simulate occasional network issues
    for attempt in range(3):
        try:
            time.sleep(download_time / 3)  # Simulate partial download

            if attempt == 0 and random.random() < 0.15:
                raise RuntimeError("Network timeout")

            print(f"Completed: {file_name} in {download_time:.1f}s")
            return {
                "file_name": file_name,
                "status": "success",
                "size_mb": size_mb,
                "download_time": download_time,
                "attempts": attempt + 1,
            }

        except RuntimeError as err:
            if attempt < 2:
                print(f"Retry {attempt + 1} for {file_name}: {err}")
                time.sleep(0.2)
            else:
                print(f"Failed: {file_name} after 3 attempts")
                return {
                    "file_name": file_name,
                    "status": "failed",
                    "error": str(err),
                    "attempts": 3,
                }


def demonstrate_download_pool() -> None:
    """Show how thread pools simplify concurrent downloads"""

    download_files = [
        ("video1.mp4", 25),
        ("video2.mp4", 30),
        ("video3.mp4", 20),
        ("doc1.pdf", 5),
        ("doc2.pdf", 3),
        ("doc3.pdf", 8),
        ("music1.mp3", 12),
        ("music2.mp3", 15),
        ("music3.mp3", 10),
    ]

    print("--- Thread Pool Download Manager ---")
    print(f"Downloading {len(download_files)} files using thread pool...")

    start_time = time.time()

    # Create a pool of 3 workers threads
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Submit all download tasks to the pool
        future_to_file = {
            executor.submit(download_files_with_retry, file_info): file_info
            for file_info in download_files
        }

        # Collect results as they complete
        results = []
        for future in as_completed(future_to_file):
            try:
                result = future.result()
                results.append(result)
            except Exception as exc:
                print(f"Download generate exception: {exc}")

    total_time = time.time() - start_time

    # Analyze results
    successful = [r for r in results if r["status"] == "success"]
    failed = [r for r in results if r["status"] == "failed"]
    total_size = sum(r["size_mb"] for r in successful)

    print(f"\n--- Download Pool Results ---")
    print(f"Total time: {total_time:.1f} seconds")
    print(f"Successful downloads: {len(successful)}/{len(download_files)}")
    print(f"Failed downloads: {len(failed)}")
    print(f"Total data downloaded: {total_size}MB")
    if total_size > 0:
        print(f"Average download speed: {total_size / total_time:.1f} MB/s")


if __name__ == "__main__":
    demonstrate_download_pool()
