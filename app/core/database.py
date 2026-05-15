import psycopg2
from psycopg2.extras import RealDictCursor
from app.core.config import settings

def get_db_connection():
    try:
        conn = psycopg2.connect(
            settings.DATABASE_URL,
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None
    
def get_db():
    conn = get_db_connection()
    if conn is None:
        raise Exception("Could not connect to the database")
    try:
        yield conn
    finally:
        conn.close()