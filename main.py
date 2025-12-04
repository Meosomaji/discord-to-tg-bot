from flask import Flask, request
import requests
import html
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    })

@app.route("/", methods=["POST"])
def discord_webhook():
    data = request.json or {}
    content = data.get("content", "")
    username = data.get("username", "Discord")
    embeds = data.get("embeds", [])

    message = f"<b>{html.escape(username)}</b>\n{html.escape(content)}"

    if embeds:
        embed = embeds[0]
        title = embed.get("title")
        description = embed.get("description")
        if title:
            message += f"\n\n<b>{html.escape(title)}</b>"
        if description:
            message += f"\n{html.escape(description)}"

    send_to_telegram(message)
    return {"status": "ok"}

@app.route("/", methods=["GET"])
def home():
    return "OK — webhook is working"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
