
#!!! 仅供科研使用
import json
import threading
import requests
import time
from tqdm import tqdm
import https_proxy_server_lists as https_proxy

servers = https_proxy.servers

results_lock = threading.Lock()
def test_speed(url, port, results, progress_bar):
    proxy = {'https': f'https://{url}:{port}'}

    try:
        start_time = time.time()
        response = requests.get("https://google.com", proxies=proxy, timeout=5)
        end_time = time.time()

        download_speed = len(response.content) / (end_time - start_time)

        with results_lock:
            results.append({"url": url, "port": port, "speed_mps": download_speed})
    except Exception as e:
        with results_lock:
            results.append({"url": url, "port": port, "error": str(e)})

    progress_bar.update(1)


def main():
    results = []

    total_tests = sum(len(country_data["hosts"]) for country_data in servers)
    with tqdm(total=total_tests, desc="Testing Speed", unit="host") as progress_bar:
        threads = []

        for country_data in servers:
            country = country_data["country"]

            for host in country_data["hosts"]:
                url = host["url"]
                port = host["port"]

                # Testing each host in a separate thread
                thread = threading.Thread(
                    target=test_speed, args=(url, port, results, progress_bar)
                )
                thread.start()
                threads.append(thread)

        # Wait for all threads to finish
        for thread in threads:
            thread.join()
    
    sorted_results = sorted(results, key=lambda x: x.get('speed_mps', 0), reverse=True)

    # Save results to a file
    with open("speed_test_results.json", "w") as f:
        json.dump(sorted_results, f, indent=2)

if __name__ == "__main__":
    main()
