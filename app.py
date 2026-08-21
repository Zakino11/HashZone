from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

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
        return jsonify({"error": "Telegram configuration is missing"}), 500

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": message
        },
        timeout=15
    )

    if response.ok:
        return jsonify({"success": True})

    return jsonify({"error": "Telegram message failed"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
