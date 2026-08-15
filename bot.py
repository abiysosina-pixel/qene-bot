import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# ሎግ ማስተካከያ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = "8866935970:AAGr1LED7cmOpgvaSZbTdlcbQ-ouyxvg99s"

# 👉 የኦነሩን (የአድሚኑን) Telegram Chat ID እዚህ አስገባ
ADMIN_CHAT_ID = 6720784698

# 1. /start ሲባል የሚመጣ መነሻ
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    try:
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"🔔 **አዲስ ተጠቃሚ ቦቱን ጀምሯል!**\n👤 ስም፦ {user.full_name}\nUsername: @{user.username if user.username else 'የለውም'}",
            parse_mode='Markdown'
        )
    except Exception:
        pass

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

# 2. የአዝራሮች (Button) መጫን እንቅስቃሴን ማስተናገጃ
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # ሀ. "ከኢትዮጵያ ውጭ" ሲመረጥ
    if data == 'loc_abroad':
        text_abroad = (
            "ደውሉ ወይም ኢንቦክስ አድርጉ\n\n"
            "📞 Phone Number: 0915642585\n"
            "💬 Telegram Username: @pawli37"
        )
        keyboard = [[InlineKeyboardButton("⬅️ ተመለስ", callback_data='back_to_start')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=text_abroad, reply_markup=reply_markup)

    # ለ. "ኢትዮጵያ ውስጥ" ሲመረጥ
    elif data == 'loc_ethiopia':
        keyboard = [
            [InlineKeyboardButton("በመጀመሪያ የሚማሩትን ይምረጡ", callback_data='start_learning')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="አሁን እንዴት ልጀምር", reply_markup=reply_markup)

    # ሐ. "በመጀመሪያ የሚማሩትን ይምረጡ" ሲነካ
    elif data == 'start_learning':
        keyboard = [
            [InlineKeyboardButton("ቅኔ", callback_data='qene')],
            [InlineKeyboardButton("ንባብ", callback_data='nibab')],
            [InlineKeyboardButton("ባሕረ ሃሳብ", callback_data='bahre_hasab')],
            [InlineKeyboardButton("ግእዝ ቋንቋ", callback_data='geez')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="በመጀመሪያ የሚማሩትን ይምረጡ", reply_markup=reply_markup)

    # መ. "ቅኔ" ሲመረጥ
    elif data == 'qene':
        qene_text = (
            "ቅኔ ውስጥ የሚማሩት፦\n\n"
            "👉 ቅኔ ዘረፋ፣ ቅኔነገራ፣ ቅኔ ቅጸላ\n"
            "👉 የቅኔ ምራታ፣ የቅኔ ፍች\n"
            "👉 የቅኔ ርቃቄ፣ የቅኔ ሠምና ወርቅ\n"
            "👉 የቅኔ ሙያ፣ ግስ ገሰሳ\n"
            "👉 ግስ ርባታ፣ ነባር አንቀጽ ርባታ\n"
            "👉 ታሪክ ትረካ፣ አገባብ ቅጸላ፣ ግስ ቅጸላ\n"
            "👉 ነባር ቅጸላ፣ ቅኔ ጎዳና\n"
            "👉 ርባታ ቅጸላ፣ ዜማ ልክ፣ ገቢር ተገብሮ"
        )
        keyboard = [
            [InlineKeyboardButton("አሁን እንዴት ልጀምር", callback_data='qene_registration')],
            [InlineKeyboardButton("⬅️ ተመለስ", callback_data='start_learning')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=qene_text, reply_markup=reply_markup)

    # ሠ. "ንባብ" ሲመረጥ
    elif data == 'nibab':
        nibab_text = (
            "ንባብ ውስጥ የሚማሩት፦\n\n"
            "👉 የዘወትር ጸሎት\n"
            "👉 ውዳሴ ማርያም\n"
            "👉 አንቀጸ ብርሃን\n"
            "👉 ይዌድስዋ መላእክት\n"
            "👉 መልክዐ ማርያም\n"
            "👉 መልክዐ ኢየሱስ\n"
            "👉 መልክዐ ሚካኤል\n"
            "👉 የወንጌል ንባብ\n"
            "👉 መዝሙረ ዳዊት\n"
            "👉 የግብረ ሐዋርያት ንባብ"
        )
        keyboard = [
            [InlineKeyboardButton("አሁን እንዴት ልጀምር", callback_data='nibab_registration')],
            [InlineKeyboardButton("⬅️ ተመለስ", callback_data='start_learning')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=nibab_text, reply_markup=reply_markup)

    # ረ. "ባሕረ ሃሳብ" ሲመረጥ
    elif data == 'bahre_hasab':
        bahre_text = (
            "ባሕረ ሃሳብ ውስጥ የሚማሩት፦\n\n"
            "👉 ወንጌላውያን\n"
            "👉 መጥቅዕና አበቅቴ\n"
            "👉 መደብና ወንበር\n"
            "👉 መባጃ ሐመርና ተውሳክ\n"
            "👉 የአጽዋማትና በዓላት አወጣጥ\n"
            "👉 ኢየአርግና ኢይወርድ\n"
            "👉 ሠርቃት/አሥርቆት\n"
            "👉 የብርሃናትና ነፋሳት አፈጣጠር\n"
            "👉 ዓመተ ሰማዕታት\n"
            "👉 ኬክሮስና ኬንትሮስ\n"
            "👉 እና ሌሎችም ...."
        )
        keyboard = [
            [InlineKeyboardButton("አሁን እንዴት ልጀምር", callback_data='bahre_registration')],
            [InlineKeyboardButton("⬅️ ተመለስ", callback_data='start_learning')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=bahre_text, reply_markup=reply_markup)

    # ሰ. "ግእዝ ቋንቋ" ሲመረጥ
    elif data == 'geez':
        geez_text = (
            "ግእዝ ቋንቋ ውስጥ የሚማሩት፦\n\n"
            "👉 ከፊደላት ትርጕም ጀምሮ\n"
            "👉 ነጠላ ግስና ርባታ\n"
            "👉 ነባር ስም ቃላት\n"
            "👉 አንቀጽና የአንቀጽ አይነቶች\n"
            "👉 ገቢርና ተገብሮ\n"
            "👉 ቅጽልና የቅጽል አይነቶች\n"
            "👉 የዋህና መሠሪ ርባታ\n"
            "👉 የንባባት ትርጉምና ርባታ\n"
            "👉 የግእዝ ዐውዳዊ ፍች\n"
            "👉 ከግእዝ ወደ ዐማርኛ መተርጐም\n"
            "👉 ከዐማርኛ ወደ ግእዝ መተርጐም"
        )
        keyboard = [
            [InlineKeyboardButton("አሁን እንዴት ልጀምር", callback_data='geez_registration')],
            [InlineKeyboardButton("⬅️ ተመለስ", callback_data='start_learning')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=geez_text, reply_markup=reply_markup)

    # ሸ. የቅኔ የመመዝገቢያ እና የክፍያ ፎርም
    elif data == 'qene_registration':
        qene_form_text = (
            "📜 **ቅኔ — የመመዝገቢያ እና የክፍያ ፎርም**\n\n"
            "💵 **የክፍያ ሁኔታና መጠን፦**\n"
            "• በቅድመ ክፍያ ነው\n"
            "• የሀገር ውስጥ ተማሪ የ6 ወራት፦ **3,900 ብር**\n"
            "• የዓመት፦ **7,500 ብር**\n\n"
            "📚 **ትምህርቱ በ4 ዓይነት መንገድ ይሰጣል፦**\n"
            "1. ቀጥታ በቴሌግራም\n"
            "2. ቅጅ በመላክ\n"
            "3. በጽሑፍ በመላክ\n"
            "4. በስልክ\n\n"
            "🏦 **የመክፈያ ቦታ፦**\n"
            "• **የኢትዮጵያ ንግድ ባንክ**\n"
            "  አካውንት ቁጥር፦ `1000185120213` (ጳውሎስ ብርሃኔ ዘሪሁን)\n"
            "• **አቢሲንያ ባንክ**\n"
            "  አካውንት ቁጥር፦ `145908407` (ጳውሎስ ብርሃኔ ዘሪሁን)\n\n"
            "➡️➡️➡️➡️➡️➡️\n"
            "ደረሰኙን ፎቶ አንስተው ወይም ስክሪን ሹት ይላኩልኝ።\n\n"
            "✍️ **እባክዎን የሚከተሉትን መረጃዎች ሞልተው ይላኩልን፦**\n"
            "1. ሙሉ ስም (ከነአያት)፦\n"
            "2. ስልክ ቁጥር፦\n"
            "3. Telegram Username፦ @\n"
            "4. አድራሻ (ከተማ/ክፍለ ከተማ)፦\n"
            "5. የክፍያ ማረጋገጫ ቁጥር (Transaction ID / Ref No)፦\n\n"
            "📞 **ለበለጠ መረጃ ይደውሉ፦** 0915642585"
        )
        keyboard = [[InlineKeyboardButton("⬅️ ወደ ዋናው ሜኑ", callback_data='back_to_start')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=qene_form_text, parse_mode='Markdown', reply_markup=reply_markup)

    # ቀ. የንባብ የመመዝገቢያ እና የክፍያ ፎርም
    elif data == 'nibab_registration':
        nibab_form_text = (
            "📖 **ንባብ — የመመዝገቢያ እና የክፍያ ፎርም**\n\n"
            "💵 **የክፍያ ሁኔታና መጠን፦**\n"
            "• በቅድመ ክፍያ ነው\n"
            "• የሀገር ውስጥ ተማሪ የ6 ወራት፦ **3,900 ብር**\n"
            "• የዓመት፦ **7,500 ብር**\n\n"
            "📚 **ትምህርቱ በ4 ዓይነት መንገድ ይሰጣል፦**\n"
            "1. ቀጥታ በቴሌግራም\n"
            "2. ቅጅ በመላክ\n"
            "3. በጽሑፍ በመላክ\n"
            "4. በስልክ\n\n"
            "🏦 **የመክፈያ ቦታ፦**\n"
            "• **የኢትዮጵያ ንግድ ባንክ**\n"
            "  አካውንት ቁጥር፦ `1000185120213` (ጳውሎስ ብርሃኔ ዘሪሁን)\n"
            "• **አቢሲንያ ባንክ**\n"
            "  አካውንት ቁጥር፦ `145908407` (ጳውሎስ ብርሃኔ ዘሪሁን)\n\n"
            "➡️➡️➡️➡️➡️➡️\n"
            "ደረሰኙን ፎቶ አንስተው ወይም ስክሪን ሹት ይላኩልኝ።\n\n"
            "✍️ **እባክዎን የሚከተሉትን መረጃዎች ሞልተው ይላኩልን፦**\n"
            "1. ሙሉ ስም (ከነአያት)፦\n"
            "2. ስልክ ቁጥር፦\n"
            "3. Telegram Username፦ @\n"
            "4. አድራሻ (ከተማ/ክፍለ ከተማ)፦\n"
            "5. የክፍያ ማረጋገጫ ቁጥር (Transaction ID / Ref No)፦\n\n"
            "📞 **ለበለጠ መረጃ ይደውሉ፦** 0915642585"
        )
        keyboard = [[InlineKeyboardButton("⬅️ ወደ ዋናው ሜኑ", callback_data='back_to_start')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=nibab_form_text, parse_mode='Markdown', reply_markup=reply_markup)

    # በ. የባሕረ ሃሳብ የመመዝገቢያ እና የክፍያ ፎርም
    elif data == 'bahre_registration':
        bahre_form_text = (
            "🗓 **ባሕረ ሃሳብ — የመመዝገቢያ እና የክፍያ ፎርም**\n\n"
            "💵 **ዋጋ፦** ወራዊ ክፍያ 600 + መመዝገቢያ 300 = **900 ብር**\n\n"
            "📚 **ትምህርቱ በ4 ዓይነት መንገድ ይሰጣል፦**\n"
            "1. ቀጥታ በቴሌግራም\n"
            "2. ቅጅ በመላክ\n"
            "3. በጽሑፍ በመላክ\n"
            "4. በስልክ\n\n"
            "🏦 **የመክፈያ ቦታ፦**\n"
            "• **የኢትዮጵያ ንግድ ባንክ**\n"
            "  አካውንት ቁጥር፦ `1000185120213` (ጳውሎስ ብርሃኔ ዘሪሁን)\n"
            "• **አቢሲንያ ባንክ**\n"
            "  አካውንት ቁጥር፦ `145908407` (ጳውሎስ ብርሃኔ ዘሪሁን)\n\n"
            "➡️➡️➡️➡️➡️➡️\n"
            "ደረሰኙን ፎቶ አንስተው ወይም ስክሪን ሹት ይላኩልኝ።\n\n"
            "✍️ **እባክዎን የሚከተሉትን መረጃዎች ሞልተው ይላኩልን፦**\n"
            "1. ሙሉ ስም (ከነአያት)፦\n"
            "2. ስልክ ቁጥር፦\n"
            "3. Telegram Username፦ @\n"
            "4. አድራሻ (ከተማ/ክፍለ ከተማ)፦\n"
            "5. የክፍያ ማረጋገጫ ቁጥር (Transaction ID / Ref No)፦\n\n"
            "📞 **ለበለጠ መረጃ ይደውሉ፦** 0915642585"
        )
        keyboard = [[InlineKeyboardButton("⬅️ ወደ ዋናው ሜኑ", callback_data='back_to_start')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=bahre_form_text, parse_mode='Markdown', reply_markup=reply_markup)

    # ተ. የግዕዝ ቋንቋ የመመዝገቢያ እና የክፍያ ፎርም
    elif data == 'geez_registration':
        geez_form_text = (
            "🔤 **ግዕዝ ቋንቋ — የመመዝገቢያ እና የክፍያ ፎርም**\n\n"
            "💵 **ዋጋ፦** ወራዊ ክፍያ 600 + መመዝገቢያ 300 = **900 ብር**\n\n"
            "📚 **ትምህርቱ በ4 ዓይነት መንገድ ይሰጣል፦**\n"
            "1. ቀጥታ በቴሌግራም\n"
            "2. ቅጅ በመላክ\n"
            "3. በጽሑፍ በመላክ\n"
            "4. በስልክ\n\n"
            "🏦 **የመክፈያ ቦታ፦**\n"
            "• **የኢትዮጵያ ንግድ ባንክ**\n"
            "  አካውንት ቁጥር፦ `1000185120213` (ጳውሎስ ብርሃኔ ዘሪሁን)\n"
            "• **አቢሲንያ ባንክ**\n"
            "  አካውንት ቁጥር፦ `145908407` (ጳውሎስ ብርሃኔ ዘሪሁን)\n\n"
            "➡️➡️➡️➡️➡️➡️\n"
            "ደረሰኙን ፎቶ አንስተው ወይም ስክሪን ሹት ይላኩልኝ።\n\n"
            "✍️ **እባክዎን የሚከተሉትን መረጃዎች ሞልተው ይላኩልን፦**\n"
            "1. ሙሉ ስም (ከነአያት)፦\n"
            "2. ስልክ ቁጥር፦\n"
            "3. Telegram Username፦ @\n"
            "4. አድራሻ (ከተማ/ክፍለ ከተማ)፦\n"
            "5. የክፍያ ማረጋገጫ ቁጥር (Transaction ID / Ref No)፦\n\n"
            "📞 **ለበለጠ መረጃ ይደውሉ፦** 0915642585"
        )
        keyboard = [[InlineKeyboardButton("⬅️ ወደ ዋናው ሜኑ", callback_data='back_to_start')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=geez_form_text, parse_mode='Markdown', reply_markup=reply_markup)

    # ቸ. ወደ መጀመሪያው የመመለሻ
    elif data == 'back_to_start':
        await start(update, context)

# 3. ተጠቃሚው የሚልከውን መረጃ (ጽሁፍ/ስክሪንሾት) ቀጥታ ወደ ኦነሩ Forward ማድረግ
async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await context.bot.forward_message(
            chat_id=ADMIN_CHAT_ID,
            from_chat_id=update.message.chat_id,
            message_id=update.message.message_id
        )
        await update.message.reply_text("የክፍያ ደረሰኝዎ ለመዝጋቢው ደርሷል። በፍጥነት መልስ ይላካል። እናመሰግናለን")
    except Exception:
        await update.message.reply_text("መረጃውን መላክ አልተቻለም። እባክዎ እንደገና ይሞክሩ።")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, forward_to_admin))

    print("ቦቱ በስኬት ስራ ጀምሯል...")
    app.run_polling()

if __name__ == '__main__':
    main()
