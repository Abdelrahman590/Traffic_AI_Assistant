from typing import List
from langchain_core.documents import Document

from ingestion.vector_store import get_or_build_vector_store, get_retriever


_vector_store = None
_retriever = None


def get_shared_retriever():
    global _vector_store, _retriever
    if _retriever is None:
        _vector_store = get_or_build_vector_store()
        _retriever = get_retriever(_vector_store)
    return _retriever


def retrieve_documents(query: str) -> List[Document]:
    retriever = get_shared_retriever()
    return retriever.invoke(query)


def format_context(documents: List[Document]) -> str:
    parts = []
    for i, doc in enumerate(documents, start=1):
        source = doc.metadata.get("source", "unknown")
        parts.append(f"[Source {i} - {source}]\n{doc.page_content}")
    return "\n\n".join(parts)
