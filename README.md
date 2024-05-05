# 聊天機器人開啟流程
1. 檢查你的程式碼跟安裝的package，尤其是在會還原的電腦上
    * pip install flask line-bot-sdk
    * 程式碼我會放在雲端硬碟，請見群組的記事本
2. 檢查ngrok的auth-token是否有設定，他相當於你的ngrok身分ID
    * 下載一個ngrok.exe，並且放到你的工作目錄底下
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
## https://www.canva.com/design/DAGBuz6PeiE/TLR-XvXXW-3FBmFW0Vo-yg/edit
1. 你要先辦中央氣象署開放資料的帳號；https://opendata.cwa.gov.tw/index
2. 保留你的授權碼，在你的程式去請求資料的時候，使用你的授權碼。
3. pip install requests 


# 安裝CKIP工具，用此工具來分析你的文本資料。
## GITHUB: https://github.com/ckiplab/ckip-transformers
1. pip install torch
2. pip install transformers
3. pip install ckip_transformers 

## 根據範例程式碼，你可以直接下載對應的模型，不同目標的模型是分開的，所以會需要下載多個
## -> 下游任務的模型是分開的
## 每一台裝置只要下載一次就好，除非有更新