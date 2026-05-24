import asyncio
import os
import threading
from pyrogram import Client, filters, idle
from pyrogram.types import BotCommand
from config import API_ID, API_HASH, BOT_TOKEN, DB_CHANNEL_ID, OWNER_ID, BOT_COMMANDS
from Database.database import add_file, get_file_by_db_id, search_files_fuzzy, get_nav_state
from utils import safe_reply, parse_duration, auto_delete_messages, style_text, style_btn
from app import app
from TDBotDev.forcesub import force_sub
from config import AUTO_DELETE_TIME, DELETE_MESSAGE_TEXT, UPDATES
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import datetime
import time

# Initialize Bot
bot = Client(
    "file_store_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="TDBotDev")
)

def run_flask():
    # Flask for Render keep-alive
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Real-time Channel Indexing handler
@bot.on_message(filters.chat(DB_CHANNEL_ID) & (filters.document | filters.video | filters.audio))
async def channel_index_handler(client, message):
    media = message.document or message.video or message.audio
    file_id = media.file_id
    file_name = getattr(media, "file_name", "document_file")

    await add_file(file_id, file_name, message.caption, message_id=message.id, channel_id=DB_CHANNEL_ID)

# Callback routing - handlers are now in plugins
# But centralized f# stays here for stability across all modes.

# Centralized File Delivery Callback
@bot.on_callback_query(filters.regex(r"^sall#"))
async def send_all_callback_handler(client, cb):
    # Force Subscribe Check
    if not await force_sub(client, cb.message, user_id=cb.from_user.id):
        return

    key = cb.data.split("#")[1]
    state = await get_nav_state(key)
    if not state:
        await cb.answer("Session expired", show_alert=True)
        return

    from config import MAX_RESULTS
    q, qu, l, pg = state["q"], state["qu"], state["l"], state["pg"]
    results, _ = await search_files_fuzzy(q, quality=qu, language=l, skip=pg*MAX_RESULTS, limit=MAX_RESULTS)

    if not results:
        await cb.answer("No files to send", show_alert=True)
        return

    await cb.answer("Sending all files...", show_alert=False)

    sent_msg_ids = [cb.message.id]
    for f in results:
        file_id = f['file_id']
        file_name = f['file_name']
        full_info = await get_file_by_db_id(str(f['_id']))
        caption = full_info.get('caption') or file_name
        m_id = full_info.get('message_id')
        c_id = full_info.get('channel_id')

        try:
            if m_id and c_id:
                m = await client.copy_message(chat_id=cb.message.chat.id, from_chat_id=c_id, message_id=m_id, caption=caption)
            else:
                m = await client.send_document(chat_id=cb.message.chat.id, document=file_id, caption=caption)
            sent_msg_ids.append(m.id)
            await asyncio.sleep(0.5)
        except Exception as e:
            print(f"Batch Send Error: {e}")
            try:
                m = await client.send_document(chat_id=cb.message.chat.id, document=file_id, caption=caption)
                sent_msg_ids.append(m.id)
            except:
                pass

    # Handle Auto-Delete
    delay = parse_duration(AUTO_DELETE_TIME)
    if delay > 0:
        readable_time = AUTO_DELETE_TIME.replace("s", " Seconds").replace("m", " Minutes").replace("h", " Hours").replace("d", " Days")
        text = style_text(DELETE_MESSAGE_TEXT.format(time=readable_time))
        btn = InlineKeyboardMarkup([[InlineKeyboardButton(style_btn("📟 UPDATE CHANNEL"), url=UPDATES)]])
        info_msg = await client.send_message(cb.message.chat.id, text, reply_markup=btn)
        sent_msg_ids.append(info_msg.id)
        asyncio.create_task(auto_delete_messages(client, cb.message.chat.id, sent_msg_ids, delay))

@bot.on_callback_query(filters.regex(r"^f#"))
async def file_callback_handler(client, cb):
    # Force Subscribe Check
    if not await force_sub(client, cb.message, user_id=cb.from_user.id):
        return

    db_id = cb.data.split("#")[1]
    file_info = await get_file_by_db_id(db_id)
    if not file_info:
        await cb.answer("File not available", show_alert=True)
        return
    file_id = file_info['file_id']
    file_name = file_info['file_name']
    caption = file_info.get('caption') or file_name

    try:
        m_id = file_info.get('message_id')
        c_id = file_info.get('channel_id')

        # Try copy_message for reliability
        if m_id and c_id:
            try:
                m = await client.copy_message(chat_id=cb.message.chat.id, from_chat_id=c_id, message_id=m_id, caption=caption)
            except Exception:
                m = await client.send_document(chat_id=cb.message.chat.id, document=file_id, caption=caption)
        else:
            m = await client.send_document(chat_id=cb.message.chat.id, document=file_id, caption=caption)

        await cb.answer()

        # Handle Auto-Delete
        delay = parse_duration(AUTO_DELETE_TIME)
        if delay > 0:
            sent_msg_ids = [cb.message.id, m.id]
            readable_time = AUTO_DELETE_TIME.replace("s", " Seconds").replace("m", " Minutes").replace("h", " Hours").replace("d", " Days")
            text = style_text(DELETE_MESSAGE_TEXT.format(time=readable_time))
            btn = InlineKeyboardMarkup([[InlineKeyboardButton(style_btn("📟 UPDATE CHANNEL"), url=UPDATES)]])
            info_msg = await client.send_message(cb.message.chat.id, text, reply_markup=btn)
            sent_msg_ids.append(info_msg.id)
            asyncio.create_task(auto_delete_messages(client, cb.message.chat.id, sent_msg_ids, delay))

    except Exception as e:
        print(f"File Send Error: {e}")
        await cb.answer("Error sending file", show_alert=True)

if __name__ == "__main__":
    # Start Flask in background thread if not running in production Gunicorn
    import os
    if not os.environ.get("GUNICORN_RUNNING"):
        threading.Thread(target=run_flask, daemon=True).start()

    async def main():
        bot.start_time = time.time()
        print(f"DEBUG: Active DB_CHANNEL_ID = {DB_CHANNEL_ID}")
        await bot.start()

        # Auto-set Bot Commands
        try:
            await bot.set_bot_commands([BotCommand(c, d) for c, d in BOT_COMMANDS])
            print("INFO: Bot Commands set successfully")
        except Exception as e:
            print(f"ERROR: Failed to set bot commands: {e}")

        try:
            await bot.send_message(OWNER_ID, f"**bot started successfully with ForceSub & Web Service ✅**\n\n**Configured Channel ID:** `{DB_CHANNEL_ID}`")
        except Exception:
            pass
        await idle()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

#========================================================================
# Don't Remove Credit Tg - @TDBotDev
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@TDBotDev
# Ask Doubt on telegram https://t.me/TDBotDev
#========================================================================
