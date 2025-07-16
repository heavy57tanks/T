import telebot
import os
import json

# ✅ إعدادات التوكن والتشات
TELEGRAM_TOKEN = "7933355250:AAH7moLKbjXd39w9A4obFpXECi1oamyruaE"
TELEGRAM_CHAT_ID = "920880801"
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# ✅ تحميل أو إنشاء الملف
FILE_PATH = "data.json"
if not os.path.exists(FILE_PATH):
    with open(FILE_PATH, "w") as f:
        json.dump({"list": []}, f)

def load_data():
    with open(FILE_PATH, "r") as f:
        return json.load(f)

def save_data(data):
    with open(FILE_PATH, "w") as f:
        json.dump(data, f)

# ✅ عرض القائمة
@bot.message_handler(commands=['عرض_القائمة'])
def show_list(message):
    data = load_data()
    items = data.get("list", [])
    if not items:
        bot.send_message(message.chat.id, "📭 القائمة فاضية يا أبو عبد الرحمن.")
    else:
        text = "📋 *القائمة الحالية:*\n"
        for i, item in enumerate(items, start=1):
            text += f"{i}. {item}\n"
        bot.send_message(message.chat.id, text, parse_mode="Markdown")

# ✅ إضافة سهم
@bot.message_handler(commands=['add'])
def add_item(message):
    item = message.text.replace("/add", "").strip()
    if not item:
        bot.send_message(message.chat.id, "❗ اكتب اسم السهم بعد الأمر.\nمثال: /add تسلا")
        return
    data = load_data()
    if item in data["list"]:
        bot.send_message(message.chat.id, f"⚠️ السهم {item} موجود بالفعل.")
    else:
        data["list"].append(item)
        save_data(data)
        bot.send_message(message.chat.id, f"✅ تم إضافة: {item}")

# ✅ حذف سهم
@bot.message_handler(commands=['remove'])
def remove_item(message):
    item = message.text.replace("/remove", "").strip()
    data = load_data()
    if item in data["list"]:
        data["list"].remove(item)
        save_data(data)
        bot.send_message(message.chat.id, f"🗑️ تم حذف: {item}")
    else:
        bot.send_message(message.chat.id, f"❌ السهم {item} غير موجود.")

# ✅ بدء البوت
bot.send_message(TELEGRAM_CHAT_ID, "✅ البوت بدأ يا أبو عبد الرحمن!")
bot.polling()