from app.search.semantic_search import SemanticSearch


class Retriever:

    def __init__(self, top_k=5):

        self.top_k = top_k
        self.search = SemanticSearch()

    def retrieve(self, question):

        results = self.search.search(
            question,
            top_k=self.top_k
        )

        documents = []

        for match in results.matches:

            metadata = match.metadata or {}

            documents.append({
                "id": match.id,
                "score": match.score,
                "text": metadata.get("text", ""),
                "metadata": metadata,
            })

        return documents

    def build_context(self, question):

        documents = self.retrieve(question)

        if not documents:
            return "No relevant information was found."

        context_parts = []

        for index, document in enumerate(
            documents,
            start=1
        ):

            context_parts.append(
                f"""
Document {index}
Similarity: {document['score']:.4f}

{document['text']}
""".strip()
            )

        return "\n\n".join(context_parts)