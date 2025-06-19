from docling.document_converter import DocumentConverter
from langchain.text_splitter import MarkdownHeaderTextSplitter

# Step 1: Convert PDF to Markdown
source = "basic-understanding-of-a-companys-financials.pdf"
converter = DocumentConverter()
result = converter.convert(source)

# Get Markdown text from the result
markdown_text = result.document.export_to_markdown()

# Step 2: Define the Header Split Rules (depends on your document's headings)
headers_to_split_on = [
    ("#", "Header 1"),         # Split on '# ' (H1)
    ("##", "Header 2"),        # Split on '## ' (H2)
    ("###", "Header 3"),       # Split on '### ' (H3)
]

# Initialize the splitter
splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

# Split the Markdown into chunks
splits = splitter.split_text(markdown_text)

# Step 3: Print Chunks
for i, chunk in enumerate(splits):
    print(f"\n\n--- Chunk {i+1} ---")
    print(f"Metadata: {chunk.metadata}")
    print(chunk.page_content)