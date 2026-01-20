import os
from langchain.vectorstores import FAISS
from langchain.embeddings import GoogleGenerativeAIEmbeddings
from app.config import GEMINI_API_KEY

VECTOR_DB_PATH = "vector_db"

def get_embeddings():
    return GoogleGenerativeAIEmbeddings(
        google_api_key=GEMINI_API_KEY,
        model="models/embedding-001"
    )

def load_vectorstore(business_id: str):
    embeddings = get_embeddings()
    path = os.path.join(VECTOR_DB_PATH, business_id)

    if not os.path.exists(path):
        os.makedirs(path)
        return FAISS.from_documents([], get_embeddings()).as_retriever()


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
