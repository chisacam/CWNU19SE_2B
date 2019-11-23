from flask import Flask
from flask import render_template
from flask import jsonify
import json

app = Flask(__name__)


@app.route('/')
@app.route('/main')
def main_page():
    return render_template("index.html")

@app.route('/js')
def jse():
    geoInfo = open('static/terminalInfo.json', 'r')
    nameInfo = open('static/terminalName.json', 'r')
    nameInfo = json.loads(nameInfo.read())
    nameInfo = json.dumps(nameInfo, ensure_ascii=False)
    geoInfo = json.loads(geoInfo.read())
    geoInfo = json.dumps(geoInfo, ensure_ascii=False)
    return jsonify(namedata=nameInfo)

@app.route('/weather')
def weather_page():
    return render_template("weather.html")


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True)
