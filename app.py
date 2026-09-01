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

    # =====================================================
    # CUSTOMER DATA
    # =====================================================

    order_number = data.get("orderNumber", "")
    name = data.get("name", "")
    email = data.get("email", "")
    contact = data.get("contact", "")
    country = data.get("country", "")
    address = data.get("address", "")
    payment = data.get("payment", "")

    # =====================================================
    # ORDER DATA
    # =====================================================

    products = data.get("products", [])
    total = data.get("total", 0)

    # =====================================================
    # PRODUCTS
    # =====================================================

    products_text = ""

    for product in products:

        product_name = product.get("name", "")
        quantity = product.get("quantity", 0)
        price = product.get("price", 0)

        products_text += (
            f"\n📦 {product_name}"
            f"\n   الكمية: {quantity}"
            f"\n   السعر: ${price:,}\n"
        )

    # =====================================================
    # TELEGRAM MESSAGE
    # =====================================================

    message = f"""
🔔 HASHZONE — طلب جديد

🆔 رقم الطلب:
{order_number}

━━━━━━━━━━━━━━━━━━

👤 الاسم:
{name}

📧 البريد الإلكتروني:
{email}

📞 Telegram / WhatsApp:
{contact}

🌍 الدولة:
{country}

📍 العنوان:
{address}

━━━━━━━━━━━━━━━━━━

🛒 المنتجات:
{products_text}

💰 الإجمالي:
${total:,}

💳 طريقة الدفع:
{payment}

⏳ حالة الدفع:
قيد التحقق

━━━━━━━━━━━━━━━━━━
HASHZONE
"""

    # =====================================================
    # TELEGRAM CONFIGURATION
    # =====================================================

    if not BOT_TOKEN or not CHAT_ID:

        return jsonify({
            "success": False,
            "error": "Telegram configuration is missing"
        }), 500

    url = (
        f"https://api.telegram.org/"
        f"bot{BOT_TOKEN}/sendMessage"
    )

    # =====================================================
    # SEND TO TELEGRAM
    # =====================================================

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

            return jsonify({
                "success": True
            }), 200

        return jsonify({
            "success": False,
            "error": "Telegram message failed"
        }), 500

    except requests.RequestException as error:

        print("Telegram Error:", error)

        return jsonify({
            "success": False,
            "error": "Could not connect to Telegram"
        }), 500


if __name__ == "__main__":

    port = int(
        os.getenv("PORT", 5000)
    )

    app.run(
        host="0.0.0.0",
        port=port
    )
