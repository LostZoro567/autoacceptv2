# main.py
import asyncio
import signal
import logging
from pyrogram import Client
from pyrogram import idle

from config import API_ID, API_HASH, BOT_TOKEN, logger, PORT
from webserver import start_web_server
from handlers.join_request import register_join_handler
from handlers.start import register_start_handler
from handlers.admin import register_admin_handlers

# single Client instance used everywhere
app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


async def run_bot():
    # register handlers onto the same client
    register_join_handler(app)
    register_start_handler(app)
    register_admin_handlers(app)

    # start the client
    await app.start()
    me = await app.get_me()
    logger.info(f"✅ Bot started as @{me.username} (id: {me.id})")

    # keep the client alive
    await idle()
    # when idle returns, stop the client
    await app.stop()
    logger.info("Bot stopped.")


async def main():
    # start web server and bot concurrently
    await asyncio.gather(
        start_web_server(),  # non-blocking site.start()
        run_bot()
    )


if __name__ == "__main__":
    # proper signal handling: stop pyrogram gracefully
    loop = asyncio.get_event_loop()

    def _shutdown():
        try:
            loop.create_task(app.stop())
        except Exception:
            pass

    for s in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(s, _shutdown)
        except NotImplementedError:
            # windows or some envs
            pass

    try:
        loop.run_until_complete(main())
    except Exception as e:
        logger.exception("Fatal error in main: %s", e)
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
