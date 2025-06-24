
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import config
from bot.handlers import start_handler, img_handler, news_handler, txt2img_handler, chat_handler

def main():
    app = ApplicationBuilder().token(config.BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(MessageHandler(filters.PHOTO, img_handler))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^@news'), news_handler))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^@image\s+'), txt2img_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_handler))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
