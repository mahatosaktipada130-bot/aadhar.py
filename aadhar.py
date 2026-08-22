import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Logging Configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Bot Variables
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8640207091:AAFaC2lGxi8YmJkoSPx27IDiCb8yTGG2A5w")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "8640207091"))
ADMIN_USERNAME = "ecbots3004"
BOT_USERNAME = "ecaadharbot"

# Commands
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
    print("Bot startup sequence running...")
    application = Application.builder().token(BOT_TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("admin", admin_panel))

    # Run Polling
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
