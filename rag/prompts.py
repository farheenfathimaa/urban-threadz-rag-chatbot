from langchain.prompts import PromptTemplate

RAG_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are an AI assistant for a business.

Use ONLY the information provided in the context below to answer the question.
If the answer is not in the context, say:
"I don't have enough information from the provided documents."

Context:
{context}

Question:
{question}

Answer clearly and concisely.
"""
)
