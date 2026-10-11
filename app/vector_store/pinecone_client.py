from pinecone import Pinecone, ServerlessSpec

from app.config.settings import (
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME,
)


EMBEDDING_DIMENSION = 384


class PineconeClient:

    def __init__(self):

        if not PINECONE_API_KEY:
            raise ValueError(
                "PINECONE_API_KEY is missing from .env"
            )

        self.pc = Pinecone(
            api_key=PINECONE_API_KEY
        )

        self.index_name = PINECONE_INDEX_NAME

        self._create_index()

        self.index = self.pc.Index(
                     self.index_name
                    )

    def _create_index(self):

        existing_indexes = [
            index.name
            for index in self.pc.list_indexes()
        ]

        if self.index_name not in existing_indexes:

            print(
                f"Creating Pinecone index: "
                f"{self.index_name}"
            )

            self.pc.create_index(
                name      = self.index_name,
                dimension = EMBEDDING_DIMENSION,
                metric    = "cosine",
                spec      = ServerlessSpec(
                            cloud="aws",
                            region="us-east-1"
                           )
            )

            print("Pinecone index created.")

        else:
            print(
                f"Pinecone index already exists: "
                f"{self.index_name}"
            )

    def get_index(self):
        return self.index