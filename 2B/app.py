from flask import Flask
from flask import render_template
from flask import jsonify
import json
from flask import request
from flask import make_response
import requests

app = Flask(__name__)


@app.route('/')
def main_Page():
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

@app.route('/searchRecent')
 def recent_search():
     return render_template("search_recent.html")


 @app.route('/searchBookmark')
 def recent_bookmark():
     return render_template("search_bookmark.html")


 @app.route('/busterminalSelect')
 def busTerminalSelect():
     return render_template('bus_terminal_select.html')


 @app.route('/nubijaSelect')
 def nubijaselect():
     return render_template('Nubija_terminal_select.html')


 @app.route('/searchText')
 def search_text():
     return render_template("search_text.html")


 @app.route('/naviNubija')
 def navi_nibija():
     return render_template("navigation_nubija.html")

 @app.route('/naviBus')
 def navi_bus():
     return render_template('navigation_bus.html')


@app.route('/bookmark')
def loadbookmarkList():
    booklist = eval(request.cookies.get('bookmark'))
    return booklist


@app.route('/recent')
def loadrecentList():
    recentlist = eval(request.cookies.get('recent'))
    return recentlist


if __name__ == '__main__':
    app.run(host='0.0.0.0')
