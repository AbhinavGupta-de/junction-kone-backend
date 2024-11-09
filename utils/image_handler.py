# utils/image_handler.py
import shutil
from pathlib import Path


async def save_image_locally(image):
    save_path = Path("static/images") / image.filename
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    return str(save_path)
