from fastapi import APIRouter, Depends
from psycopg2.extras import RealDictCursor
from app.core.database import get_db
from app.schemas.read import OCRReadingCreate, OCRReadingResponse
from app.services.storage import save_frame
from app.worker.queue import ocr_queue
from app.worker.processor import process_read

router = APIRouter(prefix="/reads", tags=["reads"])

@router.post("/", response_model=OCRReadingResponse)
def create_read(payload: OCRReadingCreate, db=Depends(get_db)):
    frame = save_frame(payload.frame, "frames")
    frame_plate = save_frame(payload.frame_plate, "plates")

    cursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        INSERT INTO ocr_readings (camera_id, frame, frame_plate, plate, status)
        VALUES (%s, %s, %s, %s, %s) RETURNING *
    """, (payload.camera_id, frame, frame_plate, payload.plate, payload.status))

    read = cursor.fetchone()
    db.commit()
    cursor.close()

    ocr_queue.enqueue(process_read, read["id"])

    return read

@router.get("/", response_model=list[OCRReadingResponse])
def get_reads(db=Depends(get_db)):

    cursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM ocr_readings ORDER BY created_at DESC")

    reads = cursor.fetchall()
    cursor.close()
    
    return reads