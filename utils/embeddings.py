# File: utils/embeddings.py
import os
import numpy as np
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
load_dotenv()
# Initialize the embedding model
# Ensure GOOGLE_API_KEY is set in your environment or .env file
# Using a standard embedding model name
embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

def embed_text(text: str) -> np.ndarray:
    """
    Generates embeddings for a given text using LangChain's Google Generative AI embeddings.
    """
    # The LangChain embed_documents method expects a list of texts
    embeddings_list = embedding_model.embed_documents([text])
    # embed_documents returns a list of embeddings (one per document),
    # so we take the first element and convert it to a numpy array
    return np.array(embeddings_list[0])

def embed_query(query: str) -> np.ndarray:
    """
    Generates embeddings for a given query using LangChain's Google Generative AI embeddings.
    """
    # The LangChain embed_query method is designed for single queries
    embedding = embedding_model.embed_query(query)
    return np.array(embedding)

# The custom Embedder class is no longer needed
# The direct functions embed_text and embed_query now use the LangChain model
