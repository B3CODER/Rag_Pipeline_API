import pdfplumber
import re

# --- PDF Parsing and Chunking ---
def parse_pdf_into_blocks(filepath: str) -> list:
    all_blocks = []
    with pdfplumber.open(filepath) as pdf:
        for idx, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables()
            if tables:
                for table in tables:
                    table_str = "\n".join(str(row) for row in table)
                    all_blocks.append(('table', table_str.strip(), idx))
            text = page.extract_text() or ""
            if text.strip():
                all_blocks.append(('text', text.strip(), idx))
    return all_blocks

def format_table_as_string(table_data_str: str) -> str:
    return f"--- TABLE START ---\n{table_data_str}\n--- TABLE END ---"

def chunk_text(text: str, max_length: int) -> list:
    text = re.sub(r'\n+', ' ', text).strip()
    sentence_endings = re.compile(r'(?<!\w\.\w\.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s')
    sentences = sentence_endings.split(text)
    sentences = [s.strip() for s in sentences if s.strip()]
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 > max_length and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            separator = " " if current_chunk else ""
            current_chunk += separator + sentence
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def generate_final_chunks(blocks: list, max_chunk_size: int = 1500, min_chunk_size: int = 300) -> list:
    initial_chunks = []
    text_buffer = ""
    current_page = None
    for block_type, content, page_number in blocks:
        if block_type == 'text':
            if current_page is None:
                current_page = page_number
            text_buffer += content + " "
        elif block_type == 'table':
            if text_buffer.strip():
                text_chunks = chunk_text(text_buffer.strip(), max_chunk_size)
                initial_chunks.extend((chunk, current_page) for chunk in text_chunks)
                text_buffer = ""
            table_chunk = format_table_as_string(content)
            initial_chunks.append((table_chunk, page_number))
            current_page = None
    if text_buffer.strip():
        text_chunks = chunk_text(text_buffer.strip(), max_chunk_size)
        initial_chunks.extend((chunk, current_page) for chunk in text_chunks)
    final_chunks = [initial_chunks[0]] if initial_chunks else []
    for chunk, page_number in initial_chunks[1:]:
        last_chunk, last_page = final_chunks[-1]
        if len(chunk) < min_chunk_size and last_page == page_number:
            final_chunks[-1] = (last_chunk + "\n\n" + chunk, last_page)
        else:
            final_chunks.append((chunk, page_number))
    import json; json.dump([{"chunk": c, "page": p} for c, p in final_chunks], open("parsed_chunks.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return final_chunks
