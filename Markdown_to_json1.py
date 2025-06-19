import re

def parse_markdown_table(markdown_text):
    tables = []
    table_blocks = re.findall(r'((?:\|.*\n)+)', markdown_text)

    for block in table_blocks:
        lines = block.strip().split("\n")
        headers = [h.strip() for h in lines[0].strip('|').split('|')]
        rows = []
        for line in lines[2:]:  # skip header and separator line
            if re.match(r'^\|[-\s|]+$', line):  # skip separator lines
                continue
            values = [v.strip() for v in line.strip('|').split('|')]
            row = dict(zip(headers, values))
            rows.append(row)
        tables.append({"headers": headers, "rows": rows})
    return tables

# Example usage
with open("conversion_results.txt", "r", encoding="utf-8") as f:
    markdown_text = f.read()

parsed_tables = parse_markdown_table(markdown_text)

import json
print(json.dumps(parsed_tables, indent=2))
