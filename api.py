from fastapi import FastAPI, UploadFile, File, HTTPException, Query
import os
import shutil
from pdf_parser.parser import parse_pdf_into_blocks, generate_final_chunks
from vectorstore.embedder import get_embedder
from vectorstore.store import init_qdrant, delete_pdf_from_qdrant
from langchain_core.documents import Document
from qa.rag_chain import create_qa_system
from config import COLLECTION_NAME

app = FastAPI()

@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        upload_dir = "uploaded_pdfs"
        os.makedirs(upload_dir, exist_ok=True)
        filename = file.filename if file.filename else ""
        if not filename:
            raise HTTPException(status_code=400, detail="Invalid file name.")
        file_path = os.path.join(upload_dir, filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        blocks = parse_pdf_into_blocks(file_path)
        chunks = generate_final_chunks(blocks)
        if not chunks:
            raise ValueError("No chunks generated from PDF.")
        docs = [Document(page_content=c, metadata={"page": p, "pdf_name": filename}) for c, p in chunks]
        embeddings = get_embedder()
        init_qdrant(COLLECTION_NAME, embeddings, docs)
        return {"message": f"PDF '{filename}' uploaded and processed."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat_pdf/")
async def chat_pdf(question: str = Query(...), pdf_name: str = Query(...)):
    try:
        if not pdf_name:
            raise HTTPException(status_code=400, detail="Invalid PDF name.")
        file_path = os.path.join("uploaded_pdfs", pdf_name)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="PDF not found.")
        invoke_chain, _ = create_qa_system(file_path)
        answer, _ = invoke_chain(question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/delete_pdf/")
async def delete_pdf(pdf_name: str = Query(...)):
    try:
        if not pdf_name:
            raise HTTPException(status_code=400, detail="Invalid PDF name.")
        file_path = os.path.join("uploaded_pdfs", pdf_name)
        if os.path.exists(file_path):
            os.remove(file_path)
        delete_pdf_from_qdrant(COLLECTION_NAME, pdf_name)
        return {"message": f"PDF '{pdf_name}' and its vectors deleted."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 