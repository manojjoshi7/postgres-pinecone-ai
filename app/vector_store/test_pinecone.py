from app.vector_store.pinecone_client import PineconeClient


def main():

    print("=" * 60)
    print("PINECONE CONNECTION TEST")
    print("=" * 60)

    client = PineconeClient()

    index = client.get_index()

    print("\nPinecone connection successful!")
    print("Index:", client.index_name)

    print("\nIndex statistics:")

    stats = index.describe_index_stats()

    print(stats)


if __name__ == "__main__":
    main()