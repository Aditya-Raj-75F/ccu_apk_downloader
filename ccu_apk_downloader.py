#!/usr/bin/env python3
import sys
import requests
import time

def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    if hours > 0:
        return f"{int(hours)} hour(s), {int(minutes)} minute(s), and {int(seconds)} second(s)"
    elif minutes > 0:
        return f"{int(minutes)} minute(s) and {int(seconds)} second(s)"
    else:
        return f"{seconds:.2f} second(s)"

def download_file(url):
    filename = url.split("/")[-1] if '/' in url else "ccu.apk"
    try:
        
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            total_length = response.headers.get('content-length')
            
            if total_length is None:
                print("Cannot determine the size of the file to download.")
            else:
                total_length = int(total_length)
                                
                start_time = time.time()
                
                with open(filename, "wb") as f:
                    contentDownloaded = 0
                    for chunk in response.iter_content(chunk_size=4096):
                        if chunk:
                            contentDownloaded += len(chunk)
                            f.write(chunk)
                            completion_progress = int(50 * contentDownloaded / total_length)
                            sys.stdout.write("\r[%s%s] %d%%" % ('=' * completion_progress, ' ' * (50 - completion_progress), 100 * contentDownloaded / total_length))
                            sys.stdout.flush()
                            
                end_time = time.time()
                total_time_elapsed = end_time - start_time
                            
            print(f"\nDownloaded {filename} from {url} in {format_time(total_time_elapsed)}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {filename} from {url}")
        print(e.response)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Requires exactly two arguments: environment and version")
        print(sys.argv)
        sys.exit(1)
    else:
        environment = sys.argv[1]
        version = sys.argv[2]
        base_url = "http://updates.75fahrenheit.com/RENATUS_CCU_"
        apk_extension = ".apk"
        download_url = base_url + environment + "_" + version + apk_extension
        download_file(download_url)