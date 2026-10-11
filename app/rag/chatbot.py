from app.rag.retriever import Retriever
from app.rag.prompt import build_prompt
from app.llm.ollama_llm import OllamaLLM


class RAGChatbot:

    def __init__(self, top_k=5):
        print("Initializing RAG Chatbot...")

        self.retriever = Retriever(
            top_k = top_k
        )

        self.llm = OllamaLLM()

        print("RAG Chatbot initialized.")

    def ask(self, question):

        print("\n" + "=" * 70)
        print("RAG PIPELINE")
        print("=" * 70)

        # 1. Retrieve relevant documents
        print("\n[1] Retrieving documents...")

        context = self.retriever.build_context(
            question
        )

        # 2. Build prompt
        print("\n[2] Building prompt...")

        prompt = build_prompt(
            question,
            context
        )

        # 3. Send prompt to Ollama
        print("\n[3] Sending prompt to Ollama...")

        answer = self.llm.generate(
            prompt
        )

        return {
            "question": question,
            "context": context,
            "prompt": prompt,
            "answer": answer
        }


def main():

    chatbot = RAGChatbot(
        top_k=5
    )

    question = (
        "How many customers spent more than $100?"
        )

    result = chatbot.ask(
        question
    )

    print("\n" + "=" * 70)
    print("FINAL ANSWER")
    print("=" * 70)

    print("\nQuestion:")
    print(result["question"])

    print("\nAnswer:")
    print(result["answer"])

    print("\n" + "=" * 70)
    print("RETRIEVED CONTEXT")
    print("=" * 70)

    print(result["context"])


if __name__ == "__main__":
    main()