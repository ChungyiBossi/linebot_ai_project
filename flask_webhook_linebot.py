from flask import Flask, request, abort
import requests
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

# OpenCV Face Detection
from opencv_face_detector import detect_faces

# Imgur Upload
from imgur_upload import upload_image_to_imgur

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


# Key: User id, Value: dictionary
user_info_dict = defaultdict(lambda:
                             {'entities': list(), 'previous_intent': '閒聊'}
                             )


@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event):
    user_message = event.message.text
    user_id = event.source.user_id

    # 取得名詞實體
    ner_tuples = get_ner(ckip_model, user_message)
    user_info_dict[user_id]['entities'].extend(ner_tuples)  # 記錄使用者資料，目前存在記憶體里面

    # 辨識意圖
    predefine_intents = ['天氣', '閒聊']  # 目前有的 intent
    intent = recognize_intent(user_message, predefine_intents)
    previous_intent = user_info_dict[user_id]['previous_intent']

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

    # log
    app.logger.info("User: " + user_message)  # 使用者講的話
    app.logger.info("\tNER tuples: " + str(ner_tuples))  # 使用者的話裡頭，可以取得的名詞實體。
    app.logger.info("\tIntent: " + intent + ", Pre-Intent: " + previous_intent)
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


def search_weather(user_message, user_id):
    cities = user_message.split()[1:]
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


@handler.add(MessageEvent, message=ImageMessageContent)
def handle_image_message(event):
    image_id = event.message.id
    reply_message = get_image_reply_message(image_id)  # 確定取得圖片
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=reply_message
            )
        )


def get_image_reply_message(image_id):
    # 拿圖片的資料
    image_url = f'https://api-data.line.me/v2/bot/message/{image_id}/content'
    response = requests.get(
        url=image_url,
        headers={
            'Authorization': f'Bearer {LINEBOT_ACCESS_TOKEN}',
            'Content-Type': 'image/png'
        }
    )
    app.logger.info("Get Image Content：" + str(response.status_code))

    reply_message = list()
    if response.status_code > 200:
        # 取得圖片有問題，可能是line server的問題‧
        text_response_to_user = '找不到圖片。'
    else:
        # OpenCV 臉部辨識
        with open("image.jpg", 'wb') as image_file:
            image_file.write(response.content)
            image_file.flush()
        text_response_to_user = '找到圖片了。'
        number_of_faces = detect_faces('image.jpg')
        if number_of_faces > 0:  # 當臉被找到，修改文字回覆
            # 文字回覆
            text_response_to_user = text_response_to_user + \
                f" 找到{number_of_faces}張臉。"
            # 圖片回覆
            link = upload_image_to_imgur('image_faces.jpg')  # 上傳到 imgur
            linebot_image_mesaage = ImageMessage(
                originalContentUrl=link, previewImageUrl=link)
            reply_message.append(linebot_image_mesaage)
    reply_message.append(TextMessage(text=text_response_to_user))
    return reply_message


if __name__ == "__main__":
    app.run(debug=True)
