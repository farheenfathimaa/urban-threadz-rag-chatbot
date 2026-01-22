import os
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

VECTOR_DB_PATH = "vector_db"

def get_embeddings():
    """
    Local, free, deterministic embeddings.
    MUST match the model used during ingestion.
    """
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

def load_vectorstore(business_id: str):
    embeddings = get_embeddings()
    path = os.path.join(VECTOR_DB_PATH, business_id)

    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
        # Empty FAISS index (safe fallback)
        return FAISS.from_documents([], embeddings)

    return FAISS.load_local(
        path,
        embeddings,
        allow_dangerous_deserialization=True
    )

def get_retriever(business_id: str, role: str):
    vectorstore = load_vectorstore(business_id)

    return vectorstore.as_retriever(
        search_kwargs={
            "k": 4,
            "filter": {
                "access": role
            }
        }
    )
