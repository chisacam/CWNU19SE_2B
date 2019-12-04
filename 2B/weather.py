import requests
import json


class Weather:
    def weatherInfo(self):
        base_address = "https://api.openweathermap.org/data/2.5/weather?id=1846326&appid=7a60cf8ebe413584303acc4e2bf4cffe"
        req_weather = requests.get(base_address)
        base_info = req_weather.text
        weatherResult = json.loads(base_info)
        weather = weatherResult["weather"][0]["main"]
        temp = weatherResult["main"]["temp"] - 273
        icon = weatherResult["weather"][0]["icon"]
        if icon in ["50n", "50d"]:
            weather = '/static/icon/weather/mist.svg'
        else:
            weather = weather.lower()
            weather = '/static/icon/weather/{}.svg'.format(weather)
        weatherDict = {
            "weather": weather,
            "temp": round(temp)
        }
        return weatherDict
