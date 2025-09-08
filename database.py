# database.py
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone, date
from config import MONGO_URI, logger

client = AsyncIOMotorClient(MONGO_URI)

# If you provided MONGO_DBNAME use it; else try default database from URI; else fallback
DBNAME = os.getenv("MONGO_DBNAME")
if DBNAME:
    db = client[DBNAME]
else:
    try:
        db = client.get_default_database()  # works if URI contains /dbname
    except Exception:
        # fallback name
        db = client["telegram_bot"]

users_col = db.users

async def save_user(user_id, username=None, first_name=None, started_via="start"):
    now = datetime.now(timezone.utc)
    doc = {
        "user_id": user_id,
        "username": username,
        "first_name": first_name,
        "created_at": now,
        "last_seen": now,
        "active": True,
        "blocked": False,
        "via": started_via
    }
    try:
        await users_col.update_one({"user_id": user_id}, {"$set": doc, "$setOnInsert": {"created_at": now}}, upsert=True)
    except Exception as e:
        logger.error(f"DB save_user error: {e}")

async def mark_blocked(user_id):
    try:
        await users_col.update_one({"user_id": user_id}, {"$set": {"active": False, "blocked": True}})
    except Exception as e:
        logger.error(f"DB mark_blocked error: {e}")
