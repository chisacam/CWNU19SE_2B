from flask import Flask
from flask import render_template
from flask import jsonify
import json
from flask import request
from flask import make_response
import requests

app = Flask(__name__)


@app.route('/')
@app.route('/main')
def main_Page():
    return render_template("index.html")

@app.route('/js')
def jse():
    geoInfo = open('static/terminalInfo.json', 'r')
    nameInfo = open('static/terminalName.json', 'r')
    nameInfo = json.loads(nameInfo.read())
    nameInfo = json.dumps(nameInfo, ensure_ascii=False)
    geoInfo = json.loads(geoInfo.read())
    geoInfo = json.dumps(geoInfo, ensure_ascii=False)
    return jsonify(namedata=nameInfo, geodata=geoInfo)

@app.route('/weather')
def Weather_page():
    base_address = "https://api.openweathermap.org/data/2.5/weather?id=1846326&appid=7a60cf8ebe413584303acc4e2bf4cffe"
    req_weather = requests.get(base_address)
    base_info = req_weather.text
    result = json.loads(base_info)
    weather = result["weather"][0]["main"]
    temp = result["main"]["temp"] - 273
    weather = weather.lower()
    weather = '/static/icon/weather/{}.svg'.format(weather)
    print(weather)
    return render_template("weather.html", weather=weather, temp=round(temp))


@app.route('/searchRecent', methods=['POST'])
def recent_search():
    print(request.form['selector'])
    #recentlist = eval(request.cookies.get('recent'))
    return render_template("search_recent.html")


@app.route('/searchBookmark')
def recent_bookmark():
    #booklist = eval(request.cookies.get('bookmark'))
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
