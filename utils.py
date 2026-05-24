import asyncio
from pyrogram.errors import MessageNotModified, FloodWait

async def safe_edit(message, text, reply_markup=None):
    try:
        return await message.edit_text(text, reply_markup=reply_markup)
    except MessageNotModified:
        return message
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await safe_edit(message, text, reply_markup)
    except Exception:
        return message

async def safe_reply(message, text, reply_markup=None):
    try:
        return await message.reply_text(text, reply_markup=reply_markup)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await safe_reply(message, text, reply_markup)
    except Exception:
        return None

def style_text(text: str):
    """
    Converts text to Small Caps and Bolds it. Monospace removed as per user request.
    """
    if not text: return text

    # Simple Small Caps mapping
    small_caps = {
        'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ғ', 'g': 'ɢ', 'h': 'ʜ',
        'i': 'ɪ', 'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ', 'p': 'ᴘ',
        'q': 'ǫ', 'r': 'ʀ', 's': 's', 't': 'ᴛ', 'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x',
        'y': 'ʏ', 'z': 'ᴢ',
        'A': 'ᴀ', 'B': 'ʙ', 'C': 'ᴄ', 'D': 'ᴅ', 'E': 'ᴇ', 'F': 'ғ', 'G': 'ɢ', 'H': 'ʜ',
        'I': 'ɪ', 'J': 'ᴊ', 'K': 'ᴋ', 'L': 'ʟ', 'M': 'ᴍ', 'N': 'ɴ', 'O': 'ᴏ', 'P': 'ᴘ',
        'Q': 'ǫ', 'R': 'ʀ', 'S': 's', 'T': 'ᴛ', 'U': 'ᴜ', 'V': 'ᴠ', 'W': 'ᴡ', 'X': 'x',
        'Y': 'ʏ', 'Z': 'ᴢ'
    }

    styled_chars = []
    for char in text:
        styled_chars.append(small_caps.get(char, char))

    styled_text = "".join(styled_chars)
    return f"**{styled_text}**"

def style_btn(text: str):
    """
    Converts button text to Small Caps (no bold/backticks).
    """
    if not text: return text

    small_caps = {
        'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ғ', 'g': 'ɢ', 'h': 'ʜ',
        'i': 'ɪ', 'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ', 'p': 'ᴘ',
        'q': 'ǫ', 'r': 'ʀ', 's': 's', 't': 'ᴛ', 'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x',
        'y': 'ʏ', 'z': 'ᴢ',
        'A': 'ᴀ', 'B': 'ʙ', 'C': 'ᴄ', 'D': 'ᴅ', 'E': 'ᴇ', 'F': 'ғ', 'G': 'ɢ', 'H': 'ʜ',
        'I': 'ɪ', 'J': 'ᴊ', 'K': 'ᴋ', 'L': 'ʟ', 'M': 'ᴍ', 'N': 'ɴ', 'O': 'ᴏ', 'P': 'ᴘ',
        'Q': 'ǫ', 'R': 'ʀ', 'S': 's', 'T': 'ᴛ', 'U': 'ᴜ', 'V': 'ᴠ', 'W': 'ᴡ', 'X': 'x',
        'Y': 'ʏ', 'Z': 'ᴢ'
    }

    styled_chars = []
    for char in text:
        styled_chars.append(small_caps.get(char, char))

    return "".join(styled_chars)

def parse_duration(duration_str: str):
    """
    Parses duration string like '30s', '1m', '1h', '1d' into seconds.
    Returns 0 if '0' or invalid.
    """
    if not duration_str or duration_str == "0":
        return 0

    unit = duration_str[-1].lower()
    try:
        value = int(duration_str[:-1])
    except ValueError:
        return 0

    if unit == 's': return value
    if unit == 'm': return value * 60
    if unit == 'h': return value * 3600
    if unit == 'd': return value * 86400

    return 0

async def auto_delete_messages(client, chat_id, message_ids, delay):
    """
    Sleeps for delay and deletes provided message_ids.
    """
    if delay <= 0: return
    await asyncio.sleep(delay)
    try:
        await client.delete_messages(chat_id, message_ids)
    except Exception:
        pass
