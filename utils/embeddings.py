from google import generativeai as genai
import os
import numpy as np

class Embedder:
    def __init__(self):
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.client = genai.Client()

    def embed_text(self, text: str) -> np.ndarray:
        result = self.client.models.embed_content(
            model="gemini-embedding-exp-03-07",
            contents=text
        )
        return np.array(result.embeddings)

    def embed_query(self, query: str) -> np.ndarray:
        return self.embed_text(query)

embedder = Embedder()

def embed_text(text: str) -> np.ndarray:
    return embedder.embed_text(text)

def embed_query(query: str) -> np.ndarray:
    return embedder.embed_query(query)