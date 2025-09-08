# handlers/admin.py
import asyncio
from pyrogram import filters
from config import OWNER_ID, logger
from database import users_col, stats, cleanup_blocked, mark_blocked

def register_admin_handlers(app):
    @app.on_message(filters.private & filters.user(OWNER_ID) & filters.command("stats"))
    async def cmd_stats(client, message):
        s = await stats()
        await message.reply_text(f"📊 Stats\nTotal: {s['total']}\nActive: {s['active']}\nBlocked: {s['blocked']}\nToday: {s['today']}")

    @app.on_message(filters.private & filters.user(OWNER_ID) & filters.command("cleanup"))
    async def cmd_cleanup(client, message):
        deleted = await cleanup_blocked()
        await message.reply_text(f"Deleted {deleted} blocked users.")

    @app.on_message(filters.private & filters.user(OWNER_ID) & filters.command("broadcast"))
    async def cmd_broadcast(client, message):
        text = message.text.partition(" ")[2]
        if not text:
            return await message.reply_text("Usage: /broadcast <text>")

        sent, failed = 0, 0
        cursor = users_col.find({"active": True, "blocked": False})

        async for doc in cursor:
            try:
                await client.send_message(doc["user_id"], text)
                sent += 1
                await asyncio.sleep(0.1)
            except:
                failed += 1
                await mark_blocked(doc["user_id"])

        await message.reply_text(f"Broadcast done ✅\nSent: {sent}\nFailed: {failed}")
