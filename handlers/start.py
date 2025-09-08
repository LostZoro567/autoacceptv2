# handlers/start.py
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import (
    START_IMAGE,
    logger,
    BUTTON1_TEXT, BUTTON1_URL,
    BUTTON2_TEXT, BUTTON2_URL
)
from database import save_user, mark_blocked

def register_start_handler(app):
    @app.on_message(filters.private & filters.command("start"))
    async def start(client, message):
        user = message.from_user
        payload = message.command[1] if len(message.command) > 1 else "start"

        # Always save user (direct /start or via button link)
        try:
            await save_user(user.id, user.username, user.first_name, started_via=payload)
        except Exception as e:
            logger.error(f"DB save error: {e}")

        # Custom welcome text
        text = (
            f"👋 Hello {user.first_name or ''}!\n\n"
            "Welcome to our bot. Here are some useful links:"
        )

        # Inline buttons from env
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton(BUTTON1_TEXT, url=BUTTON1_URL)],
            [InlineKeyboardButton(BUTTON2_TEXT, url=BUTTON2_URL)],
        ])

        try:
            if START_IMAGE:
                await client.send_photo(user.id, START_IMAGE, caption=text, reply_markup=buttons)
            else:
                await client.send_message(user.id, text, reply_markup=buttons)
        except:
            await mark_blocked(user.id)
