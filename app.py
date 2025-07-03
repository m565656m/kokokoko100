from flask import Flask, request
import requests
import os

TOKEN = "7880550955:AAEep2yo54KzCLXqKHUWcTOTIODQbZsck_4"
CHAT_ID = "6969597735"

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

@app.route("/send", methods=["POST"])
def send_message():
    data = request.json
    text = data.get("text", "No message provided")
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }
    r = requests.post(url, json=payload)
    return str(r.json())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)