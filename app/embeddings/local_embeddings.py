from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


class LocalEmbeddingModel:

    def __init__(self):
        print(f"Loading embedding model: {MODEL_NAME}")

        self.model = SentenceTransformer(MODEL_NAME)

        print("Embedding model loaded.")

    def embed_text(self, text):
        vector = self.model.encode(
            text,
            normalize_embeddings=True
        )

        return vector.tolist()

    def embed_documents(self, texts):
        vectors = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True
        )

        return vectors.tolist()