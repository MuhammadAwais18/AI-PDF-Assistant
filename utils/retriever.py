from rank_bm25 import BM25Okapi


bm25_index = None
bm25_chunks = []


def initialize_bm25(texts):

    global bm25_index
    global bm25_chunks

    bm25_chunks = texts

    tokenized = [
        text.lower().split()
        for text in texts
    ]

    bm25_index = BM25Okapi(
        tokenized
    )


def retrieve_documents(
    vectorstore,
    question,
    k=4
):

    docs = vectorstore.similarity_search(
        question,
        k=k
    )

    return docs