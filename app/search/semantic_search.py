from app.embeddings.local_embeddings import LocalEmbeddingModel
from app.vector_store.pinecone_client import PineconeClient


class SemanticSearch:

    def __init__(self):

        print("Loading embedding model...")

        self.embedding_model = LocalEmbeddingModel()

        print("Connecting to Pinecone...")

        pinecone_client = PineconeClient()

        self.index = pinecone_client.get_index()

    def search(self, question, top_k=5):

        print(f"\nQuestion: {question}")

        # Convert question into vector
        query_vector = self.embedding_model.embed_text(
            question
        )

        print(
            f"Query vector dimensions: "
            f"{len(query_vector)}"
        )

        # Search Pinecone
        result = self.index.query(
            vector=query_vector,
            top_k=top_k,
            include_metadata=True
        )

        return result


def main():

    search = SemanticSearch()

    question = (
        "What type of products are customers "
        "most interested in?"
    )

    results = search.search(
        question,
        top_k=5
    )

    print("\n" + "=" * 70)
    print("SEARCH RESULTS")
    print("=" * 70)

    for number, match in enumerate(
        results.matches,
        start=1
    ):

        print("\n" + "-" * 70)

        print(f"Result #{number}")

        print("ID:", match.id)

        print("Score:", match.score)

        metadata = match.metadata or {}

        print("\nText:")

        print(
            metadata.get(
                "text",
                "No text available"
            )
        )


if __name__ == "__main__":
    main()