# handlers/join_request.py
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.handlers import ChatJoinRequestHandler
from config import BOT_USERNAME, WELCOME_IMAGE, logger

async def handle_join_request(client, chat_join_request):
    try:
        # approve the join request (works with pyrogram ChatJoinRequest)
        await chat_join_request.approve()
        user = chat_join_request.from_user
        logger.info(f"Approved join request for {user.id}")

        payload = "auto_approved"
        start_link = f"https://t.me/{BOT_USERNAME}?start={payload}"
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("▶ Start Bot", url=start_link)]])

        if WELCOME_IMAGE:
            await client.send_photo(user.id, WELCOME_IMAGE, reply_markup=keyboard)
            logger.info(f"Sent welcome image to {user.id}")
        else:
            await client.send_message(user.id, "Click to start:", reply_markup=keyboard)
            logger.info(f"Sent fallback start message to {user.id}")

    except Exception as e:
        logger.error(f"Error in join_request handler for user {getattr(chat_join_request, 'from_user', None)}: {e}")

def register_join_handler(app):
    # register handler on provided app
    app.add_handler(ChatJoinRequestHandler(handle_join_request))
