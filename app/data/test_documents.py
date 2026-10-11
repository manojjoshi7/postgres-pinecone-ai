from app.data.documents import get_documents_batch


def main():
    documents = get_documents_batch(0,5)

    print("=" * 70)
    print("POSTGRESQL → DOCUMENTS")
    print("=" * 70)

    print(f"\nDocuments created: {len(documents)}")

    for document in documents:
        print("\n" + "-" * 70)
        print("ID:", document["id"])
        print("\nTEXT:")
        print(document["text"])

        print("\nMETADATA:")
        print(document["metadata"])


if __name__ == "__main__":
    main()