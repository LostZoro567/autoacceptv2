# handlers/start.py
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import START_IMAGE, logger, BUTTON1_TEXT, BUTTON1_URL, BUTTON2_TEXT, BUTTON2_URL
from database import save_user, mark_blocked

def register_start_handler(app):
    # ping for quick test
    @app.on_message(filters.private & filters.command("ping"))
    async def ping_handler(client, message):
        try:
            await message.reply_text("pong")
            logger.info(f"Replied pong to {message.from_user.id}")
        except Exception as e:
            logger.error(f"Ping reply failed: {e}")

    @app.on_message(filters.private & filters.command("start"))
    async def start_handler(client, message):
        logger.info(f"/start received from {message.from_user.id}")
        user = message.from_user
        payload = message.command[1] if len(message.command) > 1 else "start"

        # Save the user (works for direct DM start and deep link start)
        try:
            await save_user(user.id, user.username, user.first_name, started_via=payload)
            logger.info(f"Saved user {user.id}")
        except Exception as e:
            logger.error(f"DB save error for {user.id}: {e}")

        text = (
            f"👋 Hello {user.first_name or ''}!\n\n"
            "Welcome to our bot. Here are some useful links:"
        )

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton(BUTTON1_TEXT, url=BUTTON1_URL)],
            [InlineKeyboardButton(BUTTON2_TEXT, url=BUTTON2_URL)],
        ])

        try:
            if START_IMAGE:
                await client.send_photo(user.id, START_IMAGE, caption=text, reply_markup=buttons)
                logger.info(f"Sent start image to {user.id}")
            else:
                await client.send_message(user.id, text, reply_markup=buttons)
                logger.info(f"Sent start text to {user.id}")
        except Exception as e:
            logger.error(f"Failed to send start message to {user.id}: {e}")
            await mark_blocked(user.id)
