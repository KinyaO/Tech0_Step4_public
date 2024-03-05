from fastapi import FastAPI, Request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from dotenv import load_dotenv
import os

# .envファイルから環境変数を読み込む
load_dotenv()

# 環境変数を使用して値を取得
CHANNEL_ACCESS_TOKEN = os.getenv('CHANNEL_ACCESS_TOKEN')
CHANNEL_SECRET = os.getenv('CHANNEL_SECRET')

app = FastAPI()

line_bot_api = LineBotApi('CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('CHANNEL_SECRET')

@app.post("/webhook")
async def line_webhook(request: Request):
    # LINEからのリクエストを取得
    signature = request.headers['X-Line-Signature']
    body = await request.body()

    # 署名を検証し、問題がなければハンドラを呼び出す
    try:
        handler.handle(body.decode(), signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        return 'OK'

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # ユーザーからのメッセージに応答
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )

# LINE Payの決済処理エンドポイント（仮）
@app.post("/linepay")
async def line_pay(request: Request):
    # ここに決済処理のロジックを実装
    return {"message": "LINE Pay Payment Process"}
