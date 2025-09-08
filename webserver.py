# webserver.py
from aiohttp import web
import os
from config import logger

async def handle_root(request):
    return web.Response(text="Bot running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle_root)

    port = int(os.getenv("PORT", os.getenv("RENDER_PORT", 8000)))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logger.info(f"HTTP server started on port {port}")
