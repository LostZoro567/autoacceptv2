# handlers/admin.py
from pyrogram import filters
from config import ADMINS, logger
from database import stats, cleanup_blocked

def register_admin_handlers(app):
    @app.on_message(filters.command("stats") & filters.user(ADMINS))
    async def stats_handler(client, message):
        logger.info(f"/stats requested by {message.from_user.id}")
        s = await stats()
        text = (
            f"📊 Bot Stats:\n"
            f"👥 Total users: {s['total']}\n"
            f"🆕 Joined today: {s['today']}\n"
            f"🚫 Blocked users: {s['blocked']}"
        )
        await message.reply_text(text)

    @app.on_message(filters.command("cleanup") & filters.user(ADMINS))
    async def cleanup_handler(client, message):
        logger.info(f"/cleanup requested by {message.from_user.id}")
        removed = await cleanup_blocked()
        await message.reply_text(f"🧹 Cleanup complete!\n🗑 Removed {removed} blocked users")
