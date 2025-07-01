from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_community.vectorstores import Qdrant as LangchainQdrant

def init_qdrant(collection_name, embeddings, documents):
    client = QdrantClient(path="qdrant_data")
    try:
        client.get_collection(collection_name)
    except:
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE)
        )
    return LangchainQdrant.from_documents(
        documents=documents,
        embedding=embeddings,
        url="http://localhost:6333",
        collection_name=collection_name
    )
