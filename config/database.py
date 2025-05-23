import psycopg2
from upstash_redis import Redis
import os

def get_pg_connection():
    return psycopg2.connect(
        dbname=os.getenv('PG_DBNAME', 'derm_clinic'),
        user=os.getenv('PG_USER', 'postgres'),
        password=os.getenv('PG_PASSWORD', 'securepass'),
        host=os.getenv('PG_HOST', 'localhost'),
        port=os.getenv('PG_PORT', '5432')
    )

def get_redis_client():
    return Redis(
        url=os.getenv('UPSTASH_REDIS_URL'),
        token=os.getenv('UPSTASH_REDIS_TOKEN')
    )