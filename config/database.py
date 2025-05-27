import psycopg2
import redis
import os
from urllib.parse import urlparse

def get_pg_connection():
    """Create a connection to the PostgreSQL database."""
    return psycopg2.connect(
        dbname=os.getenv('PG_DBNAME', 'derm_clinic'),
        user=os.getenv('PG_USER', 'postgres'),
        password=os.getenv('PG_PASSWORD', 'securepass'),
        host=os.getenv('PG_HOST', 'localhost'),
        port=os.getenv('PG_PORT', '5432')
    )

def get_redis_client():
    """
    Create and return a Redis client instance.
    
    Environment variables required:
    - REDIS_HOST: Redis server host
    - REDIS_PORT: Redis server port
    - REDIS_PASSWORD: Redis server password (optional)
    - REDIS_SSL: Whether to use SSL (default: True)
    """
    host = os.getenv('REDIS_HOST', 'localhost')
    port = int(os.getenv('REDIS_PORT', '6379'))
    password = os.getenv('REDIS_PASSWORD')
    use_ssl = os.getenv('REDIS_SSL', 'true').lower() == 'true'
    
    return redis.Redis(
        host=host,
        port=port,
        password=password,
        ssl=use_ssl,
        ssl_cert_reqs=None,  # Disable certificate verification
        decode_responses=True  # Automatically decode responses to strings
    )

# Example usage:
if __name__ == "__main__":
    # Test Redis connection
    try:
        r = get_redis_client()
        r.ping()
        print("Successfully connected to Redis!")
        
        # Test set/get
        r.set('test_key', 'Hello, Redis!')
        print(f"Test value: {r.get('test_key')}")
    except Exception as e:
        print(f"Error connecting to Redis: {e}")