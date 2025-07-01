from langchain_huggingface import HuggingFaceEmbeddings
from config import EMBEDDING_MODEL

from langchain_huggingface import HuggingFaceEmbeddings

def get_embedder():
    return HuggingFaceEmbeddings(
        model_name="BAAI/bge-base-en-v1.5",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
