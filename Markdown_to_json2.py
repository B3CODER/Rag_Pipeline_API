import pandas as pd
import re
import io
import json
from markdown_it import MarkdownIt
from typing import List, Dict, Tuple

def clean_markdown_table(table_lines: List[str]) -> List[Dict]:
    try:
        md_table = "\n".join(table_lines)
        df = pd.read_csv(io.StringIO(md_table), sep="|", engine='python', skipinitialspace=True)
        df = df.dropna(axis=1, how='all').dropna(how='all')
        df.columns = [col.strip() for col in df.columns]
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        df = df[~df.iloc[:, 0].str.contains(r'^[-=]+$', na=False)]
        return df.to_dict(orient="records")
    except Exception as e:
        print(f"[Warning] Table parsing failed: {e}")
        return []

def extract_tables_separately(text: str) -> Tuple[List[Dict], List[str]]:
    tables = []
    current_table = []
    in_table = False
    table_number = 0
    extracted_raw_tables = []

    for line in text.splitlines():
        if re.match(r'^\|.*\|$', line.strip()):
            in_table = True
            current_table.append(line)
        elif in_table:
            if current_table:
                raw_table = "\n".join(current_table)
                rows = clean_markdown_table(current_table)
                if rows:
                    table_number += 1
                    tables.append({
                        "table_number": table_number,
                        "rows": rows
                    })
                    extracted_raw_tables.append(raw_table)
                current_table = []
            in_table = False

    if current_table:
        raw_table = "\n".join(current_table)
        rows = clean_markdown_table(current_table)
        if rows:
            table_number += 1
            tables.append({
                "table_number": table_number,
                "rows": rows
            })
            extracted_raw_tables.append(raw_table)

    return tables, extracted_raw_tables

def extract_text_blocks(text: str, exclude_blocks: List[str]) -> List[Dict]:
    md = MarkdownIt()
    tokens = md.parse(text)
    content_blocks = []
    block = {"type": "", "content": ""}

    for token in tokens:
        if token.type in ["heading_open", "paragraph_open"]:
            block = {"type": token.tag, "content": ""}
        elif token.type == "inline":
            block["content"] += token.content.strip() + " "
        elif token.type in ["heading_close", "paragraph_close"]:
            clean_content = block["content"].strip()
            # Exclude if the content matches or contains full markdown table content
            if all(raw_table not in clean_content for raw_table in exclude_blocks):
                content_blocks.append(block)

    return content_blocks

def extract_images(text: str) -> List[str]:
    return re.findall(r'<!--\s*image\s*-->', text)

def parse_full_markdown(filepath: str) -> Dict:
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    tables, raw_tables = extract_tables_separately(text)
    text_blocks = extract_text_blocks(text, raw_tables)
    images = extract_images(text)

    return {
        "tables": tables,
        "text_blocks": text_blocks,
        "images": images
    }

# Example usage
file_path = "conversion_results.txt"
output = parse_full_markdown(file_path)

with open("final_output.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print("✅ FINAL JSON created → 'final_output.json'")                    
