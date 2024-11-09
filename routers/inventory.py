# routers/inventory.py
from fastapi import APIRouter, Query
from fastapi import UploadFile, File, Form
from services.llm_service import process_description
from database.models import save_equipment
from utils.image_handler import save_image_locally
from database.models import fetch_equipment_by_location

router = APIRouter()


@router.get("/inventory/")
async def get_inventory(location: str, flags: list[str] = Query(None)):
    items = await fetch_equipment_by_location(location, flags)
    return {"items": items}


@router.post("/inventory/")
async def add_inventory(
    name: str = Form(...),
    location: str = Form(...),
    description: str = Form(...),
    image: UploadFile = File(...)
):
    # Save the image to server storage temporarily
    image_path = await save_image_locally(image)

    # Process description through LLM to get structured data and flags
    # structured_description, flags = await process_description(description)

    # Create data dictionary to save in the database
    equipment_data = {
        "name": name,
        "location": location,
        "description": description,
        "structured_description": description,
        "image_path": image_path,
        "flags": []  # Update with extracted flags
    }

    # Save data to the database
    await save_equipment(equipment_data)
    return {"message": "Inventory item added successfully"}
