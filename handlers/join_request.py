# handlers/join_request.py
from pyrogram.handlers import ChatJoinRequestHandler
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_USERNAME, WELCOME_IMAGE, logger

async def handle_join_request(client, chat_join_request):
    user = chat_join_request.from_user
    chat_id = chat_join_request.chat.id

    try:
        await client.approve_chat_join_request(chat_id, user.id)
        logger.info(f"Approved join request for {user.id}")

        payload = "welcome_from_channel"
        start_link = f"https://t.me/{BOT_USERNAME}?start={payload}"

        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("🚀 Start Bot", url=start_link)]]
        )

        if WELCOME_IMAGE:
            # Only image + button, no caption
            await client.send_photo(user.id, WELCOME_IMAGE, reply_markup=keyboard)
        else:
            # If no image set, fallback to just button
            await client.send_message(user.id, "Click below to start:", reply_markup=keyboard)

    except Exception as e:
        logger.error(f"Join request error: {e}")

def register_join_handler(app):
    app.add_handler(ChatJoinRequestHandler(handle_join_request))
