import math
from bs4 import BeautifulSoup
from flask import Flask, redirect, url_for
from flask import render_template
from flask import jsonify
import json
from flask import request
from flask import make_response
import requests
import re
import datetime


def weatherInfo():
    base_address = "https://api.openweathermap.org/data/2.5/weather?id=1846326&appid=7a60cf8ebe413584303acc4e2bf4cffe"
    req_weather = requests.get(base_address)
    base_info = req_weather.text
    weatherResult = json.loads(base_info)
    weather = weatherResult["weather"][0]["main"]
    temp = weatherResult["main"]["temp"] - 273
    icon = weatherResult["weather"][0]["icon"]
    if icon in "50d":
        weather = '/static/icon/weather/mist.svg'
    else:
        weather = weather.lower()
        weather = '/static/icon/weather/{}.svg'.format(weather)
    weatherDict = {
        "weather": weather,
        "temp": round(temp)
    }
    return weatherDict


def timeCheck():
    now = datetime.datetime.now()
    nowTime = now.strftime('%H')
    return int(nowTime)


def getTerminalInfo():
    req = requests.get('https://www.nubija.com/terminal/terminalState.do')
    html = req.text
    terminalInfo = []
    soup = BeautifulSoup(html, 'html.parser')
    stic = soup.find_all("a", {"href": re.compile("javascript:showMapInfoWindow.")})

    for k in stic:
        k = k.get("href").replace("javascript:showMapInfoWindow(", "").replace(");", "").replace("\'", "").split(", ")
        terminalInfo.append([k[1], k[2]])
    return terminalInfo


app = Flask(__name__)
IDkey = "jpfybhk69d"
SecretKey = "RuIMY0ILxMIf6ZZCyA9BIb2syBOXqnJrVEYzP5GX"
"""
[
    {
        "창원시청":{
            "X":"123.123",
            "Y":"345.345",
            "isBook":"Yes"
        }
    }, # 최근기록 리스트
    {
        "창원대학교":{
            "X":"342.423",
            "Y":"123.523"
        } # 북마크 리스트
    }
]
"""
defaultCookie = {
    "depart": [

    ],
    "dest": [

    ]
}
"""
defaultRoute = {
    "depart": {

    },
    "dest": {
    
    }
}
"""
defaultRoute = {
    "depart": {

    },
    "dest": {

    }
}


@app.route('/')
def main_Page():
    main_weather = weatherInfo()
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
        print(recentList)
        return render_template("index.html", weather=main_weather["weather"])


@app.route('/main', methods=['POST', 'GET'])
def result_Page():
    main_weather = weatherInfo()
    if request.method == "POST":

        sel = request.form["sel"]
        name = request.form["selname"]
        x = request.form["selY"]
        y = request.form["selX"]

        startEndCheck = eval(request.cookies.get('routeinfo'))
        print(startEndCheck)
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
                resp = make_response(redirect(url_for('navi_nubija')))
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
    weather = weatherInfo()
    return render_template("weather.html", weather=weather["weather"], temp=weather["temp"])


