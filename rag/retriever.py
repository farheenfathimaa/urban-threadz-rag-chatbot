import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from ingestion.embedder import get_embeddings  # 🔥 single source of truth

VECTOR_DB_PATH = "vector_db"

def load_vectorstore(business_id: str):
    embeddings = get_embeddings()
    path = os.path.join(VECTOR_DB_PATH, business_id)

    print("📂 Loading vector store from:", path)

    if not os.path.exists(path):
        raise FileNotFoundError(f"Vector store not found: {path}")

    vs = FAISS.load_local(
        path,
        embeddings,
        allow_dangerous_deserialization=True
    )

    print("✅ Vector store loaded, doc count:", vs.index.ntotal)
    return vs

def get_retriever(business_id: str, role: str):
    vectorstore = load_vectorstore(business_id)

    # Adding the 'filter' ensures that the search only looks at 
    # documents the current role is allowed to see.
    return vectorstore.as_retriever(
        search_kwargs={
            "k": 4,
            "filter": {"access": role} 
        }
    )
