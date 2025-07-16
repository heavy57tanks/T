import telebot
from telebot import types

# ✅ توكن البوت
TELEGRAM_TOKEN = "7933355250:AAH7moLKbjXd39w9A4obFpXECi1oamyruaE"

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# ✅ رسالة البداية
@bot.message_handler(commands=["start"])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("عرض القائمة 📋")
    markup.add(button)
    bot.reply_to(message, "✅ البوت بدأ يا أبو عبد الرحمن!", reply_markup=markup)

# ✅ عرض القائمة (سواء بالزر أو كتابة)
@bot.message_handler(func=lambda message: "عرض" in message.text and "القائمة" in message.text)
def show_list(message):
    bot.reply_to(message, "📋 هذه القائمة:\n1. سهم تسلا\n2. سهم أبل\n3. سهم أرامكو")

# ✅ لأي أمر غير مفهوم
@bot.message_handler(func=lambda message: True)
def fallback(message):
    bot.reply_to(message, "❌ لم أفهم الأمر. اختر من الأزرار الظاهرة.")

bot.polling()