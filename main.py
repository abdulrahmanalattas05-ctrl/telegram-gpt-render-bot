import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# إعداد مفتاح OpenAI من متغير البيئة
openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "👋 مرحباً بك في بوت الذكاء الاصطناعي!\n\n"
        "🤖 هذا البوت يستخدم نموذج ChatGPT من شركة OpenAI للرد على أسئلتك.\n"
        "📌 تم تطوير هذا البوت بواسطة: *عبدالرحمن جمال عبدالرب العطاس*\n\n"
        "💬 أرسل أي رسالة وسأرد عليك باستخدام الذكاء الاصطناعي ✨"
    )
    await update.message.reply_text(message, parse_mode="Markdown")

# الرد على الرسائل النصية
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_msg}
            ]
        )
        reply = response.choices[0].message.content
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ: {e}")

# تشغيل التطبيق
async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), chat))

    print("🤖 البوت قيد التشغيل...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
