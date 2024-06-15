from KEYS import WEATHER_OPENDATA
import requests
from pprint import pprint
import json

# 36小時天氣預報資源網址
url = 'https://opendata.cwa.gov.tw' + '/api'+ '/v1/rest/datastore/F-C0032-001'

# 標頭帶入授權碼，授權碼用來辨識你的身分組
header = {
    'Authorization': WEATHER_OPENDATA, 
}
parameters = {
    'locationName': ['桃園市','臺中市', '新北市']
}

response = requests.get(
    url, headers=header, params=parameters
)

# 取得類似json資料
response_json = response.json()

# Step1：存資料，看資料
# output這個變數的生存週期，到此縮排程式碼結束後就終止
with open('api_opendata.json', 'w') as output:
    json.dump(response_json, output, indent=4)


# Step2：整理並取得特定欄位
def handle_element_unit(element_name):
    p_name_and_unit = [
        ('wx', ""),
        ('ci', ""), 
        ('pop', "%"),
        ('mint', "C"), 
        ('maxt', "C")
    ]
    
    for (p, unit) in p_name_and_unit:
        if element_name.lower() == p:
            return unit


for location in response_json['records']['location']: # 刷一遍縣市
    city = location['locationName']
    print(city) # 印出各個縣市名稱
    for weather_element in location['weatherElement']: # 刷一遍天氣欄位
        element_name = weather_element['elementName']
        parameter_name = weather_element['time'][0]['parameter']['parameterName']
        print(
            '\t', 
            element_name, # 該縣市的天氣欄位名稱
            parameter_name,  # 天氣欄位數值
            handle_element_unit(element_name) # 天氣欄位數值單位
        )
