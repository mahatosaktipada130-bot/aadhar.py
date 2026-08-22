import os
import re
import random
import logging
import threading
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, 
    ConversationHandler, ContextTypes, filters
)
from curl_cffi import requests as cffi_requests

# Configuration
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8640207091:AAGzbEZWsfBEX3okHKb0ZUjfU4Uvj5G_Ig4")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "8640207091"))

# States for Conversation
PHONE, OTP = range(2)

# Global Session Store per user
user_sessions = {}

class ShopsyBotEngine:
    def __init__(self, phone):
        self.phone = phone
        self.session = cffi_requests.Session(impersonate="chrome120")
        self.otp_request_id = None
        self.fk_token = None
        self.user_id = None
        
    def send_otp(self):
        clean_phone = re.sub(r'\D', '', self.phone)[-10:]
        payload = {
            "actionRequestContext": {
                "type": "LOGIN_IDENTITY_VERIFY_SHOPSY2", 
                "loginId": clean_phone, 
                "loginIdPrefix": "+91", 
                "phoneNumberFormat": "E164", 
                "addAppHash": True, 
                "loginType": "MOBILE", 
                "verificationType": "OTP", 
                "sourceContext": "DEFAULT"
            }
        }
        try:
            resp = self.session.post(
                "https://1.rome.api.flipkart.net/1/action/view", 
                json=payload, 
                headers={"Content-Type": "application/json"},
                verify=False
            )
            if resp.status_code == 200:
                data = resp.json()
                self.otp_request_id = data.get("RESPONSE", {}).get("actionResponseContext", {}).get("requestId")
                return True
        except Exception:
            pass
        return False

    def verify_otp(self, otp_code):
        clean_phone = re.sub(r'\D', '', self.phone)[-10:]
        payload = {
            "actionRequestContext": {
                "type": "LOGIN_SHOPSY2", 
                "loginId": clean_phone, 
                "loginIdPrefix": "+91", 
                "otp": otp_code, 
                "otpRequestId": self.otp_request_id, 
                "loginType": "MOBILE", 
                "verificationType": "OTP"
            }
        }
        try:
            resp = self.session.post(
                "https://1.rome.api.flipkart.net/1/action/view", 
                json=payload, 
                headers={"Content-Type": "application/json"},
                verify=False
            )
            if resp.status_code == 200 and resp.json().get("RESPONSE", {}).get("actionResponseContext", {}).get("authenticationSuccess"):
                return True
        except Exception:
            pass
        return False

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to SuperCoin Collector Bot!\n\n📱 Apnamobile number bhejein (Example: 9876543210):")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text.strip()
    user_id = update.effective_user.id
    
    bot_engine = ShopsyBotEngine(phone)
    await update.message.reply_text("🔄 Sending OTP...")
    
    if bot_engine.send_otp():
        user_sessions[user_id] = bot_engine
        await update.message.reply_text("✅ OTP bhej diya gaya hai! Kripya OTP enter karein:")
        return OTP
    else:
        await update.message.reply_text("❌ OTP bhejne me dikkat aayi. Kripya dobara /start karein.")
        return ConversationHandler.END

async def get_otp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    otp = update.message.text.strip()
    user_id = update.effective_user.id
    bot_engine = user_sessions.get(user_id)

    if not bot_engine:
        await update.message.reply_text("Session expire ho gaya. Phir se /start karein.")
        return ConversationHandler.END

    await update.message.reply_text("🔄 Verifying OTP...")
    if bot_engine.verify_otp(otp):
        await update.message.reply_text("🎉 Login Successful! Coins Claiming process start ho raha hai...")
        # Yahan par task collection thread run kar sakte hain
    else:
        await update.message.reply_text("❌ Galat OTP. Kripya /start se dobara try karein.")

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Process cancelled.")
    return ConversationHandler.END

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            OTP: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_otp)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == '__main__':
    main()
