import os
from langchain_community.vectorstores import FAISS

from config import (
    LICENSE_DOC_PATH,
    VIOLATIONS_XLSX_PATH,
    VECTOR_STORE_DIR,
    TOP_K,
)
from ingestion.loaders import load_all_documents
from ingestion.splitter import split_documents
from ingestion.embeddings import get_embeddings_model


def build_vector_store(
    license_path: str = LICENSE_DOC_PATH,
    violations_path: str = VIOLATIONS_XLSX_PATH,
    persist_dir: str = VECTOR_STORE_DIR,
) -> FAISS:
    documents = load_all_documents(license_path, violations_path)
    chunks = split_documents(documents)

    embeddings = get_embeddings_model()
    vector_store = FAISS.from_documents(chunks, embeddings)

    os.makedirs(persist_dir, exist_ok=True)
    vector_store.save_local(persist_dir)

    return vector_store


def load_vector_store(persist_dir: str = VECTOR_STORE_DIR) -> FAISS:
    embeddings = get_embeddings_model()
    return FAISS.load_local(
        persist_dir,
        embeddings,
        allow_dangerous_deserialization=True,
    )


def get_or_build_vector_store(persist_dir: str = VECTOR_STORE_DIR) -> FAISS:
    if os.path.exists(persist_dir) and os.listdir(persist_dir):
        return load_vector_store(persist_dir)
    return build_vector_store(persist_dir=persist_dir)


def get_retriever(vector_store: FAISS, k: int = TOP_K):
    return vector_store.as_retriever(search_kwargs={"k": k})
