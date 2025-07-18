import os
import openai
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext
)

# إعداد المفاتيح من البيئة
openai.api_key = os.getenv("OPENAI_API_KEY")
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")

# أمر /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "👋 مرحباً بك في بوت الذكاء الاصطناعي!\n\n"
        "🤖 هذا البوت يستخدم نموذج ChatGPT من شركة OpenAI للرد على أسئلتك.\n"
        "📌 تم تطويره بواسطة: عبدالرحمن جمال عبدالرب العطاس.\n\n"
        "💬 أرسل لي أي رسالة الآن وسأجيبك!"
    )

# الرد التلقائي
def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        bot_reply = response["choices"][0]["message"]["content"]
        update.message.reply_text(bot_reply)
    except Exception as e:
        update.message.reply_text(f"❌ حدث خطأ: {str(e)}")

def main():
    updater = Updater(telegram_token, use_context=True)
    dp = updater.dispatcher

    # مسجّل الأوامر
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
