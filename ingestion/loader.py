from langchain.document_loaders import PyMuPDFLoader, TextLoader
from langchain.document_loaders.word_document import Docx2txtLoader
import tempfile
import os

def load_document(uploaded_file):
    suffix = uploaded_file.name.split(".")[-1].lower()

    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as tmp:
        tmp.write(uploaded_file.read())
        temp_path = tmp.name

    try:
        if suffix == "pdf":
            loader = PyMuPDFLoader(temp_path)
        elif suffix == "txt":
            loader = TextLoader(temp_path, encoding="utf-8")
        elif suffix == "docx":
            loader = Docx2txtLoader(temp_path)
        else:
            raise ValueError("Unsupported file type")

        documents = loader.load()
        return documents

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
