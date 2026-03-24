
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8516441685:AAEiHeNLtNjqVEfWyt93oruTqQIBed7h9Ik"

# የሰዎችን ሂሳብ ለጊዜው ለመያዝ
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id] = {'income': 0, 'expense': 0, 'history': []}
    
    await update.message.reply_text(
        "ሰላም! የታደሰ (Tade) የሂሳብ ረዳት ነኝ።\n\n"
        "አጠቃቀም፦\n"
        "1. ገቢ ሲኖር፦ '5000 ደመወዝ' ብለው ይጻፉ።\n"
        "2. ወጪ ሲኖር፦ '200 ለምሳ' ብለው ይጻፉ።\n"
        "3. ድምር ለማየት፦ /report ብለው ይላኩ።\n"
        "4. ለማጥፋት፦ /clear ይበሉ。"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    
    if user_id not in user_data:
        user_data[user_id] = {'income': 0, 'expense': 0, 'history': []}

    try:
        parts = text.split()
        amount = float(parts[0])
        reason = " ".join(parts[1:]) if len(parts) > 1 else "ያልተጠቀሰ"

        # ወጪ መሆኑን በ "ለ" ወይም "ወጪ" ቃላት ይለያል
        if "ለ" in text or "ወጪ" in text or "ገዛሁ" in text:
            user_data[user_id]['expense'] += amount
            status = "📉 ወጪ ተመዝግቧል"
        else:
            user_data[user_id]['income'] += amount
            status = "💰 ገቢ ተመዝግቧል"
        
        user_data[user_id]['history'].append(f"{status}: {amount} ({reason})")
        await update.message.reply_text(f"{status}!\nመጠን፦ {amount} ብር\nምክንያት፦ {reason}\n\nአጠቃላይ ድምር ለማየት /report ይበሉ")
        
    except ValueError:
        await update.message.reply_text("እባክህ መጀመሪያ ቁጥሩን ጻፍ። ምሳሌ፦ '200 ለታክሲ'")

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_data:
        await update.message.reply_text("ገና ምንም ሂሳብ አላስገቡም።")
        return

    data = user_data[user_id]
    balance = data['income'] - data['expense']
    
    report_msg = (
        f"📊 የሂሳብ ሪፖርት\n"
        f"━━━━━━━━━━━━━\n"
        f"💰 ጠቅላላ ገቢ፦ {data['income']} ብር\n"
        f"📉 ጠቅላላ ወጪ፦ {data['expense']} ብር\n"
        f"━━━━━━━━━━━━━\n"
        f"💵 የቀረህ ሂሳብ፦ {balance} ብር\n"
    )
    
    if balance < 100:
        report_msg += "\n⚠️ ወጪህን ቀንስ፣ ሂሳብህ እያለቀ ነው!"
    else:
        report_msg += "\n✅ ጥሩ አያያዝ ነው፣ ቀጥልበት!"

    await update.message.reply_text(report_msg)

async def clear_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id] = {'income': 0, 'expense': 0, 'history': []}
    await update.message.reply_text("ሁሉም መረጃ ተሰርዟል! አዲስ መመዝገብ ይችላሉ።")

async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("report", report))
    app.add_handler(CommandHandler("clear", clear_data))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("ቦቱ እየሰራ ነው...")
    await app.initialize()
    await app.updater.start_polling()
    await app.start()
    while True: await asyncio.sleep(1)

if __name__ == '__main__':
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(main())
