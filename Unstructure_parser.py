import time
import tracemalloc
import psutil
import os

# Start tracking time and memory
# start_time = time.time()
# tracemalloc.start()

# process = psutil.Process(os.getpid())

# === Your Code Starts Here ===
from langchain_unstructured import UnstructuredLoader

loader = UnstructuredLoader(
    file_path="leac204.pdf",
    strategy="hi_res",
    extract_images_in_pdf=True,
    infer_table_structure=True,
)

docs = []
for doc in loader.lazy_load():
    docs.append(doc)

print(docs)
# === Your Code Ends Here ===

# Stop tracking
# current, peak = tracemalloc.get_traced_memory()
# tracemalloc.stop()

# end_time = time.time()

# print(f"Execution Time: {end_time - start_time:.2f} seconds")
# print(f"Memory Usage: {current / 1024 / 1024:.2f} MB; Peak: {peak / 1024 / 1024:.2f} MB")
# print(f"CPU Usage: {process.cpu_percent(interval=1.0)}%")
# print(f"Memory Used by Process: {process.memory_info().rss / 1024 / 1024:.2f} MB")
