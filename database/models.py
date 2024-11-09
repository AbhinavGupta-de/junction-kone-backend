# database/models.py

from database.connection import db
from bson import ObjectId

# Ensure indexes on the equipment collection


async def ensure_indexes():
    await db.equipment.create_index("location")
    await db.equipment.create_index([("location", 1), ("flags", 1)])

# Convert MongoDB document to dictionary


def equipment_helper(equipment) -> dict:
    return {
        "id": str(equipment["_id"]),
        "name": equipment["name"],
        "location": equipment["location"],
        "description": equipment["description"],
        "structured_description": equipment["structured_description"],
        "image_path": equipment["image_path"],
        "flags": equipment["flags"]
    }

# Function to save equipment data


async def save_equipment(data: dict):
    # Ensure indexes are created before the first insert
    await ensure_indexes()
    equipment = await db.equipment.insert_one(data)
    new_equipment = await db.equipment.find_one({"_id": equipment.inserted_id})
    return equipment_helper(new_equipment)

# Function to fetch equipment data by location and optional flags


async def fetch_equipment_by_location(location: str, flags: list = None):
    await ensure_indexes()  # Ensure indexes are set before queries
    query = {"location": location}
    if flags:
        # Ensures all flags in the list are matched
        query["flags"] = {"$all": flags}

    equipment_items = await db.equipment.find(query).to_list(length=100)
    return [equipment_helper(equipment) for equipment in equipment_items]
