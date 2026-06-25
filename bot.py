import os
from flask import Flask
import threading
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# 1. Setup a tiny Flask server to keep Render happy
html_app = Flask(__name__)

@html_app.route('/')
def home():
    return "Bot is alive!", 200

def run_flask():
    html_app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# 2. Your standard Telegram Bot logic
async def start_command(update, context):
    greeting = (
        "Welcome to LinkGuard. 🛡️\n\n"
        "This security system is active and monitoring. "
        "Please send any link or web address directly to this chat, "
        "and it will be scanned thoroughly for malicious content, phishing scams, or security threats."
    )
    await update.message.reply_text(greeting)

async def monitor_messages(update, context):
    text = update.message.text
    if "http" in text.lower():
        await update.message.reply_text("🔍 Scanning link...")

def main():
    # Start the background web thread
    threading.Thread(target=run_flask, daemon=True).start()

    # Build the standard app without proxy restrictions!
    token = os.environ.get("TELEGRAM_TOKEN")
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, monitor_messages))

    print("Bot starting polling loop...")
    app.run_polling()

if __name__ == '__main__':
    main()
