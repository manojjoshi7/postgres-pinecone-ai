import os

from ollama import Client


class OllamaLLM:

    def __init__(self):

        host = os.getenv(
            "OLLAMA_HOST",
            "http://ollama:11434"
        )

        self.model = os.getenv(
            "OLLAMA_MODEL",
            "llama3.2:3b"
        )

        self.client = Client(
            host=host
        )

    def generate(self, prompt):

        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]