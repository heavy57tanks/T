from flask import Flask, request
import requests

app = Flask(__name__)

# إعدادات التوكن والمعرف
TOKEN = "7933355250:AAH7moLKbjXd39w9A4obFpXECi1oamyruaE"
ADMIN_ID = "920880801"
API_URL = f"https://api.telegram.org/bot{TOKEN}"

# قاعدة بيانات مصغرة
allowed_users = set()

# دالة إرسال الرسائل
def send(chat_id, text, buttons=None):
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if buttons:
        data["reply_markup"] = {"inline_keyboard": buttons}
    requests.post(f"{API_URL}/sendMessage", json=data)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()

    # إذا كانت رسالة جديدة
    if "message" in data:
        msg = data["message"]
        chat_id = msg["chat"]["id"]
        text = msg.get("text", "")
        username = msg["from"].get("username", "بدون اسم")

        # أمر /start
        if text == "/start":
            welcome_msg = f"""👋 مرحبًا بك في <b>التحليل الشامل</b>!

🟢 اختر نوع الاشتراك:
1️⃣ <b>الاشتراك الشهري</b>
2️⃣ <b>الاشتراك مدى الحياة</b>

📩 حدد كيف تحب يكون الرد من الإدارة 👇"""
            buttons = [
                [{"text": "📩 تسجيل - رد خاص", "callback_data": "register_private"}],
                [{"text": "📩 تسجيل - رد عام", "callback_data": "register_public"}],
                [{"text": "💰 معرفة الأسعار", "callback_data": "prices"}]
            ]
            send(chat_id, welcome_msg, buttons)

        # أوامر المدير فقط
        elif str(chat_id) == ADMIN_ID:
            if text.startswith("/add "):
                try:
                    user_id = int(text.split()[1])
                    allowed_users.add(user_id)
                    send(chat_id, f"✅ تم إضافة المستخدم: <code>{user_id}</code>")
                    send(user_id, "✅ تم قبول تسجيلك في التحليل الشامل.")
                except:
                    send(chat_id, "❌ تأكد من كتابة الأمر هكذا:\n/add [id]")

            elif text.startswith("/remove "):
                try:
                    user_id = int(text.split()[1])
                    allowed_users.discard(user_id)
                    send(chat_id, f"🚫 تم حذف المستخدم: <code>{user_id}</code>")
                except:
                    send(chat_id, "❌ تأكد من كتابة الأمر هكذا:\n/remove [id]")

            elif text == "/users":
                if allowed_users:
                    users_list = "\n".join([str(uid) for uid in allowed_users])
                    send(chat_id, f"📋 قائمة المشتركين:\n{users_list}")
                else:
                    send(chat_id, "🚫 لا يوجد مشتركين حتى الآن.")

        # إذا كان غير مسموح له
        elif chat_id not in allowed_users:
            send(chat_id, "🚫 لا تملك صلاحية الاستخدام. الرجاء التسجيل أولًا.")

    # إذا كانت ضغطة زر
    elif "callback_query" in data:
        query = data["callback_query"]
        chat_id = query["from"]["id"]
        username = query["from"].get("username", "بدون اسم")
        action = query["data"]

        if action in ["register_private", "register_public"]:
            preference = "🔒 رد خاص" if action == "register_private" else "🔓 رد عام"
            send(chat_id, f"✅ تم استلام طلبك. انتظر موافقة المدير.\nتفضيلك: {preference}")
            send(ADMIN_ID, f"""📥 طلب تسجيل جديد:

👤 المستخدم: @{username}
🆔 ID: <code>{chat_id}</code>
🎯 التفضيل: {preference}

🛠️ استخدم الأمر:
/add {chat_id}
""")

        elif action == "prices":
            prices_msg = """💳 <b>أسعار الاشتراك:</b>

- اشتراك شهري: 100 ريال
- اشتراك مدى الحياة: 500 ريال

📩 للتسجيل، ارجع واضغط على زر "📩 التسجيل" أعلاه.
"""
            send(chat_id, prices_msg)

    return "ok"