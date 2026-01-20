import os
from langchain.vectorstores import FAISS
from ingestion.loader import load_document
from ingestion.chunker import chunk_documents
from ingestion.embedder import get_embeddings

VECTOR_DB_PATH = "vector_db"

if max_docs and len(uploaded_files) > max_docs:
    raise ValueError(f"Maximum {max_docs} documents allowed for this package.")

def ingest_files(
    uploaded_files,
    business_id: str,
    access: str
):
    all_docs = []

    for file in uploaded_files:
        documents = load_document(file)

        for doc in documents:
            doc.metadata.update({
                "business_id": business_id,
                "access": access,
                "source": file.name
            })

        chunks = chunk_documents(documents)
        all_docs.extend(chunks)

    if not all_docs:
        raise ValueError("No valid documents found for ingestion.")

    embeddings = get_embeddings()
    business_path = os.path.join(VECTOR_DB_PATH, business_id)

    if os.path.exists(business_path):
        vectorstore = FAISS.load_local(
            business_path,
            embeddings,
            allow_dangerous_deserialization=True
        )
        vectorstore.add_documents(all_docs)
    else:
        vectorstore = FAISS.from_documents(all_docs, embeddings)

    vectorstore.save_local(business_path)
