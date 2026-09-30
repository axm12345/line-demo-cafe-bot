"""
app.py

This is the plumbing: it receives messages from LINE and sends replies back.
You generally won't need to change much here — reply_logic.py is where the
actual behavior lives.
"""

import os
from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from reply_logic import generate_reply

app = Flask(__name__)

# These come from the LINE Developers Console for your Official Account.
# Set them as environment variables — never hardcode them in the file.
CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]

configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.route("/callback", methods=["POST"])
def callback():
    """This is the URL you'll register with LINE as your webhook."""
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        # Someone (or something) sent a request that wasn't really from LINE.
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    """Called automatically for every text message LINE forwards to us."""
    user_message = event.message.text
    reply_text = generate_reply(user_message)

    with ApiClient(configuration) as api_client:
        MessagingApi(api_client).reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_text)],
            )
        )


@app.route("/", methods=["GET"])
def health_check():
    """Just so you can confirm the server is alive by visiting the URL."""
    return "Bot is running!"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
