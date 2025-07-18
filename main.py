import os
import openai
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler

# مفاتيح من بيئة التشغيل
openai.api_key = os.getenv("OPENAI_API_KEY")
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")

# رسالة الترحيب
def start(update: Update, context: CallbackContext):
    welcome_message = (
        "👋 مرحباً بك في بوت الذكاء الاصطناعي!\n\n"
        "🤖 هذا البوت يستخدم نموذج ChatGPT من شركة OpenAI للرد على أسئلتك بشكل ذكي.\n"
        "📌 تم تطوير هذا البوت بواسطة: *عبدالرحمن جمال عبدالرب العطاس*.\n\n"
        "💬 ابدأ بإرسال أي رسالة وسأقوم بالرد عليك ✨"
    )
    update.message.reply_text(welcome_message, parse_mode="Markdown")

# الرد على الرسائل النصية
def chat(update: Update, context: CallbackContext):
    user_message = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response['choices'][0]['message']['content']
        update.message.reply_text(reply)
    except Exception as e:
        update.message.reply_text("حدث خطأ: " + str(e))

# تفعيل البوت
def main():
    updater = Updater(telegram_token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, chat))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
