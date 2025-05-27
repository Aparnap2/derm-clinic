# File: routes/rag.py

from flask import Blueprint, request, jsonify
from config.database import get_pg_connection, get_redis_client
from config.qdrant import get_qdrant_client
# Removed: from config.adk import get_patient_agent
from utils.embeddings import embed_query
from datetime import datetime

# New imports for LangChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage

rag_bp = Blueprint('rag', __name__)

# Initialize the LLM
# Ensure GOOGLE_API_KEY is set in your environment or .env file
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001")

# Define a prompt template
prompt_template = PromptTemplate.from_template(
    """Use the following context to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context:
{context}

Question: {question}

Answer:"""
)


@rag_bp.route('/rag', methods=['POST'])
def rag_query():
    data = request.json
    query = data['question']
    user_id = data['user_id']

    redis_client = get_redis_client()
    cache_key = f"rag:{query}:{user_id}"
    cached_response = redis_client.get(cache_key)
    if cached_response:
        # Decode the cached response before returning
        return jsonify({'response': cached_response.decode()}), 200

    qdrant_client = get_qdrant_client()
    vector = embed_query(query)
    results = qdrant_client.search(
        collection_name="medical_kb",
        query_vector=vector,
        limit=5
    )
    # Join the context snippets into a single string
    context = "\n\n".join([result.payload['text'] for result in results])

    # Create the prompt with context and query
    prompt_text = prompt_template.format(context=context, question=query)

    # Invoke the LLM
    messages = [HumanMessage(content=prompt_text)]
    llm_response = llm.invoke(messages)
    response = llm_response.content # Extract the content from the AIMessage object

    # Cache the response (encode before caching)
    redis_client.setex(cache_key, 3600, response.encode('utf-8'))

    conn = get_pg_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO queries (user_id, question, response, timestamp) VALUES (%s, %s, %s, %s)",
                   (user_id, query, response, datetime.now()))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'response': response}), 200
