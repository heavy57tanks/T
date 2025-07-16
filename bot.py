import telebot

# إعدادات التوكن والمعرف
TELEGRAM_TOKEN = "7933355250:AAH7moLKbjXd39w9A4obFpXECi1oamyruaE"
MANAGER_ID = "920880801"
MANAGER_USERNAME = "التحليل الشامل"

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def start_msg(message):
    bot.send_message(message.chat.id, f"""
مرحباً بك في قناة {MANAGER_USERNAME} 📊

🛡️ فقط المدير يستطيع إرسال الرسائل.
📌 للاشتراك الشهري أو تحليل سهم لمرة واحدة، تواصل معنا.

💵 الأسعار:
- اشتراك سهم واحد: 10 ريال
- اشتراك شهري شامل: 100 ريال
    """)

# تشغيل البوت
print("🤖 البوت يعمل الآن...")
bot.infinity_polling()
