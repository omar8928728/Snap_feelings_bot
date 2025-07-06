import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 مرحباً! أرسل لي رابط ستوري من سناب شات وسأنزّله لك.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "snapchat.com" in text:
        await update.message.reply_text("🔄 جارٍ التحميل...")
        url = get_download_link(text)
        if url:
            await update.message.reply_video(url)
        else:
            await update.message.reply_text("❌ ما قدرت أحصل الفيديو. تأكد أن الرابط صحيح.")
    else:
        await update.message.reply_text("📎 أرسل رابط سنابشات فقط.")

def get_download_link(snap_url):
    try:
        res = requests.post("https://api.allsnap.net/download", json={"url": snap_url})
        if res.status_code == 200:
            return res.json().get("videoUrl")
    except:
        return None
    return None

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