@app.route('/searchRecent', methods=['POST'])
def recent_search():
    if timeCheck() in [1, 2, 3, 4]:
        isServiceTime = False
    else:
        isServiceTime = True
    sel = request.form['sel']
    hiddenLat = request.form['hiddenLat']
    hiddenLong = request.form['hiddenLong']
    recentList = eval(request.cookies.get('recentlist'))
    bookList = eval(request.cookies.get('booklist'))
    recentDepartLen = len(recentList["depart"])
    recentDestLen = len(recentList["dest"])
    bookDepartLen = len(bookList["depart"])
    bookDestLen = len(bookList["dest"])
    print(recentList)
    if bookDepartLen != 0:
        for checkRecent in range(0, recentDepartLen):
            for key, value in recentList["depart"][checkRecent].items():
                for checkBook in range(0, bookDepartLen):
                    if key in bookList["depart"][checkBook]:
                        recentList["depart"][checkRecent][key]["isBook"] = "Yes"
                        break
                    else:
                        recentList["depart"][checkRecent][key]["isBook"] = "Nope"
    if bookDestLen != 0:
        for checkRecent in range(0, recentDestLen):
            for key, value in recentList["dest"][checkRecent].items():
                for checkBook in range(0, bookDestLen):
                    if key in bookList["dest"][checkBook]:
                        recentList["dest"][checkRecent][key]["isBook"] = "Yes"
                        break
                    else:
                        recentList["dest"][checkRecent][key]["isBook"] = "Nope"

    if sel in 'depart':  # 출발지
        setCookie = json.dumps(recentList, ensure_ascii=False)
        resp = make_response(render_template("search_recent.html", resultList=recentList["depart"], sel=sel,
                               isServiceTime=isServiceTime, hiddenLong=hiddenLong, hiddenLat=hiddenLat))
        resp.set_cookie('recentlist', setCookie)
        return resp

    if sel in 'dest':  # 목적지
        setCookie = json.dumps(recentList, ensure_ascii=False)
        resp = make_response(render_template("search_recent.html", resultList=recentList["dest"], sel=sel,
                                             isServiceTime=isServiceTime, hiddenLong=hiddenLong, hiddenLat=hiddenLat))
        resp.set_cookie('recentlist', setCookie)
        return resp


@app.route('/searchBookmark', methods=['POST'])
def recent_bookmark():
    sel = request.form['sel']
    hiddenLat = request.form['hiddenLat']
    hiddenLong = request.form['hiddenLong']
    bookList = eval(request.cookies.get('booklist'))
    if sel in 'depart':  # 출발지
        return render_template("search_bookmark.html", resultList=bookList["depart"], sel=sel,
                               hiddenLong=hiddenLong, hiddenLat=hiddenLat)

    if sel in 'dest':  # 목적지
        return render_template("search_bookmark.html", resultList=bookList["dest"], sel=sel,
                               hiddenLong=hiddenLong, hiddenuserLat=hiddenLat)


@app.route('/nubijaSelect', methods=['POST'])
def nubijaTerminalSelect():
    sel = request.form['sel']
    y = float(request.form['selX'])
    x = float(request.form['selY'])
    distList = dict()
    terminalInfo = getTerminalInfo()
    selectResult = []

    with open('static/terminalInfo.json', 'r', encoding='UTF8') as json_nubiloc:
        json_locdata = json.load(json_nubiloc)

        for i in json_locdata:
            dist = math.pow((x - json_locdata[i][0]), 2) + math.pow((y - json_locdata[i][1]), 2)
            distList[i] = math.sqrt(dist)

        rankTemp = sorted(distList.items(), key=lambda t: t[1])

        with open('static/terminalName.json', 'r', encoding='UTF8') as json_nubiname:
            json_nubidata = json.load(json_nubiname)
            check = 0
            for j in range(0, 278):
                if terminalInfo[int(rankTemp[int(j)][0])][0] != 0 or terminalInfo[int(rankTemp[int(j)][0])][1] != 0:

                    check = check + 1
                    selectResult.append({
                        "name": json_nubidata[rankTemp[int(j)][0]],
                        "loc": json_locdata[rankTemp[int(j)][0]],
                        "info": terminalInfo[int(rankTemp[int(j)][0])]
                    })
                    if check is 3:
                        break

    return render_template('Nubija_terminal_select.html', selectResult=selectResult, sel=sel)


@app.route('/searchText', methods=['POST'])
def search_text():
    sel = request.form['sel']
    name = request.form['seartext']
    x = request.form['hiddenLong']
    y = request.form['hiddenLat']
    print(sel, name, x, y)
    params = {'query': name, "coordinate": x + "," + y}
    headers = {"X-NCP-APIGW-API-KEY-ID": IDkey, "X-NCP-APIGW-API-KEY": SecretKey}
    base_search_addr = "https://naveropenapi.apigw.ntruss.com/map-place/v1/search"
    res = requests.get(base_search_addr, params=params, headers=headers)
    code = res.status_code

    if code == 200:
        test = res.json()
        print(test)
        textResult = res.json()["places"]
        if sel in 'depart':  # 출발지
            return render_template("search_text.html", result=textResult, sel=sel, hiddenLong=x, hiddenLat=y)

        if sel in 'dest':  # 목적지
            return render_template("search_text.html", result=textResult, sel=sel, hiddenLong=x, hiddenLat=y)

    else:
        print(code)


