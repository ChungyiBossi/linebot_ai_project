from flask import Flask, request, abort
from collections import defaultdict

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage, ImageMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    ImageMessageContent
)
# 把chatgpt的程式碼import進來
from chatgpt_api import openai_chatgpt, recognize_intent

# 天氣預報
from weather_forecast import forecast_weather

# CKIP Tools
from ckip_transformer_api import load_ner_driver, get_ner

# IMPORT 密碼進來
from KEYS import LINEBOT_ACCESS_TOKEN, LINEBOT_SECRET_KEY

ckip_model = load_ner_driver()
app = Flask(__name__)
configuration = Configuration(access_token=LINEBOT_ACCESS_TOKEN)
handler = WebhookHandler(LINEBOT_SECRET_KEY)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info(
            "Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


user_info_dict = defaultdict(
    lambda: {'entities': list(), 'previous_intent': '閒聊'})


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_message = event.message.text
    user_id = event.source.user_id

    # 取得名詞實體
    ner_tuples = get_ner(ckip_model, user_message)
    app.logger.info("User: " + user_message)  # 使用者講的話
    user_info_dict[user_id]['entities'].extend(ner_tuples)  # 記錄使用者資料，目前存在記憶體里面
    print("\tNER tuples: ", ner_tuples)  # 使用者的話裡頭，可以取得的名詞實體。

    # 辨識意圖
    predefine_intents = ['天氣', '閒聊']
    intent = recognize_intent(user_message, predefine_intents)
    previous_intent = user_info_dict[user_id]['previous_intent']

    print("Intent: ", intent)
    print("Pre-Intent: ", previous_intent)
    # 指令集
    # 預計的指令格式：!天氣 桃園市 臺北市 花蓮縣
    if user_message.startswith("!天氣") or \
       user_message.startswith("！天氣") or \
       '天氣' in intent or \
       '天氣' in previous_intent:
        chatgpt_response = search_weather(user_message, user_id)
    else:
        # 透過 chatgpt 生成回覆
        chatgpt_response = openai_chatgpt(
            last_user_message=user_message)  # 使用者講的話

    # 更新意圖
    user_info_dict[user_id]['previous_intent'] = intent

    app.logger.info("Bot: " + chatgpt_response)  # BOT 講的話
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[
                    TextMessage(text=chatgpt_response)
                ]
            )
        )


# 處理收到的圖片訊息
@handler.add(MessageEvent, message=ImageMessageContent)
def handle_image_message(event):
    # 取得圖片訊息的 ID
    image_id = event.message.id

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        # 下載圖片
        message_content = line_bot_api.get_message_content(image_id)
        with open(f"{image_id}.jpg", 'wb') as f:
            for chunk in message_content.iter_content():
                f.write(chunk)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[
                    TextMessage(text="Get Image")
                ]
            )
        )


# 意圖:查詢天氣


def search_weather(user_message, user_id):
    cities = user_message.split()[1:]
    print("cities: ", cities)
    if cities:  # 假設指令有給地區訊息
        response = forecast_weather(cities)
    else:  # 假設指令沒給地區訊息
        history_locations = [
            # 取得過往紀錄內的名詞實體
            entity for entity, entity_type in user_info_dict[user_id]['entities']
            if entity_type in ['GPE', 'LOC']  # 且為行政區名或地名
        ]
        if history_locations:
            response = forecast_weather(history_locations[-1:])
        else:
            response = '請給我一個縣市名稱，方便讓我查詢天氣唷！'

    return response


if __name__ == "__main__":
    app.run(debug=True)
