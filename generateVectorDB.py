import chromadb
from chromadb.api.models import Collection
import streamlit as st
from pdf_read_info import get_text_data
from sentence_embeddings import MyEmbeddingFunction


# pdf_path = "./BEA_report.pdf"

@st.cache_resource
def get_collection() -> Collection:
    client = chromadb.PersistentClient(path="./DB/")

    return client.get_or_create_collection(name="pdf_demo", embedding_function=MyEmbeddingFunction())


def process_pdf(pdf_path, collection):
    all_text = get_text_data(pdf_path)
    doc_list = []
    id_list = []

    page_size = 512
    overlap = 128

    page_offset = collection.count()

    deletable_ids = [str(idx) for idx in range(page_offset)]
    collection.delete(ids=deletable_ids)

    page_offset = collection.count()
    print(page_offset)

    for idx in range(0, len(all_text) - page_size, page_size):
        if idx != 0:
            idx -= overlap
        doc_list.append(all_text[idx: idx + page_size])
        id_list.append(str(page_offset))
        page_offset += 1

    collection.add(documents=doc_list,
                   ids=id_list)
