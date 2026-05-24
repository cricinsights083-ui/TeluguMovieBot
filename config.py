#========================================================================
# Don't Remove Credit Tg - @TDBotDev
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@TDBotDev
# Ask Doubt on telegram https://t.me/TDBotDev
#========================================================================
import os
import random
from dotenv import load_dotenv

# config.py
load_dotenv()

API_ID = int(os.environ.get("API_ID", )
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# Search Settings
DB_CHANNEL_ID = int(os.environ.get("DB_CHANNEL_ID", -100))
START_TEXT = os.environ.get("START_TEXT", "🚀 Welcome to Movie Serch \n\n🎬 Movies • Series • Anime • Episodes — All in One Place\n⚡ Lightning Fast Search with Smart Auto Filters\n🧠 Auto Detect Language • Quality • Seasons\n\n📂 Continue Watching • 🔥 Trending • ▶️ One Click Play\n\n🔍 Just send any name (movie / series / file) to start exploring")
MAX_RESULTS = int(os.environ.get("MAX_RESULTS", 10))

# Help and About Texts
HELP_TEXT = os.environ.get("HELP_TEXT", "📖 **Help Menu**\n\n1. Send any movie or series name to search.\n2. Use the quality and language filters to narrow down results.\n3. Click on the file name to receive it instantly.")
ABOUT_TEXT = os.environ.get("ABOUT_TEXT", "❄️ **About This Bot**\n\nThis is a high-speed file storage and search bot for CineVerse users. It indexes thousands of files and provides them with minimal delay.\n\nDeveloper: [ @TDBotDev ]")

# Database Settings
MONGO_URI = os.environ.get("MONGO_URI", "")
DATABASE_NAME = os.environ.get("DATABASE_NAME", "autofilebot")
COLLECTION_NAME = "files"

# Optional settings
OWNER_ID = int(os.environ.get("OWNER_ID", 1573111356))
ADMINS = [int(x) for x in os.environ.get("ADMINS", "1573111356").split(",") if x]  # multiple admins allowed ("8475661555","8475661555")

# Force Subscribe Settings
# Updated to multiple channels as per user request
FORCE_SUB_CHANNELS = [int(x) for x in os.environ.get("FORCE_SUB_CHANNELS", "-100").split(",") if x] # multiple force sub allowed ("-1003511440278",-1003511440278")
ADMIN_IDS = ADMINS + [OWNER_ID]
FORCE_SUB_TEXT = os.environ.get("FORCE_SUB_TEXT", "📥 **Please join our channels to use this bot!**\n\nDue to high server load, only subscribers can search files.")

# Updates Link
UPDATES = os.environ.get("UPDATES", "https://t.me/Team_TD_Link")

# Auto-Delete Settings
AUTO_DELETE_TIME = os.environ.get("AUTO_DELETE_TIME", "30s") # Format: 30s, 1m, 1h, 1d or '0' to disable
DELETE_MESSAGE_TEXT = "⚠️ <b><u>IMPORTANT:</u></b>\n\n<i>ᴀʟʟ ᴍᴇssᴀɢᴇs ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ ᴀғᴛᴇʀ {time}. ᴘʟᴇᴀsᴇ sᴀᴠᴇ ᴏʀ ғᴏʀᴡᴀʀᴅ ᴛʜᴇᴍ ᴛᴏ ʏᴏᴜʀ sᴀᴠᴇᴅ ᴍᴇssᴀɢᴇs.</i>"

# UI Images
PICS = [
    "https://ibb.co/39zW3dNh",
    "https://ibb.co/v4FX9rMN",
    "https://ibb.co/8L9rDmB4",
    "https://ibb.co/kVTGm4Rn",
    "https://ibb.co/Hff6FyNH",
    "https://ibb.co/DDRzKfv5",
    "https://ibb.co/Y7ds8xGg",
    "https://ibb.co/0jY0HHND",
    "https://ibb.co/Z1kCz73X"
]

def get_random_pic():
    return random.choice(PICS)

# Initial images
START_PIC = PICS[0]
FORCE_PIC = PICS[1]

# Bot Commands
BOT_COMMANDS = [
    ("start", "🚀 Start the bot"),
    ("help", "🆘 How to use the bot"),
    ("delete_file", "🗑️ Delete your DB files (admin)"),
    ("broadcast", "⚡ Broadcast message (admin)"),
    ("status", "👀 Bot statistics (admin)"),
    ("reset", "❌ Total reset (only owner)")
]

#========================================================================
# Don't Remove Credit Tg - @TDBotDev
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@TDBotDev
# Ask Doubt on telegram https://t.me/TDBotDev
#========================================================================
