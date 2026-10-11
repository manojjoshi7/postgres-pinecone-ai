from app.embeddings.local_embeddings import LocalEmbeddingModel


def main():

    embedding_model = LocalEmbeddingModel()

    text = """
    Customer purchased electronics products.
    Customer purchase amount was 599.99.
    Customer is interested in online shopping.
    """

    vector = embedding_model.embed_text(text)

    print("=" * 60)
    print("LOCAL EMBEDDING TEST")
    print("=" * 60)

    print("Model: all-MiniLM-L6-v2")
    print("Vector dimensions:", len(vector))

    print("\nFirst 10 values:")
    print(vector[:10])


if __name__ == "__main__":
    main()