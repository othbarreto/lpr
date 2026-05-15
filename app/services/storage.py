import base64
import uuid
from pathlib import Path
from app.core.config import settings

def save_frame(b64: str, type: str) -> str:

    try:
        if "," in b64:
            b64 = b64.split(",")[1]

        img_data = base64.b64decode(b64)
    except Exception as e:
        raise ValueError("Invalid base64 string")
    
    filename = f"{uuid.uuid4()}.jpg"
    file_path = Path(settings.FRAMES_DIR) / type / filename

    with open(file_path, "wb") as f:
        f.write(img_data)

    return str(file_path)