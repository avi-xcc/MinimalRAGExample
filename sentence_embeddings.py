from chromadb import EmbeddingFunction, Documents, Embeddings
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2", cache_folder="./models/")


class MyEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input_docs: Documents) -> Embeddings:
        return model.encode(input_docs).tolist()
