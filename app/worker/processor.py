import psycopg2
from datetime import datetime
from app.core.config import settings
from app.services.ocr import read_plate

def process_read(read_id: int):

    try:
        conn = psycopg2.connect(settings.DATABASE_URL)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM ocr_readings WHERE id = %s", (read_id,))
        read = cursor.fetchone()

        if not read:
            print(f"❌ Read with ID {read_id} not found.")
            return
        
        frame_path = read[3]

        print(f"🔍 Processing read ID {read_id} with frame {frame_path}...")

        plate_text = read_plate(frame_path)

        status = "CONCLUIDO" if plate_text != "NO RESULT" else "NO RESULT"

        cursor.execute("""
            UPDATE ocr_readings
            SET plate = %s, status = %s, updated_at = %s
            WHERE id = %s
        """,
        (plate_text, status, datetime.utcnow(), read_id))

        conn.commit()
        print(f"✅ Read ID {read_id} processed with plate: {plate_text}")

    except Exception as e:
        print(f"❌ Error processing read ID {read_id}: {e}")
        cursor.execute("""
                    UPDATE ocr_readings
                    SET plate = 'NO_RESULT', status = 'NO_RESULT', updated_at = %s
                    WHERE id = %s
        """, 
        (datetime.now(), read_id))
        conn.commit()

    finally:
        cursor.close()
        conn.close()
