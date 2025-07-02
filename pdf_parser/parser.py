import pdfplumber
import re
import json
import os
from typing import List, Tuple

# --- PDF Parsing and Chunking with Error Handling ---
def parse_pdf_into_blocks(filepath: str) -> List[Tuple[str, str, int]]:
    all_blocks = []

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"❌ File not found: {filepath}")

    try:
        with pdfplumber.open(filepath) as pdf:
            if not pdf.pages:
                raise ValueError(f"❗ PDF is empty: {filepath}")

            for idx, page in enumerate(pdf.pages, start=1):
                try:
                    tables = page.extract_tables()
                except Exception as e:
                    print(f"[Warning] Failed to extract tables on page {idx}: {e}")
                    tables = []

                for table in tables or []:
                    try:
                        table_str = "\n".join(str(row) for row in table)
                        all_blocks.append(('table', table_str.strip(), idx))
                    except Exception as e:
                        print(f"[Warning] Failed to format table on page {idx}: {e}")

                try:
                    text = page.extract_text() or ""
                    if text.strip():
                        all_blocks.append(('text', text.strip(), idx))
                except Exception as e:
                    print(f"[Warning] Failed to extract text on page {idx}: {e}")
    except Exception as e:
        raise RuntimeError(f"❌ Error reading PDF '{filepath}': {e}")

    return all_blocks


def format_table_as_string(table_data_str: str) -> str:
    return f"--- TABLE START ---\n{table_data_str}\n--- TABLE END ---"


def chunk_text(text: str, max_length: int) -> List[str]:
    try:
        text = re.sub(r'\n+', ' ', text).strip()
        sentence_endings = re.compile(r'(?<!\w\.\w\.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s')
        sentences = sentence_endings.split(text)
        sentences = [s.strip() for s in sentences if s.strip()]
    except Exception as e:
        raise RuntimeError(f"❌ Failed during sentence splitting: {e}")

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        try:
            if len(current_chunk) + len(sentence) + 1 > max_length and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                separator = " " if current_chunk else ""
                current_chunk += separator + sentence
        except Exception as e:
            print(f"[Warning] Failed while building chunk: {e}")
            continue

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def generate_final_chunks(blocks: List[Tuple[str, str, int]], max_chunk_size: int = 1500, min_chunk_size: int = 300) -> List[Tuple[str, int]]:
    initial_chunks = []
    text_buffer = ""
    current_page = None

    for block_type, content, page_number in blocks:
        try:
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
        except Exception as e:
            print(f"[Warning] Error processing block on page {page_number}: {e}")

    if text_buffer.strip():
        try:
            text_chunks = chunk_text(text_buffer.strip(), max_chunk_size)
            initial_chunks.extend((chunk, current_page) for chunk in text_chunks)
        except Exception as e:
            print(f"[Warning] Failed final text flush: {e}")

    final_chunks = []
    try:
        if initial_chunks:
            final_chunks = [initial_chunks[0]]
            for chunk, page_number in initial_chunks[1:]:
                last_chunk, last_page = final_chunks[-1]
                if len(chunk) < min_chunk_size and last_page == page_number:
                    final_chunks[-1] = (last_chunk + "\n\n" + chunk, last_page)
                else:
                    final_chunks.append((chunk, page_number))
    except Exception as e:
        raise RuntimeError(f"❌ Error merging chunks: {e}")

    # Save to JSON
    try:
        output_path = "parsed_chunks.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump([{"chunk": c, "page": p} for c, p in final_chunks], f, ensure_ascii=False, indent=2)
        print(f"✅ Saved parsed chunks to {output_path}")
    except Exception as e:
        print(f"[Warning] Failed to save output to JSON: {e}")

    return final_chunks
