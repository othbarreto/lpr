from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OCRReadingCreate(BaseModel):
    camera_id: str
    frame: str  # b64
    frame_plate: str    # b64

class OCRReadingResponse(BaseModel):
    id: int
    camera_id: str
    frame: Optional[str]
    frame_plate: Optional[str]
    plate: str
    status: str
    created_at: datetime
    updated_at: datetime