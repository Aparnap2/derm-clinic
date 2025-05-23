from flask import Blueprint, request, jsonify
from config.qdrant import get_qdrant_client
from config.database import get_pg_connection
from utils.embeddings import embed_text
from docling.document_converter import DocumentConverter
from datetime import datetime

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    user_id = request.form.get('user_id')
    file = request.files['file']
    converter = DocumentConverter()
    doc = converter.convert(file)
    chunks = [doc.text[i:i+512] for i in range(0, len(doc.text), 512)]
    
    qdrant_client = get_qdrant_client()
    qdrant_client.upload_collection(
        collection_name="medical_kb",
        documents=chunks,
        vectors=[embed_text(chunk) for chunk in chunks]
    )
    
    conn = get_pg_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO audit_logs (user_id, action, timestamp) VALUES (%s, %s, %s)",
                   (user_id, f'Uploaded PDF: {file.filename}', datetime.now()))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({'status': 'success'}), 200