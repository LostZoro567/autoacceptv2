# handlers/start.py
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import save_user
from config import START_IMAGE, START_TEXT, START_BTN1_TEXT, START_BTN1_URL, START_BTN2_TEXT, START_BTN2_URL, logger

def register_start_handler(app):
    @app.on_message(filters.private & filters.command("start"))
    async def start_command(client, message):
        user_id = message.from_user.id
        await save_user(user_id, started_via="start")

        try:
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton(START_BTN1_TEXT, url=START_BTN1_URL)],
                [InlineKeyboardButton(START_BTN2_TEXT, url=START_BTN2_URL)]
            ])
            await client.send_photo(
                chat_id=user_id,
                photo=START_IMAGE,
                caption=START_TEXT,
                reply_markup=buttons
            )
            logger.info(f"/start sent to {user_id}")
        except Exception as e:
            logger.error(f"Error sending /start response to {user_id}: {e}")
