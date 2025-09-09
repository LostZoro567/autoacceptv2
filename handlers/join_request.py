# handlers/join_request.py
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_USERNAME, JOIN_IMAGE, logger

def register_join_handler(app):
    @app.on_chat_join_request()
    async def handle_join(client, chat_join_request):
        user = chat_join_request.from_user
        try:
            await chat_join_request.approve()
            logger.info(f"Approved join request for {user.id}")

            # Send "Start Bot" button (no DB save here, only when they press /start)
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("▶ Start Bot", url=f"https://t.me/{BOT_USERNAME}?start=join")]
            ])

            await client.send_photo(
                chat_id=user.id,
                photo=JOIN_IMAGE,
                reply_markup=buttons
            )
            logger.info(f"Start button sent to {user.id}")
        except Exception as e:
            logger.error(f"Error approving/sending start to {user.id}: {e}")
