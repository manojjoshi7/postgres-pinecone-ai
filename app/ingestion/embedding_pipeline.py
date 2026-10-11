from app.data.documents import get_documents_batch
from app.embeddings.local_embeddings import LocalEmbeddingModel
from app.vector_store.pinecone_client import PineconeClient


BATCH_SIZE = 100


def main():

    print("=" * 70)
    print("POSTGRESQL → EMBEDDINGS → PINECONE")
    print("=" * 70)

    # Load embedding model only once
    embedding_model = LocalEmbeddingModel()

    # Connect to Pinecone
    pinecone_client = PineconeClient()
    index = pinecone_client.get_index()

    offset = 4200
    total_uploaded = 0

    while True:

        print("\n" + "-" * 70)
        print(
            f"Loading PostgreSQL batch: "
            f"offset={offset}, size={BATCH_SIZE}"
        )

        documents = get_documents_batch(
            offset=offset,
            batch_size=BATCH_SIZE
        )

        if not documents:
            print("\nNo more documents.")
            break

        print(
            f"Documents loaded: {len(documents)}"
        )

        # ------------------------------------------------
        # Generate embeddings
        # ------------------------------------------------

        texts = [
            document["text"]
            for document in documents
        ]

        print("Generating embeddings...")

        vectors = embedding_model.embed_documents(
            texts
        )

        # ------------------------------------------------
        # Prepare Pinecone records
        # ------------------------------------------------

        pinecone_vectors = []

        for document, vector in zip(
            documents,
            vectors
        ):

            metadata = {
                "text": document["text"]
            }

            for key, value in document["metadata"].items():

                if key == "id":
                    continue

                if value is not None:

                    metadata[key] = str(value)

            pinecone_vectors.append({
                "id": document["id"],
                "values": vector,
                "metadata": metadata
            })

        # ------------------------------------------------
        # Upload to Pinecone
        # ------------------------------------------------

        print("Uploading to Pinecone...")

        index.upsert(
            vectors=pinecone_vectors
        )

        total_uploaded += len(documents)

        print(
            f"Uploaded batch: {len(documents)}"
        )

        print(
            f"Total uploaded: {total_uploaded}"
        )

        # Move to next batch
        offset += BATCH_SIZE

    # ----------------------------------------------------
    # Final statistics
    # ----------------------------------------------------

    print("\n" + "=" * 70)
    print("INGESTION COMPLETED")
    print("=" * 70)

    print(
        f"Total vectors uploaded: {total_uploaded}"
    )

    print("\nPinecone statistics:")

    print(
        index.describe_index_stats()
    )


if __name__ == "__main__":
    main()