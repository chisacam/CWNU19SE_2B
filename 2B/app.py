import json
import requests

from flask import Flask
from flask import render_template
from flask import request
from flask import make_response

app = Flask(__name__)


@app.route('/')
def mainPage():
    return render_template("index.html")


@app.route('/weather')
def getWeatherInfo():
    base_address = "https://api.openweathermap.org/data/2.5/weather?id=1846326&appid=7a60cf8ebe413584303acc4e2bf4cffe"
    req_weather = requests.get(base_address)
    base_info = req_weather.text
    result = json.loads(base_info)
    weather = result["weather"][0]["main"]
    temp = result["main"]["temp"] - 273
    icon = "http://openweathermap.org/img/w/" + result["weather"][0]["icon"] + ".png"
    """print(round(temp), weather)"""
    return render_template("weather.html", weather=weather, temp=round(temp), icon=icon)


@app.route('/bookmark')
def loadbookmarkList():
    booklist = eval(request.cookies.get('bookmark'))
    return booklist


@app.route('/recent')
def loadrecentList():
    recentlist = eval(request.cookies.get('recent'))
    return recentlist


@app.route('/search')
def test():
    """
    bookmark = {
        "경남도청": {
            "X": "111.222",
            "Y": "222.333"
        },
        "창원시청": {
            "X": "111.111",
            "Y": "222.222"
        }
    }"""

    inputstr = "경기도청"
    inputstr2 = "창원시청"
    bookmark = eval(request.cookies.get('bookmark'))
    cookie = json.dumps(bookmark, ensure_ascii=False, indent=4)
    test = json.loads(cookie)
    print(type(cookie))
    print(test["경남도청"])
#    resp = make_response("Cookie Setting Complete")
#    resp.set_cookie('bookmark', cookie)
    return print(cookie)


"""@app.route('/result')"""

if __name__ == '__main__':
    app.run(host='0.0.0.0')
