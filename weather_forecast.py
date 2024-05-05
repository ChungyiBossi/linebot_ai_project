from chatgpt_api import openai_chatgpt
from cwa_opendata_api import get_cwa_opendata


def forecast_weather(cities):

    # 取得天氣資料
    weather_data = get_cwa_opendata(cities)
    weather_data_string = ""
    for city_name in weather_data:
        city_data = [city_name]  # 城市名稱
        city_data += [f"{field}={value}" for field,
                      value in weather_data[city_name]]  # 加入天氣資料字串

        if weather_data_string:  # 組合不同縣市的資料到一起
            weather_data_string = weather_data_string + \
                ";" + ",".join(city_data)
        else:
            weather_data_string = ",".join(city_data)

    # 丟給 OpenAI 做文字生成
    weather_infomation = f'請你幫我根據以下的天氣資料，生成一段簡短的天氣預報：{weather_data_string}'
    return openai_chatgpt(weather_infomation)


if __name__ == '__main__':

    cities = ['嘉義縣']
    print(forecast_weather(cities))
