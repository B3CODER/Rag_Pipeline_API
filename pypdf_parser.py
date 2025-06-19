import pdfplumber
import tracemalloc
import time
import psutil
import os

pdf_path = "leac204.pdf"

# Start memory tracking
tracemalloc.start()
process = psutil.Process(os.getpid())  # For process-level memory
start_time = time.time()

with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        print(f"\n===== Page {i + 1} =====\n")

        # 1️⃣ Print page text
        text = page.extract_text()
        if text:
            print("Text Content:\n")
            print(text)
        else:
            print("No text found on this page.")

        # 2️⃣ Print tables, if any
        tables = page.extract_tables()
        if tables:
            for j, table in enumerate(tables):
                print(f"\nTable {j + 1}:\n")
                for row in table:
                    print(row)

end_time = time.time()
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

# Get current process memory in MB
memory_used_by_process = process.memory_info().rss / (1024 * 1024)

print("\n===== Resource Usage =====")
print(f"Execution Time: {end_time - start_time:.2f} seconds")
print(f"Python Allocated Memory (Current): {current / 10**6:.2f} MB")
print(f"Python Peak Allocated Memory (Peak): {peak / 10**6:.2f} MB")
print(f"Memory Used by Process (RSS): {memory_used_by_process:.2f} MB")
