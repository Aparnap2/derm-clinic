from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Optional, Dict, Any
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class AIConfig(BaseModel):
    model: str = "gemini-2.0-flash"
    temperature: float = 0.7
    max_tokens: Optional[int] = 1000

def get_ai_client(config: Optional[Dict] = None) -> ChatGoogleGenerativeAI:
    if config is None:
        config = AIConfig().dict()
    
    # Get API key from environment variables
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables. Please set it in the .env file.")
    
    return ChatGoogleGenerativeAI(
        model=config["model"],
        temperature=config["temperature"],
        max_tokens=config["max_tokens"],
        google_api_key=api_key
    )
