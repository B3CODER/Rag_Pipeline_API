import os
import tika
from tika import parser as tika_parser

# Initialize Java VM for Tika (required only once)
tika.TikaClientOnly = True
tika.initVM()

def parse_file(filepath: str):
    """
    Universal file parser using Apache Tika.
    Returns a list with a single dict containing page_content and metadata.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    parsed = tika_parser.from_file(filepath)
    content = parsed.get("content", "")
    metadata = {"source": filepath}

    return [{"page_content": content.strip(), "metadata": metadata}]

if __name__ == "__main__":
    filename = input("Enter the filename to parse: ").strip()

    try:
        docs = parse_file(filename)
        text_output = docs[0]["page_content"]

        # Write to TXT file (same name as input but with .txt extension)
        output_filename = os.path.splitext(filename)[0] + ".txt"
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(text_output)

        print(f"\n✅ Content saved to '{output_filename}'")

    except Exception as e:
        print(f"\n❌ Error parsing file: {e}")



# # # # import requests

# # # # file_path = "leac204.pdf"
# # # # url = "http://localhost:9998/tika"

# # # # with open(file_path, "rb") as f:
# # # #     headers = {"Accept": "text/html"}
# # # #     response = requests.put(url, data=f, headers=headers)

# # # # html_output = response.text
# # # # print(html_output)




# # # from tika import parser as p 
# # # import requests
# # # import tika



# # # def get_data_from_given_path(file_path):
# # #     results = p.from_file(file_path)
# # #     return results


# # # pdf_file_path = "leac204.pdf"
# # # results = get_data_from_given_path(pdf_file_path)
# # # print(results["content"].strip())

