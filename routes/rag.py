from flask import Blueprint, request, jsonify
from config.database import get_pg_connection, get_redis_client
from config.qdrant import get_qdrant_client
from config.adk import get_patient_agent
from utils.embeddings import embed_query
from datetime import datetime

rag_bp = Blueprint('rag', __name__)

@rag_bp.route('/rag', methods=['POST'])
def rag_query():
    data = request.json
    query = data['question']
    user_id = data['user_id']
    
    redis_client = get_redis_client()
    cache_key = f"rag:{query}:{user_id}"
    cached_response = redis_client.get(cache_key)
    if cached_response:
        return jsonify({'response': cached_response.decode()}), 200
    
    qdrant_client = get_qdrant_client()
    vector = embed_query(query)
    results = qdrant_client.search(
        collection_name="medical_kb",
        query_vector=vector,
        limit=5
    )
    context = [result.payload['text'] for result in results]
    
    agent = get_patient_agent()
    response = agent.run(query, context)
    
    redis_client.setex(cache_key, 3600, response)
    
    conn = get_pg_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO queries (user_id, question, response, timestamp) VALUES (%s, %s, %s, %s)",
                   (user_id, query, response, datetime.now()))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({'response': response}), 200