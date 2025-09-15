# config.py
import os
import logging

# -----------------------
# Logging setup
# -----------------------
logging.basicConfig(
    format='[%(asctime)s] %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# -----------------------
# Telegram API credentials
# -----------------------
API_ID = int(os.getenv("API_ID", "12345"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# -----------------------
# MongoDB
# -----------------------
MONGO_URI = os.getenv("MONGO_URI", "")
MONGO_DBNAME = os.getenv("MONGO_DBNAME", "telegram_bot")

# -----------------------
# Admins (comma-separated user IDs)
# -----------------------
ADMINS = list(map(int, filter(None, os.getenv("ADMINS", "").split(","))))

# -----------------------
# Bot username
# -----------------------
BOT_USERNAME = os.getenv("BOT_USERNAME", "YourBotUsername")

# -----------------------
# Media & Messages
# -----------------------
# Join request welcome image
JOIN_IMAGE = os.getenv("JOIN_IMAGE", "https://example.com/join_image.jpg")

# Start command full message
START_IMAGE = os.getenv("START_IMAGE", "https://example.com/start_image.jpg")
START_TEXT = os.getenv(
    "START_TEXT",
    "🔞 𝘽𝙝𝙖𝙗𝙝𝙞 𝙇𝙤𝙫𝙚𝙧𝙨 😈😈\n https://t.me/+_eHCTEMA7zpjZTJl \n\n 🤒 𝘼𝙨𝙞𝙖𝙣 𝙊𝙣𝙡𝙮𝙛𝙖𝙣𝙨 🍑🍑 \n https://t.me/+n99vYeGDKoBmYTg1 \n\n 𝐅𝐮𝐥𝐥 𝐋𝐞𝐧𝐠𝐭𝐡 𝐇𝐞𝐧𝐭𝐚𝐢 💦 \n https://t.me/+9WOgYXXXJIE0ODY1 \n\n 🥵 𝐀𝐈 / 𝐃𝐫𝐞𝐬𝐬 𝐑𝐞𝐦𝐨𝐯𝐞𝐫 ☠️☠️ \n https://t.me/+eAtctmllKshmNTI1 \n\n 📹 𝗢𝗻𝗹𝗶𝗻𝗲 𝗖𝗮𝗺 𝗚𝗶𝗿𝗹 💦💦 \n https://t.me/+5VsHBPsaIl4xYTU1 \n\n 👅 𝐁𝐫𝐚𝐳𝐳𝐞𝐫𝐬 𝟒𝐤 𝐅𝐮𝐥𝐥 😻🫶🏻 \n https://t.me/+rzB9xKDJt4pmNDBl \n\n Promotion :- @fps244hz"
)

# Inline button 1
START_BTN1_TEXT = os.getenv("START_BTN1_TEXT", "📢 Updates Channel")
START_BTN1_URL = os.getenv("START_BTN1_URL", "https://t.me/your_channel")

# Inline button 2
START_BTN2_TEXT = os.getenv("START_BTN2_TEXT", "💬 Community Group")
START_BTN2_URL = os.getenv("START_BTN2_URL", "https://t.me/your_group")

# -----------------------
# Webserver (Render)
# -----------------------
PORT = int(os.getenv("PORT", "10000"))
