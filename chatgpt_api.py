from openai import OpenAI
from KEYS import OPENAI_API_KEY

# 使用你的api-key，並且透過OpenAI API連線到OpenAI雲端
client = OpenAI(api_key=OPENAI_API_KEY)

# 只存文字訊息
# ["訊息一", "訊息二", "訊息三"]
history = list()

def update_history(message):
    # 更新對話紀錄，不論是User or System(Chatbot)，都會以純文字的方式儲存在對話紀錄中。
    history.append(message)

def create_chatgpt_message(history, is_show_history=False):
    # 生成符合ChatGPT官方API的格式
    roles = ('user', 'system')
    messages = []
    # 先把對話紀錄反過來，用來確保最後一句話一定是User說的。
    for index, content in enumerate(reversed(history)):
        messages.append(
            {
                "role": roles[ index%2 ], 
                "content": content
            }
        )
    messages.reverse() # 最後再倒序成原來的順序

    # 決定是否要顯示歷史訊息
    if is_show_history:
        for i, message in enumerate(messages):
            print(f"History {i}: ", message)
    return messages

def openai_chatgpt(last_user_message, is_show_history=False):
    
    # 更新 User 訊息到歷史紀錄
    update_history(last_user_message)
    
    # 產生回覆
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=create_chatgpt_message(history, is_show_history=is_show_history)
    )
    response = completion.choices[0].message

    # 更新 Chatbot回覆 到歷史紀錄
    update_history(response.content)
    return response.content

def recognize_intent(user_message, predefine_intents):
    intent_recongization_message = f'''
        有下列意圖：{",".join(predefine_intents)}。
        請幫我分辨下面這句話是上述意圖中的哪一種？回覆意圖名稱。{user_message}
    '''
    # 產生回覆
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": 'user', 
                "content": intent_recongization_message
            }
        ]
    )
    response = completion.choices[0].message
    return response.content

if __name__ == '__main__':
    # print(openai_chatgpt('你好嗎今天天氣如何。'))
    weather_infomation = '請你幫我根據以下的天氣資料，生成一段天氣預報：Wx=陰時多雲,POP=80%,MinT=27C,MaxT=30T,CI=舒適'
    print(openai_chatgpt(weather_infomation, is_show_history=True))

    intents = ['天氣預報', '股市預測', '閒聊']
    print(recognize_intent('請告訴我明天的天氣狀況?', intents))
    print(recognize_intent('請告訴我明天股市會漲嗎?', intents))
    print(recognize_intent('請告訴我明天會下雨嗎?', intents))
    print(recognize_intent('你有沒有喜歡的動畫?', intents))
    print(recognize_intent('請告訴我明天股市會出太陽嗎?', intents))