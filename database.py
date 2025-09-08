# database.py
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone, date
from config import MONGO_URI, MONGO_DBNAME, logger

# -----------------------
# MongoDB setup
# -----------------------
client = AsyncIOMotorClient(MONGO_URI)
DBNAME = MONGO_DBNAME or "telegram_bot"
db = client[DBNAME]
users_col = db.users

# -----------------------
# Save a user (conflict-free)
# -----------------------
async def save_user(user_id, username=None, first_name=None, started_via="start"):
    now = datetime.now(timezone.utc)
    doc_set = {
        "user_id": user_id,
        "username": username,
        "first_name": first_name,
        "last_seen": now,
        "active": True,
        "blocked": False,
        "via": started_via
    }
    try:
        await users_col.update_one(
            {"user_id": user_id},
            {"$set": doc_set, "$setOnInsert": {"created_at": now}},
            upsert=True
        )
        logger.info(f"User {user_id} saved/updated successfully")
    except Exception as e:
        logger.error(f"DB save_user error for {user_id}: {e}")

# -----------------------
# Mark user as blocked
# -----------------------
async def mark_blocked(user_id):
    try:
        await users_col.update_one(
            {"user_id": user_id},
            {"$set": {"active": False, "blocked": True}}
        )
        logger.info(f"User {user_id} marked as blocked")
    except Exception as e:
        logger.error(f"DB mark_blocked error for {user_id}: {e}")

# -----------------------
# Stats: total, today, blocked
# -----------------------
async def stats():
    try:
        total = await users_col.count_documents({})
        today = date.today()
        today_count = await users_col.count_documents({
            "created_at": {"$gte": datetime(today.year, today.month, today.day, tzinfo=timezone.utc)}
        })
        blocked = await users_col.count_documents({"blocked": True})
        return {"total": total, "today": today_count, "blocked": blocked}
    except Exception as e:
        logger.error(f"DB stats error: {e}")
        return {"total": 0, "today": 0, "blocked": 0}

# -----------------------
# Cleanup blocked users
# -----------------------
async def cleanup_blocked():
    try:
        result = await users_col.delete_many({"blocked": True})
        logger.info(f"Cleanup complete, removed {result.deleted_count} blocked users")
        return result.deleted_count
    except Exception as e:
        logger.error(f"DB cleanup error: {e}")
        return 0
