from KEYS import WEATHER_OPENDATA
import requests

tw_cities = [
    "宜蘭縣", "花蓮縣", "臺東縣", "澎湖縣", "金門縣",
    "連江縣", "臺北市", "新北市", "桃園市", "臺中市",
    "臺南市", "高雄市", "基隆市", "新竹縣", "新竹市",
    "苗栗縣", "彰化縣", "南投縣", "雲林縣", "嘉義縣",
    "嘉義市", "屏東縣"
]


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


def get_cwa_opendata(cities_name):
    # 36小時天氣預報資源網址
    url = 'https://opendata.cwa.gov.tw' + '/api' + '/v1/rest/datastore/F-C0032-001'

    # 標頭帶入授權碼，授權碼用來辨識你的身分組
    header = {
        'Authorization': WEATHER_OPENDATA,
    }
    parameters = {
        'locationName': cities_name
    }

    response_json = requests.get(
        url,
        headers=header,
        params=parameters
    ).json()

    locations_info = dict()  # 結構化存天氣資料用的資料格式
    for location in response_json['records']['location']:  # 刷一遍縣市
        city = location['locationName']
        weather_infomation = list()
        for weather_element in location['weatherElement']:  # 刷一遍天氣欄位
            element_name = weather_element['elementName']
            parameter_name = weather_element['time'][0]['parameter']['parameterName']
            weather_infomation.append(
                (
                    element_name,  # 天氣資訊的欄位名稱
                    # 天氣資訊的數值 + 單位
                    parameter_name + handle_element_unit(element_name)
                )
            )
        locations_info[city] = weather_infomation

    for city_name in cities_name:
        if city_name not in tw_cities:  # 檢查縣市名稱是否合法
            print(f"Something wrong: {city_name} is not a Taiwan city.")

    return locations_info


if __name__ == '__main__':
    from pprint import pprint
    cities = ['嘉義市', '花蓮縣', '臺北市']
    pprint(get_cwa_opendata(cities))