@app.route('/naviNubija', methods=['GET'])
def navi_nubija():
    route = eval(request.cookies.get('routeinfo'))
    print(route)
    x1 = ''
    x2 = ''
    y1 = ''
    y2 = ''
    name1 = ''
    name2 = ''
    for key, value in route["depart"].items():
        name1 = key
        x1 = value["x"]
        y1 = value["y"]
    for key, value in route["dest"].items():
        name2 = key
        x2 = value["x"]
        y2 = value["y"]
    params = {'start': x1 + "," + y1, "goal": x2 + "," + y2}
    headers = {"X-NCP-APIGW-API-KEY-ID": IDkey, "X-NCP-APIGW-API-KEY": SecretKey}
    base_search_addr = "https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving"
    res = requests.get(base_search_addr, params=params, headers=headers)
    code = res.status_code
    straight = [1, 21, 28, 54, 55, 56, 91, 98]
    turnleft = [2, 8, 12, 25, 95]
    turnright = [3, 15, 31, 101]
    left = [4, 11, 13, 23, 24, 26, 27, 41, 42, 57, 58, 62, 63, 64, 65, 81, 93, 94, 96, 97]
    right = [5, 14, 16, 29, 30, 32, 33, 66, 67, 71, 72, 73, 74, 82, 99, 100, 102, 103]
    uturn = [6, 22, 34, 92, 104]
    flag = [87, 88]
    iconaddr = "/static/icon/navi/"
    if code == 200:
        tem = []
        icons = []
        js = res.json()
        if js['code'] == 0:
            guide = js["route"]["traoptimal"][0]["guide"]
            # print(js)
            # print(tem)
            for i in guide:
                tem.append([i["instructions"]])
                if i["type"] in straight:
                    icons.append(iconaddr + "straight.svg")
                elif i["type"] in turnleft:
                    icons.append(iconaddr + "turnleft.svg")
                elif i["type"] in turnright:
                    icons.append(iconaddr + "turnright.svg")
                elif i["type"] in left:
                    icons.append(iconaddr + "left.svg")
                elif i["type"] in right:
                    icons.append(iconaddr + "right.svg")
                elif i["type"] in uturn:
                    icons.append(iconaddr + "uturn.svg")
                elif i["type"] in flag:
                    icons.append(iconaddr + "flag.svg")
                else:
                    icons.append(iconaddr + "else.svg")

            recentList = eval(request.cookies.get('recentlist'))
            departLen = len(recentList['depart'])
            destLen = len(recentList['dest'])
            if departLen == 0:
                recentList['depart'].append({
                    name1: {
                        "x": x1,
                        "y": y1,
                        "isBook": "Nope"
                    }
                })
            if destLen == 0:
                recentList['dest'].append({
                    name2: {
                        "x": x2,
                        "y": y2,
                        "isBook": "Nope"
                    }
                })
            if destLen != 0 and departLen != 0:
                isInDepart = False
                isInDest = False
                for check in range(0, departLen):
                    if name1 in recentList['depart'][check]:
                        if check != departLen - 1:
                            temp = recentList['depart'][check]
                            for move in range(check, departLen - 1):
                                recentList['depart'][move] = recentList['depart'][move + 1]
                            del recentList['depart'][departLen - 1]
                            recentList['depart'].append(temp)
                            isInDepart = True
                        else:
                            isInDepart = True

                if isInDepart is False:
                    if departLen >= 5:
                        del recentList['depart'][0]
                        recentList['depart'].append({
                            name1: {
                                "x": x1,
                                "y": y1,
                                "isBook": "Nope"
                            }
                        })
                    else:
                        recentList['depart'].append({
                            name1: {
                                "x": x1,
                                "y": y1,
                                "isBook": "Nope"
                            }
                        })

                for check in range(0, destLen):
                    if name2 in recentList['dest'][check]:
                        if name2 in recentList['dest'][check]:
                            if check != destLen - 1:
                                temp = recentList['dest'][check]
                                for move in range(check, destLen - 1):
                                    recentList['dest'][move] = recentList['dest'][move + 1]
                                del recentList['dest'][destLen - 1]
                                recentList['dest'].append(temp)
                                isInDest = True
                            else:
                                isInDest = True

                if isInDest is False:
                    if departLen >= 5:
                        del recentList['dest'][0]
                        recentList['dest'].append({
                            name2: {
                                "x": x2,
                                "y": y2,
                                "isBook": "Nope"
                            }
                        })
                    else:
                        recentList['dest'].append({
                            name2: {
                                "x": x2,
                                "y": y2,
                                "isBook": "Nope"
                            }
                        })
            temp = json.dumps(recentList, ensure_ascii=False)
            temp2 = json.dumps(defaultRoute, ensure_ascii=False)
            resp = make_response(render_template("navigation_nubija.html", tem=tem, icons=icons,
                                                 start=name1, end=name2))
            resp.set_cookie("routeinfo", temp2)
            resp.set_cookie("recentlist", temp)
            return resp
        else:
            temp2 = json.dumps(defaultRoute, ensure_ascii=False)
            resp = make_response(render_template("navigation_nubija.html", tem=[["네이버API에러"], ["길찾기실패"]],
                                                 icons=[iconaddr + "else.svg"], start=name1, end=name2))
            resp.set_cookie("routeinfo", temp2)
            return resp
    else:
        print(code)


