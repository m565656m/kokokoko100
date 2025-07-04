from flask import Flask, request
import requests
import os

# قراءة التوكن والشات آي دي من متغيرات البيئة
7880550955:AAEep2yo54KzCLXqKHUWcTOTIODQbZsck_4 = os.environ.get("7880550955:AAEep2yo54KzCLXqKHUWcTOTIODQbZsck_4")
6969597735=os.environ.get("6969597735")

# تأكد إنهم موجودين
if not 7880550955:AAEep2yo54KzCLXqKHUWcTOTIODQbZsck_4 or not 6969597735:
    raise ValueError("⚠️ BOT_TOKEN أو CHAT_ID مفقودين من Environment Variables!")

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Bot is running!"

@app.route("/send", methods=["POST"])
def send_message():
    data = request.json
    text = data.get("text", "🚫 لا توجد رسالة")

    url = f"https://api.telegram.org/bot{7880550955:AAEep2yo54KzCLXqKHUWcTOTIODQbZsck_4}/sendMessage"
    payload = {
        "6969597735": CHAT_ID,
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
