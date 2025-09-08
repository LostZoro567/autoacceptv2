# main.py
import asyncio
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN, logger
from webserver import start_web_server
from handlers.join_request import register_join_handler
from handlers.start import register_start_handler
from handlers.admin import register_admin_handlers

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def main():
    # register handlers
    register_join_handler(app)
    register_start_handler(app)
    register_admin_handlers(app)

    # start aiohttp web server
    await start_web_server()

    # start bot
    await app.start()
    me = await app.get_me()
    logger.info(f"Bot started as @{me.username}")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
