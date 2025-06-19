import re

def split_markdown_into_chunks(markdown_text, min_chars=1000, max_chars=1500):
    header_pattern = re.compile(r'^(#{1,2})\s+.*')
    table_pattern = re.compile(r'^\s*\|')  # Markdown table row starts with '|'
    
    lines = markdown_text.splitlines()
    chunks = []
    current_chunk = []
    current_text = ''
    
    def flush_chunk():
        nonlocal current_chunk, current_text
        if current_text.strip():
            chunks.append(current_text.strip())
        current_chunk = []
        current_text = ''

    i = 0
    while i < len(lines):
        line = lines[i]

        # Check for table start
        if table_pattern.match(line):
            flush_chunk()
            table_lines = []
            while i < len(lines) and (table_pattern.match(lines[i]) or lines[i].strip() == ''):
                table_lines.append(lines[i])
                i += 1
            chunks.append('\n'.join(table_lines).strip())
            continue

        # Check for header
        if header_pattern.match(line):
            if len(current_text) >= min_chars:
                flush_chunk()
            elif len(current_text) > 0:
                current_text += '\n' + line
            else:
                flush_chunk()
                current_text += line
        else:
            current_text += '\n' + line

        # Split if current_text exceeds max_chars
        if len(current_text) >= max_chars:
            flush_chunk()
        
        i += 1

    # Add remaining content as last chunk
    flush_chunk()
    
    return chunks

# Example usage with your markdown file
with open("conversion_results.md", "r", encoding="utf-8") as f:
    markdown_text = f.read()

chunks = split_markdown_into_chunks(markdown_text)

# Saving chunks to individual files or printing
with open("all_chunks.md", "w", encoding="utf-8") as f:
    for idx, chunk in enumerate(chunks, 1):
        f.write(f"\n\n<!-- ================= Chunk {idx} ================= -->\n\n")
        f.write(chunk)