# PDF RAG Chat Backend

A modular, production-ready FastAPI backend for PDF upload, chunking, embedding, vector storage (Qdrant), and LLM-powered chat.

## Features
- Upload PDFs, parse, chunk, embed, and store in Qdrant
- Chat with PDFs using LLM and retrieval
- Delete PDFs and their vectors
- Modular, reusable code structure

## Usage
- **POST /upload_pdf/**: Upload a PDF file
- **POST /chat_pdf/**: Chat with a PDF (provide `question` and `pdf_name`)
- **DELETE /delete_pdf/**: Delete a PDF and its vectors (provide `pdf_name`)
