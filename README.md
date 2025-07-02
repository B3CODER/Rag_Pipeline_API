# PDF RAG Chat Backend

A modular, production-ready FastAPI backend for PDF upload, chunking, embedding, vector storage (Qdrant), and LLM-powered chat.

## Features
- Upload PDFs, parse, chunk, embed, and store in Qdrant
- Chat with PDFs using LLM and retrieval
- Delete PDFs and their vectors
- Modular, reusable code structure

## Project Structure
```
app/
  api/routes.py         # All API endpoints
  core/config.py        # Configuration and environment
  core/startup.py       # Startup logic (placeholder)
  main.py               # FastAPI app entrypoint
  models/schemas.py     # Pydantic models
  services/pdf_service.py    # PDF upload/parse logic
  services/chat_service.py   # Chat logic
  services/vector_service.py # Vector store logic
  utils/helpers.py      # Utility functions (placeholder)

uploaded_pdfs/          # Uploaded PDF files
qdrant_data/            # Qdrant vector DB data
requirements.txt        # Dependencies
.env.example            # Example environment variables
```

## Setup
1. **Clone the repo and install dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Copy and edit environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env as needed
   ```
3. **Run the server:**
   ```bash
   uvicorn app.main:app --reload
   ```
4. **Open Swagger UI:**
   [http://localhost:8000/docs](http://localhost:8000/docs)

## Usage
- **POST /upload_pdf/**: Upload a PDF file
- **POST /chat_pdf/**: Chat with a PDF (provide `question` and `pdf_name`)
- **DELETE /delete_pdf/**: Delete a PDF and its vectors (provide `pdf_name`)

## License
MIT 