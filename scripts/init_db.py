#!/usr/bin/env python3
"""
Initialize the PostgreSQL database and Qdrant vector store.
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

import psycopg2
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from config.qdrant import get_qdrant_client

def init_postgres():
    """Initialize the PostgreSQL database with required tables."""
    try:
        # Get database connection parameters from environment variables
        db_params = {
            'dbname': os.getenv('PG_DBNAME', 'derm_clinic'),
            'user': os.getenv('PG_USER', 'postgres'),
            'password': os.getenv('PG_PASSWORD', 'securepass'),
            'host': os.getenv('PG_HOST', 'localhost'),
            'port': os.getenv('PG_PORT', '5432')
        }
        
        conn = psycopg2.connect(**db_params)
        conn.autocommit = False
        cursor = conn.cursor()
        
        print("Initializing PostgreSQL database...")
        
        # Create tables if they don't exist
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
            
            -- Add indexes for better query performance
            CREATE INDEX IF NOT EXISTS idx_messages_phone_number ON messages(phone_number);
            CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp);
            CREATE INDEX IF NOT EXISTS idx_queries_user_id ON queries(user_id);
            
            -- Insert default admin user if not exists
            INSERT INTO users (id, name, email, password, role)
            VALUES ('550e8400-e29b-41d4-a716-446655440000', 'Admin User', 'admin@clinic.com', 'secure123', 'admin')
            ON CONFLICT (email) DO NOTHING;
        """)
        
        conn.commit()
        print("PostgreSQL database initialized successfully.")
        
    except Exception as e:
        print(f"Error initializing PostgreSQL database: {str(e)}")
        if 'conn' in locals():
            conn.rollback()
        raise
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def init_qdrant():
    """Initialize the Qdrant vector store with required collections."""
    try:
        print("Initializing Qdrant vector store...")
        qdrant_client = get_qdrant_client()
        
        # Create collections if they don't exist
        collections = qdrant_client.get_collections()
        collection_names = [collection.name for collection in collections.collections]
        
        # Example: Create a collection for document embeddings
        if "documents" not in collection_names:
            qdrant_client.create_collection(
                collection_name="documents",
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )
            print("Created 'documents' collection in Qdrant.")
        else:
            print("'documents' collection already exists in Qdrant.")
            
    except Exception as e:
        print(f"Error initializing Qdrant: {str(e)}")
        raise

if __name__ == "__main__":
    # Load environment variables from .env file if it exists
    from dotenv import load_dotenv
    load_dotenv()
    
    try:
        init_postgres()
        init_qdrant()
        print("Database and Qdrant initialization completed successfully!")
    except Exception as e:
        print(f"Initialization failed: {str(e)}")
        sys.exit(1)