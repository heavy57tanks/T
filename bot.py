import telebot
from telebot import types

# التوكن
TELEGRAM_TOKEN = "7933355250:AAH7moLKbjXd39w9A4obFpXECi1oamyruaE"
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# عند إرسال /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📊 تحليل السوق", "🧪 فحص الأسهم")
    markup.row("📈 عرض النتائج", "ℹ️ تعليمات")
    bot.send_message(message.chat.id, "✅ مرحباً يا أبو عبد الرحمن! اختر من القائمة:", reply_markup=markup)

# التعامل مع الأوامر النصية
@bot.message_handler(func=lambda m: True)
def handle_message(message):
    text = message.text.strip()

    if text == "📊 تحليل السوق":
        bot.reply_to(message, "🔍 يتم الآن تحليل السوق...")

    elif text == "🧪 فحص الأسهم":
        bot.reply_to(message, "✅ جاري فحص الأسهم...")

    elif text == "📈 عرض النتائج":
        bot.reply_to(message, "📋 هذه هي نتائج الفحص الأخيرة...")

    elif text == "ℹ️ تعليمات":
        bot.reply_to(message, "📘 تعليمات الاستخدام:\n- اختر أمر من القائمة\n- انتظر الرد\n- تواصل معي في حال وجود استفسار")

    else:
        bot.reply_to(message, "❌ لم أفهم الأمر. اختر من الأزرار الظاهرة.")

# تشغيل البوت
print("✅ البوت يعمل الآن...")
bot.infinity_polling()