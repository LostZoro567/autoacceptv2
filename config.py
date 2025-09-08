# config.py
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bot")

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
MONGO_URI = os.getenv("MONGO_URI", "")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))
BOT_USERNAME = os.getenv("BOT_USERNAME", "")
PORT = int(os.getenv("PORT", os.getenv("RENDER_PORT", 8000)))

WELCOME_IMAGE = os.getenv("WELCOME_IMAGE", "")
START_IMAGE = os.getenv("START_IMAGE", "")

# Inline button configs
BUTTON1_TEXT = os.getenv("BUTTON1_TEXT", "🌐 Visit Website")
BUTTON1_URL = os.getenv("BUTTON1_URL", "https://example.com")
BUTTON2_TEXT = os.getenv("BUTTON2_TEXT", "📢 Join Channel")
BUTTON2_URL = os.getenv("BUTTON2_URL", "https://t.me/examplechannel")

if not all([API_ID, API_HASH, BOT_TOKEN, MONGO_URI, OWNER_ID]):
    raise RuntimeError("Missing required environment variables")
