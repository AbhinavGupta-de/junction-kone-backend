# main.py

from fastapi import FastAPI
from routers import inventory  # Import your router
from database.connection import db  # Import db to handle startup/shutdown events

app = FastAPI()

# Include the router for inventory routes
app.include_router(inventory.router)

# Ensure database indexes on startup


@app.on_event("startup")
async def startup_db_client():
    await db.equipment.create_index("location")
    await db.equipment.create_index([("location", 1), ("flags", 1)])

# Close database connection on shutdown


@app.on_event("shutdown")
async def shutdown_db_client():
    db.client.close()
