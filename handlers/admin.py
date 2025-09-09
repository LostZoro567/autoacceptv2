# handlers/admin.py
from pyrogram import filters
from database import users_col, stats, cleanup_blocked, mark_blocked
from config import ADMINS, logger

def register_admin_handlers(app):
    # Broadcast
    @app.on_message(filters.command("broadcast") & filters.user(ADMINS))
    async def broadcast_handler(client, message):
        if not message.reply_to_message:
            await message.reply("⚠️ Reply to a message to broadcast it")
            return

        sent, failed = 0, 0
        async for user in users_col.find({"active": True, "blocked": False}):
            try:
                await message.reply_to_message.copy(user["user_id"])
                sent += 1
            except Exception:
                failed += 1
                await mark_blocked(user["user_id"])
        await message.reply(f"📢 Broadcast complete!\n✅ Sent: {sent}\n❌ Failed: {failed}")

    # Stats
    @app.on_message(filters.command("stats") & filters.user(ADMINS))
    async def stats_handler(client, message):
        data = await stats()
        await message.reply(
            f"📊 Stats:\n"
            f"👥 Total users: {data['total']}\n"
            f"🆕 Joined today: {data['today']}\n"
            f"🚫 Blocked users: {data['blocked']}"
        )

    # Cleanup
    @app.on_message(filters.command("cleanup") & filters.user(ADMINS))
    async def cleanup_handler(client, message):
        deleted = await cleanup_blocked()
        await message.reply(f"🧹 Cleanup complete!\n🗑️ Removed {deleted} blocked users")
