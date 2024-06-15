# 聊天機器人開啟流程
1. 檢查你的程式碼跟安裝的package，尤其是在會還原的電腦上
    * pip install flask line-bot-sdk
    * 程式碼我會放在雲端硬碟，請見群組的記事本
2. 檢查ngrok的auth-token是否有設定，他相當於你的ngrok身分ID
    * 下載一個[ngrok](https://ngrok.com/download)，並且放到你的工作目錄底下
    * .\ngrok config add-authtoken xxxxxxxx
3. 啟動服務
    * 把flask app 跑起來：
        * python xxx.py
        * flask run (檔名必須要是app.py)
    * 把 ngrok 跑起來：.\ngrok http 5000
    * 複製 ngrok 給你的Forwarding網址，這是ngrok代管的外網網址。
        * 類似 https://6e0f-120-124-133-84.ngrok-free.app ，每次開啟都會不一樣，直到你關閉為止
    * 把Forwarding 的網址，複製到linebot webhook server的欄位

# 串接ChatGPT
1. 到OpenAI 官方網站尋找sample code
    * https://platform.openai.com/docs/quickstart?context=python
2. 根據步驟，建立此專案使用的API key
    * https://platform.openai.com/docs/quickstart/step-2-set-up-your-api-key
    * 保留好你的api key，因為他不會再出現了
    * 建立一個 KEYS.py 檔案，把 API Key 當作變數放入
        * OPENAI_API_KEY=YOUR_API_KEY
        * 新增一個變數，各種key作為字串assign給該變數，你也可以把其他種類的金鑰透過這種方式整理起來。

3. 建立 ChatGPT sample，你可以參考 chatgpt_api_0401.py 這個檔案，裡面包含：
    * 蒐集對話紀錄，User & Chatbot
    * 生成符合chatgpt的對話紀錄格式


# 下載天氣資料，請參考投影片
[下載天氣資料投影片](https://www.canva.com/design/DAGBuz6PeiE/TLR-XvXXW-3FBmFW0Vo-yg/edit)
1. 你要先辦中央氣象署開放資料的帳號；https://opendata.cwa.gov.tw/index
2. 保留你的授權碼，在你的程式去請求資料的時候，使用你的授權碼。
3. 安裝python package:
    >pip install requests 


# 電腦視覺
## OpenCV-Python API
1. 安裝opencv：pip install opencv-python
2. 下載 [Cascade Model](https://github.com/opencv/opencv/tree/4.x/data/haarcascades)
3. 實作臉部辨識的模組：
    * 上傳圖片的(非即時的)
    * 取用camera擷取的(即時的)
4. 串接到linebot上面
    * 處理收到圖片的流程:
        * 儲存圖片為image.jpg到本地端
        * 臉部辨識該圖片，並另存一張新圖片image_faces.jpg到本地端
        * 上傳辯識結果image_faces.jpg到imgur，並取得URL
        * 回覆使用者辯識結果的文字(eg. 幾個臉被找到了)跟結果圖(imgur url的圖)
        > 因為linebot sdk 回傳圖片訊息的方式，只能透過公開的URL讓Line官方下載，所以我們才需要先上傳到免費空間，再取得URL。

    * 上傳資料到 Imgur: [上傳到Imgur流程](https://medium.com/front-end-augustus-study-notes/imgur-api-3a41f2848bb8)
        * [申請Imgur Account/APP，並取得你的 Imgur Client ID & Secret](https://api.imgur.com/oauth2/addclient) 
        * [Imgur Python API](https://github.com/Imgur/imgurpython/tree/master)
            > pip install imgurpython
## Mediapipe
* 安裝python pacakge：
    > pip install mediapipe tensorflow opencv-python

* 測試程式:
    1. [下載測試模型，並放到當前目錄](https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/latest/blaze_face_short_range.tflite)
    2. [測試程式](https://steam.oxxostudio.tw/category/python/ai/ai-mediapipe-2023.html)
    3. [測試模型(待商確定)]
    4. 整合到linebot中


#### 實作參考
* [Steam OpenCV](https://steam.oxxostudio.tw/category/python/ai/opencv-index.html)
* [Steam Mediapipe](https://steam.oxxostudio.tw/category/python/ai/ai-mediapipe-2023.html)
# 安裝CKIP工具，用此工具來分析你的文本資料。
[GITHUB](https://github.com/ckiplab/ckip-transformers)
1. pip install torch
2. pip install transformers
3. pip install ckip_transformers 

> 根據範例程式碼，你可以直接下載對應的模型，不同目標的模型是分開的，所以會需要下載多個

>下游任務的模型是分開的，每一台裝置只要下載一次就好，除非有更新
