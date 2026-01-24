import os
import tempfile
from langchain_community.vectorstores import FAISS
from ingestion.loader import load_document
from ingestion.chunker import chunk_documents
from ingestion.embedder import get_embeddings
from app.config import BUSINESS_ID

VECTOR_DB_PATH = "vector_db"

def ingest_files(uploaded_files, business_id: str, access: str, max_docs: int | None = None
):
    if not uploaded_files:
        return

    if max_docs is not None and len(uploaded_files) > max_docs:
        raise ValueError(f"Maximum {max_docs} documents allowed for this package.")

    all_docs = []

    for file in uploaded_files:
        filename = os.path.basename(file.name).lower()

        # ✅ HARD FILTER (no more unsupported file crashes)
        if not filename.endswith((".pdf", ".txt", ".docx")):
            print(f"Skipping unsupported file: {filename}")
            continue

        # ✅ Normalize to temp file (works for upload + disk)
        with tempfile.NamedTemporaryFile(delete=False, suffix=filename) as tmp:
            tmp.write(file.read())
            temp_path = tmp.name

        try:
            documents = load_document(temp_path)

            for doc in documents:
                doc.metadata.update({
                    "business_id": business_id,
                    "access": access,
                    "source": filename
                })

            chunks = chunk_documents(documents)
            all_docs.extend(chunks)

        finally:
            os.remove(temp_path)

    if not all_docs:
        raise ValueError("No valid documents found for ingestion.")
        return

    embeddings = get_embeddings()
    business_path = os.path.join(VECTOR_DB_PATH, business_id)

    try:
        if os.path.exists(business_path):
            vectorstore = FAISS.load_local(
                business_path,
                embeddings,
                allow_dangerous_deserialization=True
            )
            vectorstore.add_documents(all_docs)
        else:
            raise FileNotFoundError
    except Exception as e:
        print(f"Rebuilding FAISS index for {business_id}: {e}")
        vectorstore = FAISS.from_documents(all_docs, embeddings)

    vectorstore.save_local(business_path)

if __name__ == "__main__":
    from pathlib import Path

    BUSINESS_ID = BUSINESS_ID
    BASE_PATH = Path("businesses") / BUSINESS_ID

    admin_docs = list((BASE_PATH / "admin_docs").glob("*.txt"))
    public_docs = list((BASE_PATH / "public_docs").glob("*.txt"))

    class FileLike:
        def __init__(self, path):
            self.name = path.name
            self._path = path

        def read(self):
            return self._path.read_bytes()

    admin_files = [FileLike(p) for p in admin_docs]
    public_files = [FileLike(p) for p in public_docs]

    print("Ingesting admin docs...")
    ingest_files(admin_files, BUSINESS_ID, access="admin")

    print("Ingesting public docs...")
    ingest_files(public_files, BUSINESS_ID, access="public")

    print("✅ Ingestion completed")
