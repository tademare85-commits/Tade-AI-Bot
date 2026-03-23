import asyncio
import nest_asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

nest_asyncio.apply()

TOKEN = "8516441685:AAEiHeNLtNjqVEfWyt93oruTqQIBed7h9Ik"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ሰላም! እኔ የ Tade AI ረዳት ነኝ። ገቢና ወጪዎን በኮማ ለይተው ይላኩ (ምሳሌ፦ 5000,2000)")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        income, expense = map(float, update.message.text.split(','))
        profit = income - expense
        advice = "ጥሩ ትርፍ ነው!" if profit > 0 else "ኪሳራ አለብህ!"
        await update.message.reply_text(f"📊 ሪፖርት\nትርፍ፡ {profit} ብር\nምክር፡ {advice}")
    except:
        await update.message.reply_text("እባክህ ቁጥሮቹን በዚህ መልክ አስገባ፦ 5000,2000")

async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    await app.initialize()
    await app.updater.start_polling()
    await app.start()
    while True: await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main())
