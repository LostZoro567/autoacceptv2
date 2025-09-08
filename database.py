# database.py
from datetime import datetime, timezone, date
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI

client = AsyncIOMotorClient(MONGO_URI)
db = client.get_default_database()
users_col = db.users

async def save_user(user_id, username, first_name, started_via="start"):
    doc = {
        "user_id": user_id,
        "username": username,
        "first_name": first_name,
        "started_at": datetime.now(timezone.utc),
        "last_seen": datetime.now(timezone.utc),
        "active": True,
        "blocked": False,
        "via": started_via,
    }
    await users_col.update_one(
        {"user_id": user_id},
        {"$set": doc, "$setOnInsert": {"created_at": datetime.now(timezone.utc)}},
        upsert=True,
    )

async def mark_blocked(user_id):
    await users_col.update_one(
        {"user_id": user_id},
        {"$set": {"active": False, "blocked": True, "last_seen": datetime.now(timezone.utc)}},
    )

async def stats():
    total = await users_col.count_documents({})
    total_active = await users_col.count_documents({"active": True, "blocked": False})
    total_blocked = await users_col.count_documents({"blocked": True})
    today_start = await users_col.count_documents({
        "created_at": {"$gte": datetime.combine(date.today(), datetime.min.time()).replace(tzinfo=timezone.utc)}
    })
    return {"total": total, "active": total_active, "blocked": total_blocked, "today": today_start}

async def cleanup_blocked():
    res = await users_col.delete_many({"blocked": True})
    return res.deleted_count
