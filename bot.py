from flask import Flask, request
import requests

app = Flask(__name__)

# ✅ التوكن الخاص ببوتك
TOKEN = "7933355250:AAH7moLKbjXd39w9A4obFpXECi1oamyruaE"
API_URL = f"https://api.telegram.org/bot{TOKEN}"

@app.route("/")
def home():
    return "✅ البوت يعمل بنجاح على Render!"

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id