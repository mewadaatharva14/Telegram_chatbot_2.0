
from telegram import Update
from telegram.ext import ContextTypes
from .chat import chat_response
from .news import get_latest_news
from .img2text import caption_image
from .text2img import generate_image
import os


user_chats = {}

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "My name is Atharva Mewada the CREATOR of this bot\n"
        "👋 Hi! I can:\n"
        "• Chat with you using DialoGPT\n"
        "• Convert images to text (send a photo)\n"
        "• Get latest news (@news)\n"
        "• Generate images (@image your prompt)\n"
        "\nTry them out!"
    )
    await update.message.reply_text(text)

async def img_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    path = f"temp_{photo.file_id}.jpg"
    await file.download_to_drive(path)

    caption = caption_image(path)
    if not caption or "Error" in caption:
        await update.message.reply_text("Failed to generate caption.")
    else:
        await update.message.reply_text(f" Caption: {caption}")
    os.remove(path)

async def news_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    articles = get_latest_news()
    await update.message.reply_text("📰 Latest News:\n" + "\n".join(articles))

async def txt2img_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text.partition(" ")[2]  
    await update.message.reply_text("🎨 Generating image, please wait...")
    img_path = generate_image(prompt, output_path=f"out_{update.message.message_id}.png")
    await update.message.reply_photo(photo=open(img_path, "rb"))
    os.remove(img_path)

async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.message.from_user.id
        text = update.message.text
        prev = user_chats.get(user_id)
        reply, chat_history = chat_response(text, prev)
        user_chats[user_id] = chat_history
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error in chat: {e}")
