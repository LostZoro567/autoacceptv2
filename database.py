from datetime import datetime, timezone, date

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

async def cleanup_blocked():
    try:
        result = await users_col.delete_many({"blocked": True})
        return result.deleted_count
    except Exception as e:
        logger.error(f"DB cleanup error: {e}")
        return 0
