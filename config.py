import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
QDRANT_PATH = "qdrant_data"
COLLECTION_NAME = "rag_collection"
EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"
