from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.from_texts(
    ["Refund policy is 7 days", "Office timing is 9 to 6"],
    embedding=embeddings
)

docs = db.similarity_search("When can I get a refund?")
print(docs[0].page_content)
