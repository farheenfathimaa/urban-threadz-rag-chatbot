from langchain.embeddings import GoogleGenerativeAIEmbeddings
from app.config import GEMINI_API_KEY

def get_embeddings():
    return GoogleGenerativeAIEmbeddings(
        google_api_key=GEMINI_API_KEY,
        model="models/embedding-001"
    )
