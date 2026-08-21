from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


@app.route("/", methods=["GET"])
def home():
    return "HashZone Backend is running!"


@app.route("/order", methods=["POST"])
def order():
    data = request.get_json(silent=True) or {}

    name = data.get("name", "")
    country = data.get("country", "")
    address = data.get("address", "")
    phone = data.get("phone", "")

    message = f"""
🔔 New HashZone Order

👤 Name: {name}
🌍 Country: {country}
📍 Address: {address}
📞 Phone: {phone}
"""

    if not BOT_TOKEN or not CHAT_ID:
        return jsonify({
            "success": False,
            "error": "Telegram configuration is missing"
        }), 500

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    try:
        response = requests.post(
            url,
            json={
                "chat_id": CHAT_ID,
                "text": message
            },
            timeout=15
        )

        if response.ok:
            return jsonify({"success": True}), 200

        return jsonify({
            "success": False,
            "error": "Telegram message failed"
        }), 500

    except requests.RequestException:
        return jsonify({
            "success": False,
            "error": "Could not connect to Telegram"
        }), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
