import ollama
import cv2
import os
from app.core.config import settings

def read_plate(frame_path: str) -> str:

    try:
        image = cv2.imread(frame_path)
        height, width = image.shape[:2]

        new_width = settings.OCR_IMAGE_WIDTH
        new_height = int((new_width / width) * height)

        resized_image = cv2.resize(image, (new_width, new_height))

        resized_image_path = frame_path.replace(".jpg", "_resized.jpg")
        cv2.imwrite(resized_image_path, resized_image)

        response = ollama.chat(
            model=settings.OCR_MODEL,
            messages=[{
                'role': 'user',
                'content': 'Read the license plate text in this image. Reply with ONLY the alphanumeric characters of the plate, no spaces, no explanation.',
                'image': resized_image_path
            }]

        )

        text = response['message']['content'].strip()

        os.remove(resized_image_path)

        if not text:
            return "NO RESULT"
        
        return text.upper()
    
    except Exception as e:
        print(f"❌ Erro no OCR: {e}")
        return "NO RESULT"

