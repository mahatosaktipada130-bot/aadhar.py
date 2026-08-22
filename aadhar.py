import os
import logging
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Configuration Variables
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8640207091:AAGzbEZWsfBEX3okHKb0ZUjfU4Uvj5G_Ig4")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "8640207091"))
ADMIN_USERNAME = "ecbots3004"
BOT_USERNAME = "ecaadharbot"

# Flask Web Server for Render binding
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running live on Render!"

# Command Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Namaste {user.first_name}!\n\n"
        f"Welcome to @{BOT_USERNAME}.\n"
        f"Aap yahan e-Aadhaar ki services access kar sakte hain.\n\n"
        f"Kisi bhi madad ke liye Admin (@{ADMIN_USERNAME}) se sampark karein."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Aap /start daba kar bot ka upyog kar sakte hain.\n"
        f"Support: @{ADMIN_USERNAME}"
    )

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("Aapke paas admin rights nahi hain.")
        return
    await update.message.reply_text(f"Welcome Admin (@{ADMIN_USERNAME})! System fully functional hai.")

def main():
    # Application setup
    application = Application.builder().token(BOT_TOKEN).build()

    # Handlers Add Karein
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("admin", admin_panel))

    # Bot Polling Start Karein
    application.run_polling()

if __name__ == "__main__":
    # Flask application in background for Render web service check
    import threading
    port = int(os.environ.get("PORT", 5000))
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=port)).start()
    
    # Run Telegram Bot
    main()

