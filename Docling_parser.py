import time
import tracemalloc
import psutil
import os

from docling.document_converter import DocumentConverter

# Start monitoring
# start_time = time.time()
# tracemalloc.start()
# process = psutil.Process(os.getpid())

# === Your Document Conversion Code Starts ===
source = "leac204.pdf"  # Local file path

converter = DocumentConverter()
result = converter.convert(source)

# Print markdown result
markdown_output = result.document.export_to_html()
print(markdown_output)

# Save to file
# with open('conversion_results.md', 'w', encoding='utf-8') as f:
#     f.write("\n\nMarkdown Conversion:\n")
#     f.write(markdown_output)

# === Your Code Ends ===

# # Stop monitoring
# current, peak = tracemalloc.get_traced_memory()
# tracemalloc.stop()
# end_time = time.time()

# # Print resource usage
# print("\n--- Resource Usage ---")
# print(f"Execution Time      : {end_time - start_time:.2f} seconds")
# print(f"Memory Usage        : {current / 1024 / 1024:.2f} MB (current)")
# print(f"Peak Memory Usage   : {peak / 1024 / 1024:.2f} MB (peak)")
# print(f"Process RSS (RAM)   : {process.memory_info().rss / 1024 / 1024:.2f} MB")
# print(f"CPU Usage (percent) : {process.cpu_percent(interval=1.0)}%")
