import logging
import json
import os
from datetime import time
import pytz
from threading import Thread
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# 1. Render Port እንዳይዘጋ የሚያደርግ Web Server
app_flask = Flask('')

@app_flask.route('/')
def home():
    return "Bot is running live!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app_flask.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

# 2. ሎግ ማስተካከያ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = "8866935970:AAGr1LED7cmOpgvaSZbTdlcbQ-ouyxvg99s"
ADMIN_CHAT_ID = 1001745313
# ፋይል ሳያስፈልግ ተጠቃሚዎችን በሜሞሪ (RAM) ብቻ መያዣ
users = set()

def save_user(user_id):
    try:
        users = load_users()
        if user_id not in users:
            users.add(user_id)
            with open(USERS_FILE, "w") as f:
                json.dump(list(users), f)
    except Exception as e:
        logging.error(f"User ID ማስቀመጥ አልተቻለም፦ {e}")

# 3. /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user
        if user:
            save_user(user.id)
    except Exception:
        pass

    keyboard = [
        [InlineKeyboardButton("ኢትዮጵያ ውስጥ", callback_data='loc_ethiopia')],
        [InlineKeyboardButton("ከኢትዮጵያ ውጭ", callback_data='loc_abroad')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg_text = "የሚኖሩበትን ቦታ ይምረጡ፦"
    
    try:
        if update.message:
            await update.message.reply_text(msg_text, reply_markup=reply_markup)
        elif update.callback_query:
            await update.callback_query.message.delete()
            await context.bot.send_message(
                chat_id=update.callback_query.message.chat_id, 
                text=msg_text, 
                reply_markup=reply_markup
            )
    except Exception as e:
        logging.error(f"Start መልእክት መላክ አልተቻለም፦ {e}")
    keyboard = [
        [InlineKeyboardButton("ኢትዮጵያ ውስጥ", callback_data='loc_ethiopia')],
        [InlineKeyboardButton("ከኢትዮጵያ ውጭ", callback_data='loc_abroad')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg_text = "የሚኖሩበትን ቦታ ይምረጡ፦"
    
    if update.message:
        await update.message.reply_text(msg_text, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.delete()
        await context.bot.send_message(chat_id=update.callback_query.message.chat_id, text=msg_text, reply_markup=reply_markup)

# 4. Buttons handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == 'loc_abroad':
        text_abroad = (
            "ደውሉ ወይም ኢንቦክስ አድርጉ\n\n"
            "📞 Phone Number: 0915642585\n"
            "💬 Telegram Username: @awuli37"
        )
        keyboard = [[InlineKeyboardButton("⬅️ ተመለስ", callback_data='back_to_start')]]
        await query.edit_message_text(text=text_abroad, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == 'loc_ethiopia':
        keyboard = [[InlineKeyboardButton("በመጀመሪያ የሚማሩትን ይምረጡ", callback_data='start_learning')]]
        await query.edit_message_text(text="አሁን እንዴት ልጀምር", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == 'start_learning':
        keyboard = [
            [InlineKeyboardButton("ቅኔ", callback_data='qene')],
            [InlineKeyboardButton("ንባብ", callback_data='nibab')],
            [InlineKeyboardButton("ባሕረ ሃሳብ", callback_data='bahre_hasab')],
            [InlineKeyboardButton("ግእዝ ቋንቋ", callback_data='geez')]
        ]
        await query.edit_message_text(text="በመጀመሪያ የሚማሩትን ይምረጡ", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data in ['qene', 'nibab', 'bahre_hasab', 'geez']:
        details = {
            'qene': ("ቅኔ ውስጥ የሚማሩት፦\n\n👉 ቅኔ ዘረፋ፣ ቅኔነገራ...\n👉 የቅኔ ምራታ፣ ፍች፣ ርቃቄ...", 'qene_registration'),
            'nibab': ("ንባብ ውስጥ የሚማሩት፦\n\n👉 የዘወትር ጸሎት\n👉 ውዳሴ ማርያም...", 'nibab_registration'),
            'bahre_hasab': ("ባሕረ ሃሳብ ውስጥ የሚማሩት፦\n\n👉 ወንጌላውያን፣ መጥቅዕና አበቅቴ...", 'bahre_registration'),
            'geez': ("ግእዝ ቋንቋ ውስጥ የሚማሩት፦\n\n👉 ነጠላ ግስና ርባታ፣ ነባር ስም...", 'geez_registration')
        }
        text, reg_target = details[data]
        keyboard = [
            [InlineKeyboardButton("አሁን እንዴት ልጀምር", callback_data=reg_target)],
            [InlineKeyboardButton("⬅️ ተመለስ", callback_data='start_learning')]
        ]
        await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif '_registration' in data:
        form_text = (
            "📜 **የመመዝገቢያ እና የክፍያ ፎርም**\n\n"
            "🏦 **የመክፈያ ቦታ፦**\n"
            "• **ንግድ ባንክ፦** `1000185120213` (ጳውሎስ ብርሃኔ ዘሪሁን)\n"
            "• **አቢሲንያ ባንክ፦** `145908407` (ጳውሎስ ብርሃኔ ዘሪሁን)\n\n"
            "➡️ ደረሰኙን/ስክሪንሾቱን እና መረጃዎን ይላኩልን።\n"
            "1. ሙሉ ስም፦\n2. ስልክ ቁጥር፦\n3. Telegram Username፦ @\n4. Transaction ID፦"
        )
        keyboard = [[InlineKeyboardButton("⬅️ ወደ ዋናው ሜኑ", callback_data='back_to_start')]]
        await query.edit_message_text(text=form_text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == 'back_to_start':
        await start(update, context)

# 5. በየቀኑ አውቶማቲክ የሚላክ የመጽሐፍ ማስታወቂያ
async def send_daily_ad(context: ContextTypes.DEFAULT_TYPE):
    users = load_users()
    ad_text = (
        "📚 **የመጽሐፍ ማስታወቂያ**\n\n"
        "የመምህሩ አዲስ መጽሐፍ ለሽያጭ ቀርቧል! ለመግዛትና ለበለጠ መረጃ በስልክ ቁጥር 0915642585 ይደውሉ ወይም @awuli37 ያግኙን።"
    )
    for u_id in users:
        try:
            await context.bot.send_message(chat_id=u_id, text=ad_text, parse_mode='Markdown')
        except Exception:
            pass

# 6. የመምህሩ ብሮድካስት command (/broadcast)
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_CHAT_ID:
        return
    
    msg = update.message.text.replace("/broadcast", "").strip()
    if not msg:
        await update.message.reply_text("ከመጨረሻው ላይ /broadcast ካሉ በኋላ የማስታወቂያውን ጽሁፍ ጽፈው ይላኩ።")
        return

    users = load_users()
    count = 0
    for u_id in users:
        try:
            await context.bot.send_message(chat_id=u_id, text=msg)
            count += 1
        except Exception:
            pass
    await update.message.reply_text(f"ማስታወቂያው ለ {count} ተጠቃሚዎች ተልኳል!")

# 7. መረጃዎችን እና የክፍያ ስክሪንሾት ወደ አድሚን ማስተላለፊያ
async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user.id)
    try:
        await context.bot.forward_message(
            chat_id=ADMIN_CHAT_ID,
            from_chat_id=update.message.chat_id,
            message_id=update.message.message_id
        )
        await update.message.reply_text("የላኩት መረጃ/የክፍያ ደረሰኝ ለአድሚኑ ደርሷል! በቅርቡ ያናግሩዎታል።")
    except Exception:
        await update.message.reply_text("መረጃውን መላክ አልተቻለም። እባክዎ እንደገና ይሞክሩ።")

def main():
    keep_alive()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, forward_to_admin))

    job_queue = app.job_queue
    eat_tz = pytz.timezone('Africa/Addis_Ababa')
    job_queue.run_daily(send_daily_ad, time=time(hour=9, minute=0, second=0, tzinfo=eat_tz))

    print("ቦቱ በስኬት ስራ ጀምሯል...")
    app.run_polling()

if __name__ == '__main__':
    main()
