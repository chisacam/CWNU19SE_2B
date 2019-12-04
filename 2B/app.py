from flask import Flask, redirect, url_for
from flask import render_template
from flask import jsonify
import json
from flask import request
from flask import make_response
import datetime
from OpenSSL import SSL

import bookmark
import recent
import nubija
import weather
import search


weatherClass = weather.Weather()
nubijaClass = nubija.Nubija()
bookmarkClass = bookmark.BookMark()
searchClass = search.Search()
recentClass = recent.Recent()


def timeCheck():
    KST = datetime.timezone(datetime.timedelta(hours=9))
    now = datetime.datetime.now(KST)
    nowTime = now.strftime('%H')
    return int(nowTime)


def checkServiceTime():
    if timeCheck() in [1, 2, 3]:
        return False
    else:
        return True


app = Flask(__name__)

defaultCookie = {
    "depart": [

    ],
    "dest": [

    ]
}

defaultRoute = {
    "depart": {

    },
    "dest": {

    }
}


@app.route('/')
def main_Page():
    main_weather = weatherClass.weatherInfo()
    recentList = request.cookies.get('recentlist')
    if recentList is None:
        defaultJson = json.dumps(defaultCookie, ensure_ascii=False)
        startend = json.dumps(defaultRoute, ensure_ascii=False)
        resp = make_response(render_template("index.html", weather=main_weather["weather"]))
        resp.set_cookie('recentlist', defaultJson)
        resp.set_cookie('booklist', defaultJson)
        resp.set_cookie('routeinfo', startend)
        return resp
    else:

        return render_template("index.html", weather=main_weather["weather"])


@app.route('/main', methods=['POST', 'GET'])
def result_Page():
    main_weather = weatherClass.weatherInfo()
    if request.method == "POST":

        sel = request.form["sel"]
        name = request.form["selname"]
        x = request.form["selY"]
        y = request.form["selX"]

        startEndCheck = eval(request.cookies.get('routeinfo'))

        if sel in 'depart':
            startEndCheck["depart"] = {
                name: {
                    "x": x,
                    "y": y
                }
            }
        if sel in 'dest':  # 'dest':
            startEndCheck["dest"] = {
                name: {
                    "x": x,
                    "y": y
                }
            }

        if startEndCheck["depart"]:
            if startEndCheck["dest"]:
                saveRoute = json.dumps(startEndCheck, ensure_ascii=False)
                resp = make_response(redirect(url_for('navinubija')))
                resp.set_cookie('routeinfo', saveRoute)
                return resp

        saveRoute = json.dumps(startEndCheck, ensure_ascii=False)
        resp = make_response(render_template("index.html", weather=main_weather["weather"], name=name, sel=sel))
        resp.set_cookie('routeinfo', saveRoute)
        return resp
    else:
        return render_template("index.html", weather=main_weather["weather"])


@app.route('/js')
def jse():
    geoInfo = open('static/terminalInfo.json', 'r', encoding='UTF8')
    nameInfo = open('static/terminalName.json', 'r', encoding='UTF8')
    nameInfo = json.loads(nameInfo.read())
    nameInfo = json.dumps(nameInfo, ensure_ascii=False)
    geoInfo = json.loads(geoInfo.read())
    geoInfo = json.dumps(geoInfo, ensure_ascii=False)
    return jsonify(namedata=nameInfo, geodata=geoInfo)


@app.route('/weather')
def Weather_page():
    main_weather = weatherClass.weatherInfo()
    return render_template("weather.html", weather=main_weather["weather"], temp=main_weather["temp"])


@app.route('/searchRecent', methods=['POST'])
def recent_search():
    sel = request.form['sel']
    hiddenLat = request.form['hiddenLat']
    hiddenLong = request.form['hiddenLong']
    recentList = eval(request.cookies.get('recentlist'))
    bookList = eval(request.cookies.get('booklist'))
    return recentClass.loadRecentPlaceList(sel, hiddenLat, hiddenLong, recentList, bookList, checkServiceTime())


@app.route('/searchBookmark', methods=['POST'])
def recent_bookmark():
    sel = request.form['sel']
    hiddenLat = request.form['hiddenLat']
    hiddenLong = request.form['hiddenLong']
    bookList = eval(request.cookies.get('booklist'))
    return bookmarkClass.loadBookmarkPlaceList(sel, hiddenLat, hiddenLong, bookList)


@app.route('/manageBook', methods=['POST'])
def manageBook():
    sel = request.form['sel']
    name = request.form['selname']
    y = request.form['selX']
    x = request.form['selY']
    hiddenLong = request.form['hiddenLong']
    hiddenLat = request.form['hiddenLat']
    bookmarkCheck = eval(request.cookies.get('booklist'))
    return bookmarkClass.manageBookmark(sel, name, y, x, hiddenLong, hiddenLat, bookmarkCheck)


@app.route('/nubijaSelect', methods=['POST'])
def nubijaSelect():
    sel = request.form['sel']
    x = float(request.form['selX'])
    y = float(request.form['selY'])
    hiddenLat = request.form['hiddenLat']
    hiddenLong = request.form['hiddenLong']
    return nubijaClass.nubijaTerminalSelect(sel, x, y, hiddenLat, hiddenLong, checkServiceTime())


@app.route('/searchText', methods=['POST'])
def searchtext():
    sel = request.form['sel']
    name = request.form['seartext']
    x = request.form['hiddenLong']
    y = request.form['hiddenLat']
    return searchClass.search_text(sel, name, x, y)


@app.route('/naviNubija', methods=['GET'])
def navinubija():
    route = eval(request.cookies.get('routeinfo'))
    recent = eval(request.cookies.get('recentlist'))
    return searchClass.navi_nubija(route, recent)


@app.route('/swap')
def swap():
    swap_weather = weatherClass.weatherInfo()
    route = eval(request.cookies.get('routeinfo'))
    name = ''
    isError = False
    if route["depart"]:
        for name, loc in route["depart"].items():
            route["dest"][name] = loc
        del route["depart"][name]
        resp = make_response(render_template('index.html', sel="dest", name=name, weather=swap_weather["weather"],
                                             isError=isError))
    elif route["dest"]:
        for name, loc in route["dest"].items():
            route["depart"][name] = loc
        del route["dest"][name]
        resp = make_response(render_template('index.html', sel="depart", name=name, weather=swap_weather["weather"],
                                             isError=isError))
    else:
        isError = True
        resp = make_response(render_template('index.html', isError=isError, weather=swap_weather["weather"]))

    resultRoute = json.dumps(route, ensure_ascii=False)
    resp.set_cookie('routeinfo', resultRoute)
    return resp


contextSSL = ('server.crt', 'server.key')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, ssl_context=contextSSL)
