import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone, date
from config import MONGO_URI, logger

# Mongo client and collection
client = AsyncIOMotorClient(MONGO_URI)
DBNAME = os.getenv("MONGO_DBNAME", "telegram_bot")
db = client[DBNAME]
users_col = db.users

# Save a user
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
        await users_col.update_one(
            {"user_id": user_id},
            {"$set": doc, "$setOnInsert": {"created_at": now}},
            upsert=True
        )
    except Exception as e:
        logger.error(f"DB save_user error: {e}")

# Mark a user as blocked
async def mark_blocked(user_id):
    try:
        await users_col.update_one(
            {"user_id": user_id},
            {"$set": {"active": False, "blocked": True}}
        )
    except Exception as e:
        logger.error(f"DB mark_blocked error: {e}")

# Stats (for /stats)
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

# Cleanup blocked users
async def cleanup_blocked():
    try:
        result = await users_col.delete_many({"blocked": True})
        return result.deleted_count
    except Exception as e:
        logger.error(f"DB cleanup error: {e}")
        return 0
