import psycopg2
from app.core.config import settings

def init_db():
    conn = psycopg2.connect(settings.DATABASE_URL)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ocr_readings (
            id SERIAL PRIMARY KEY,
            camera_id VARCHAR NOT NULL,
            frame VARCHAR,
            frame_plate VARCHAR,
            plate VARCHAR DEFAULT 'PROCESSANDO',
            status VARCHAR DEFAULT 'PROCESSANDO',
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        );
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Database initialized!")

if __name__ == "__main__":
    init_db()