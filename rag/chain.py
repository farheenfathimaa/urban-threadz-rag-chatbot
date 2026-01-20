from langchain.chains import RetrievalQA
from rag.prompts import RAG_PROMPT
from rag.llm_factory import get_primary_llm, get_fallback_llm

def build_rag_chain(retriever):
    llm = get_primary_llm()

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={
            "prompt": RAG_PROMPT
        },
        return_source_documents=False
    )

def run_rag(chain, query: str):
    try:
        return chain.run(query)
    except Exception:
        fallback_llm = get_fallback_llm()
        chain.llm = fallback_llm
        return chain.run(query)
