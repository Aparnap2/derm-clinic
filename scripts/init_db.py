import psycopg2
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from config.qdrant import get_qdrant_client

def init_postgres():
    conn = psycopg2.connect(
        dbname="derm_clinic", user="postgres", password="securepass", host="localhost", port="5432"
    )
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id UUID PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100) UNIQUE,
            password VARCHAR(255),
            role VARCHAR(20)
        );
        
        CREATE TABLE IF NOT EXISTS queries (
            id SERIAL PRIMARY KEY,
            user_id UUID REFERENCES users(id),
            question TEXT,
            response TEXT,
            timestamp TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            phone_number VARCHAR(20),
            message TEXT,
            response TEXT,
            timestamp TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS audit_logs (
            id SERIAL PRIMARY KEY,
            user_id UUID,
            action TEXT,
            timestamp TIMESTAMP
        );
        
        INSERT INTO users (id, name, email, password, role)
        VALUES ('550e8400-e29b-41d4-a716-446655440000', 'Admin User', 'admin@clinic.com', 'secure123', 'admin')
        ON CONFLICT (email) DO NOTHING;
    """)
    
    conn.commit()
    cursor.close()
    conn.close()

def init_qdrant():
    client = get_qdrant_client()
    client.recreate_collection(
        collection_name="medical_kb",
        vectors_config=VectorParams(size=768, distance=Distance.COSINE)
    )

if __name__ == "__main__":
    init_postgres()
    init_qdrant()
    print("Database and Qdrant initialized successfully.")