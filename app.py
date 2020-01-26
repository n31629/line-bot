from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('NZH1GBiThx8kyVidJXw4OrBIyYJjDn1Brn2kFSlNyxqz04CDgMFh42MY3gO795Zn4zorAeUyfZ0YaHNvglH9IUoVKg5oNmLCqkCHAOX2W7M8i1krUo5Kimepb+wM/IX3t43nQfRPpUKk/Wcm4RdP/AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('4ffbccd60f22e3ba47449efe8fcc86f1')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()