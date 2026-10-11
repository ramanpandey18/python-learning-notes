import threading
import time
from concurrent.futures import ThreadPoolExecutor
import requests

def fetch_data(url):
    print(f"Fetching {url}")
    time.sleep(1)           # ← actual 1 second delay
    print(f"Done {url}")

start = time.time()

threads = []
for url in ["url1", "url2", "url3"]:
    t = threading.Thread(target=fetch_data, args=(url,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"Total time: {time.time() - start:.2f}s")


def fetch_data_v2(api_name, delay):
    print(f"Fetching data for {api_name}...")
    time.sleep(delay)
    print(f"Finished fetch for {api_name}!")

thread1 = threading.Thread(target=fetch_data_v2, args=("UserAPI", 2))
thread2 = threading.Thread(target=fetch_data_v2, args=("productAPI", 4))

thread1.start()
thread2.start()

thread1.join()
thread2.join()
print(f"All API data fetched successfully!")


# def download_file(file_id):
#     print(f"Downloading file {file_id}...")
#     time.sleep(1.5)
#     return f"File {file_id} content"

# file_ids = [101, 102, 103, 104]

# # Using a context manager automatically shuts down the pool when finished
# with ThreadPoolExecutor(max_workers=3) as executor:
#     # map applies the function to each element in the list concurrently
#     results = executor.map(download_file, file_ids)

# # Process results
# for result in results:
#     print(result)


# def task(n):
#     print(f"Starting task {n}")
#     time.sleep(2)

#     if n == 2:
#         raise ValueError("Something went wrong!")

#     return n * 10

# executor = ThreadPoolExecutor(max_workers=3)

# try:
#     futures = []

#     for i in range(4):
#         futures.append(executor.submit(task, i))

#     for future in futures:
#         print(future.result())  # Raises exception for task 2

# except Exception as e:
#     print("Caught exception:", e)

# finally:
#     print("Shutting down executor...")
#     executor.shutdown(wait=True)
#     print("Executor shutdown complete.")


img_urls = [
    'https://media.geeksforgeeks.org/wp-content/uploads/20190623210949/download21.jpg',
    'https://media.geeksforgeeks.org/wp-content/uploads/20190623211125/d11.jpg',
    'https://media.geeksforgeeks.org/wp-content/uploads/20190623211655/d31.jpg',
    'https://media.geeksforgeeks.org/wp-content/uploads/20190623212213/d4.jpg',
    'https://media.geeksforgeeks.org/wp-content/uploads/20190623212607/d5.jpg',
    'https://media.geeksforgeeks.org/wp-content/uploads/20190623235904/d6.jpg',
]


t1 = time.perf_counter()

def download_image(img_url):
    requests.get(img_url).content
    print("Downloading...")

for img in img_urls:
    download_image(img)

t2 = time.perf_counter()
print(f'Single Threaded Code Took :{t2 - t1} seconds')

print("*"*50)

t1 = time.perf_counter()

def download_image(img_url):
    requests.get(img_url).content
    print("Downloading...")

with ThreadPoolExecutor(3) as executor:
    executor.map(download_image, img_urls)

t2 = time.perf_counter()
print(f'MultiThreaded Code Took:{t2 - t1} seconds')
