import os
import logging

# -----------------------
# Telegram API / Bot
# -----------------------
API_ID = int(os.getenv("API_ID", "123456"))  # replace with your default/test ID if needed
API_HASH = os.getenv("API_HASH", "your_api_hash")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")
BOT_USERNAME = os.getenv("BOT_USERNAME", "YourBotUsername")

# -----------------------
# MongoDB
# -----------------------
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DBNAME = os.getenv("MONGO_DBNAME", "telegram_bot")

# -----------------------
# Admins
# -----------------------
# comma-separated list of Telegram user IDs
ADMINS_ENV = os.getenv("ADMINS", "")
ADMINS = list(map(int, filter(None, ADMINS_ENV.split(","))))

# -----------------------
# Webserver / Render
# -----------------------
PORT = int(os.getenv("PORT", 10000))  # default Render port

# -----------------------
# Start / Welcome images & buttons
# -----------------------
START_IMAGE = os.getenv(
    "START_IMAGE",
    "https://graph.org/file/a632ff5bfea88c2e3bc4e-fc860032d437a5d866.jpg"
)
WELCOME_IMAGE = os.getenv(
    "WELCOME_IMAGE",
    "https://graph.org/file/5c159e3cb5694e24aefe2-34301124b07248c91f.jpg"
)

# Inline button texts and URLs (set in environment for easy changes)
BUTTON1_TEXT = os.getenv("BUTTON1_TEXT", "📢 Updates Channel")
BUTTON1_URL = os.getenv("BUTTON1_URL", "https://t.me/YourChannel")
BUTTON2_TEXT = os.getenv("BUTTON2_TEXT", "💬 Community Group")
BUTTON2_URL = os.getenv("BUTTON2_URL", "https://t.me/YourGroup")

# -----------------------
# Logging setup
# -----------------------
logging.basicConfig(
    format='[%(asctime)s] %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
