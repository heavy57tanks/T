import telebot
from telebot import types

TELEGRAM_TOKEN = "ضع التوكن هنا"
ADMIN_ID = 920880801  # رقمك الشخصي

bot = telebot.TeleBot(TELEGRAM_TOKEN)

users_data = {}

# ✅ الرد على /start
@bot.message_handler(commands=['start'])
def welcome_user(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📦 الاشتراك الشهري", "🎯 اشتراك مرة واحدة", "ℹ️ معلومات الاشتراك")
    bot.send_message(message.chat.id,
        "🎯 أهلاً بك في بوت *التحليل الشامل*.\nيرجى اختيار نوع الاشتراك:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

# ✅ الاشتراك الشهري
@bot.message_handler(func=lambda msg: msg.text == "📦 الاشتراك الشهري")
def monthly_subscription(msg):
    users_data[msg.from_user.id] = "شهري"
    bot.send_message(msg.chat.id,
        "📦 *الاشتراك الشهري: 100 ريال*\n"
        "- دعم ومقاومات فنية\n"
        "- تحليل مالي لأسهم مختارة\n"
        "- تحليلين زمنيين لأسهم من اختيارك\n"
        "- أول اشتراك يشمل تحليلين إضافيين مجانًا",
        parse_mode="Markdown"
    )
    notify_admin(msg, "📦 اشترك شهريًا")

# ✅ اشتراك مرة واحدة
@bot.message_handler(func=lambda msg: msg.text == "🎯 اشتراك مرة واحدة")
def single_subscription(msg):
    users_data[msg.from_user.id] = "مرة واحدة"
    bot.send_message(msg.chat.id,
        "🎯 *الاشتراك لمرة واحدة: 10 ريال للسهم*\n"
        "- دعم ومقاومات Color\n"
        "- تحليل زمني\n"
        "- تحليل مالي للشركات بدون مركز مالي واضح",
        parse_mode="Markdown"
    )
    notify_admin(msg, "🎯 اشترك مرة واحدة")

# ✅ معلومات الاشتراك
@bot.message_handler(func=lambda msg: msg.text == "ℹ️ معلومات الاشتراك")
def info_subscription(msg):
    bot.send_message(msg.chat.id,
        "💡 *أنواع الاشتراكات:*\n"
        "1. 📦 شهري = 100 ريال\n"
        "2. 🎯 لمرة واحدة = 10 ريال لكل سهم\n\n"
        "🛑 لا يمكن كتابة رسائل في هذا البوت، فقط اختيار من القوائم.",
        parse_mode="Markdown"
    )

# ✅ التنبيه للمشرف
def notify_admin(msg, choice_text):
    user = msg.from_user
    notice = f"👤 مستخدم جديد:\n"\
             f"اسم: {user.first_name}\n"\
             f"يوزر: @{user.username if user.username else '—'}\n"\
             f"معرف: `{user.id}`\n"\
             f"📝 اختار: {choice_text}"
    bot.send_message(ADMIN_ID, notice, parse_mode="Markdown")

# ✅ منع أي رسالة كتابة
@bot.message_handler(func=lambda msg: True)
def block_text(msg):
    bot.send_message(msg.chat.id, "❌ لا يمكن إرسال رسائل. يرجى استخدام الأزرار فقط.")

bot.polling()