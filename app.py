import os
from flask import Flask, request
import requests

# استبدل القيم الوهمية بقيمك الحقيقية
BOT_TOKEN = "123456789:AAEep2yo54KzCLXqKHUWcTOTIODQbZsck_4"   # ← استبدل هذا
CHAT_ID = "6969597735"                                         # ← استبدل هذا

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Bot is running!"

@app.route("/send", methods=["POST"])
def send_message():
    data = request.json
    text = data.get("text", "🚫 لا توجد رسالة")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }

    try:
        response = requests.post(url, json=payload)
        print("رد تيليجرام:", response.text)
        return response.text
    except Exception as e:
        print("⚠️ خطأ أثناء إرسال الرسالة:", e)
        return {"error": str(e)}, 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
