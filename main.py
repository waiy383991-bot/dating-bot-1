import os
import logging
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- CONFIGURATION ---
# သင့် Bot ရဲ့ Token နဲ့ Admin ID
TOKEN = "7864468696:AAH1yM6o52kL4IofZqNqE7_h_L_nU4Y-190"
ADMIN_ID = 6980157986

# --- WEB SERVER FOR UPTIME (Flask) ---
# ဒါမှ Render က 24 နာရီ run ပေးမှာပါ
app = Flask('')

@app.route('/')
def home():
    return "Dating Bot is alive! 💕"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- BOT LOGIC ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_msg = f"မင်္ဂလာပါ {user.first_name}!\nDating Bot မှ ကြိုဆိုပါတယ်။ Profile တင်ရန် အချက်အလက်များ ပို့ပေးပါခင်ဗျာ။"
    await update.message.reply_text(welcome_msg)
    
    # Admin ဆီကို User အသစ်ရောက်ကြောင်း Noti ပို့ခြင်း
    admin_noti = f"🔔 **User အသစ်တစ်ယောက် ရောက်လာပါပြီ!**\nName: {user.first_name}\nID: {user.id}\nUsername: @{user.username if user.username else 'None'}"
    await context.bot.send_message(chat_id=ADMIN_ID, text=admin_noti)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("အကူအညီအတွက် Admin ကို ဆက်သွယ်ပါ သို့မဟုတ် /start ကို ပြန်နှိပ်ပါ။")

def main():
    # Web Server ကို အရင်နှိုးမယ်
    keep_alive()

    # Bot Application ကို စတင်မယ်
    application = Application.builder().token(TOKEN).build()

    # Commands များ
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # Message များ (စာရိုက်ရင် တုံ့ပြန်ဖို့)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, start))

    print("Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    mပေးမှာပါ