@app.route('/manageBook', methods=['POST'])
def manageBook():
    sel = request.form['sel']
    name = request.form['selname']
    y = request.form['selX']
    x = request.form['selY']
    hiddenLat = request.form['hiddenLong']
    hiddenLong = request.form['hiddenLat']
    resp = make_response()
    print(sel, name, x, y, hiddenLat, hiddenLong)
    isInDepart = False
    isInDest = False
    bookmarkCheck = eval(request.cookies.get('booklist'))
    departLen = len(bookmarkCheck["depart"])
    destLen = len(bookmarkCheck["dest"])
    print(bookmarkCheck)
    print(departLen, destLen)
    if sel in 'depart':
        if departLen == 0:
            bookmarkCheck["depart"].append({
                name: {
                    "x": x,
                    "y": y
                }
            })
        else:
            for check in range(0, len(bookmarkCheck["depart"]) - 1):
                if name in bookmarkCheck["depart"][check]:
                    del bookmarkCheck["depart"][check]
                    isInDepart = True
            if isInDepart is False:
                bookmarkCheck["depart"].append({
                    name: {
                        "x": x,
                        "y": y
                    }
                })
        resp = make_response(render_template('search_bookmark.html', resultList=bookmarkCheck["depart"], sel=sel,
                                             hiddenLong=hiddenLong, hiddenLat=hiddenLat))
    if sel in 'dest':
        if destLen == 0:
            bookmarkCheck["dest"].append({
                name: {
                    "x": x,
                    "y": y
                }
            })
        else:
            for check in range(0, len(bookmarkCheck["dest"]) - 1):
                if name in bookmarkCheck["dest"][check]:
                    del bookmarkCheck["dest"][check]
                    isInDest = True
            if isInDest is False:
                bookmarkCheck["dest"].append({
                    name: {
                        "x": x,
                        "y": y
                    }
                })
        resp = make_response(render_template('search_bookmark.html', resultList=bookmarkCheck["dest"], sel=sel,
                                             hiddenLong=hiddenLong, hiddenLat=hiddenLat))
    print(bookmarkCheck)
    resultBook = json.dumps(bookmarkCheck, ensure_ascii=False)
    resp.set_cookie('booklist', resultBook)
    return resp


@app.route('/swap')
def swap():
    route = eval(request.cookies.get('routeinfo'))
    name = ''
    if route["depart"]:
        for name, loc in route["depart"].items():
            route["dest"][name] = loc
        del route["depart"][name]
        resp = make_response(render_template('index.html', sel="dest", name=name))
    else:
        for name, loc in route["dest"].items():
            route["depart"][name] = loc
        del route["dest"][name]
        resp = make_response(render_template('index.html', sel="depart", name=name))
    resultRoute = json.dumps(route, ensure_ascii=False)
    resp.set_cookie('routeinfo', resultRoute)
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
