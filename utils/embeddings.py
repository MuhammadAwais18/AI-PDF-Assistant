import streamlit as st
import os
import hashlib
from rank_bm25 import BM25Okapi

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


@st.cache_resource
def load_embedding_model():
    """
    Load embedding model once and reuse.
    """

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

def get_pdf_hash(pdf_text: str):

    return hashlib.md5(
        pdf_text.encode("utf-8")
    ).hexdigest()


def create_vector_store(pdf_text: str):

    """
    Create FAISS vector database
    while preserving page numbers.
    """

    if not pdf_text.strip():
        raise ValueError("PDF text is empty.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    pages = pdf_text.split("[Page ")

    texts = []

    metadatas = []

    for page in pages:

        if not page.strip():
            continue

        try:

            file_name = page.split("[FILE:")[1].split("]")[0]

            page_number = int(
                page.split("[Page ")[1].split("]")[0]
            )

            content = page.split("]", 2)[2]

        except Exception:

            file_name = "Unknown"

            page_number = 0

            content = page

        chunks = splitter.split_text(
            content
        )

        for chunk in chunks:

            texts.append(chunk)

            metadatas.append(
                {
                    "page": page_number,
                    "file": file_name
                }
            )
            
    pdf_hash = get_pdf_hash(pdf_text)

    cache_dir = f"vector_cache/{pdf_hash}"

    embeddings = load_embedding_model()

    if os.path.exists(cache_dir):

       return FAISS.load_local(
           cache_dir,
           embeddings,
           allow_dangerous_deserialization=True
        )

    vectorstore = FAISS.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas
    )

    tokenized_texts = [
        text.split()
        for text in texts
    ]

    bm25 = BM25Okapi(
        tokenized_texts
    )


    os.makedirs(
        "vector_cache",
        exist_ok=True
    )

    vectorstore.save_local(
        cache_dir
    )

    return vectorstore