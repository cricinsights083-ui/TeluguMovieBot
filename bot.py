if __name__ == "__main__":

    async def main():
        bot.start_time = time.time()
        print(f"DEBUG: Active DB_CHANNEL_ID = {DB_CHANNEL_ID}")

        await bot.start()

        # Auto-set Bot Commands
        try:
            await bot.set_bot_commands(
                [BotCommand(c, d) for c, d in BOT_COMMANDS]
            )
            print("INFO: Bot Commands set successfully")
        except Exception as e:
            print(f"ERROR: Failed to set bot commands: {e}")

        try:
            await bot.send_message(
                OWNER_ID,
                f"✅ Bot Started Successfully\n\nDB Channel: `{DB_CHANNEL_ID}`"
            )
        except Exception:
            pass

        await idle()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
