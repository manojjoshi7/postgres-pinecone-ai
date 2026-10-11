from app.rag.retriever import Retriever


def main():

    retriever = Retriever(top_k=5)

    question = (
        "Which products did customers buy for more than $100"
        
    )

    print("=" * 70)
    print("RAG RETRIEVER TEST")
    print("=" * 70)

    context = retriever.build_context(
        question
    )

    print("\nQUESTION:")
    print(question)

    print("\n" + "=" * 70)
    print("RETRIEVED CONTEXT")
    print("=" * 70)

    print(context)


if __name__ == "__main__":
    main()