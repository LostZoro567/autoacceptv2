# handlers/start.py
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import START_IMAGE, logger
from database import save_user, mark_blocked

def register_start_handler(app):
    @app.on_message(filters.private & filters.command("start"))
    async def start(client, message):
        user = message.from_user
        payload = message.command[1] if len(message.command) > 1 else "start"

        try:
            await save_user(user.id, user.username, user.first_name, started_via=payload)
        except Exception as e:
            logger.error(f"DB save error: {e}")

        text = f"Hello {user.first_name} 👋\nWelcome!"
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("My Profile", callback_data="profile")]])

        try:
            if START_IMAGE:
                await client.send_photo(user.id, START_IMAGE, caption=text, reply_markup=buttons)
            else:
                await client.send_message(user.id, text, reply_markup=buttons)
        except:
            await mark_blocked(user.id)
