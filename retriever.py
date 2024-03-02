from typing import List
from chromadb.api.models import Collection

#
# client = chromadb.PersistentClient(path="./DB/")
#
# collection = client.get_or_create_collection(name="pdf_demo", embedding_function=MyEmbeddingFunction())


def get_documents_by_query(query: str, collection: Collection) -> List[str]:
    return collection.query(query_texts=[query], n_results=10)['documents'][0]


