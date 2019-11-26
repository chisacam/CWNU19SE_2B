import math
from bs4 import BeautifulSoup
from flask import Flask
from flask import render_template
from flask import jsonify
import json
from flask import request
from flask import make_response
import requests
import re


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


app = Flask(__name__)
IDkey = "jpfybhk69d"
SecretKey = "RuIMY0ILxMIf6ZZCyA9BIb2syBOXqnJrVEYzP5GX"


@app.route('/')
def main_Page():
    main_weather = weatherInfo()
    recentList = request.cookies.get('recentlist')
    if recentList is None:
        """
    [
        "창원시청":{
            "X":"123.123",
            "Y":"345.345",
            "isBook":"True"
        }, # 최근기록 리스트
        
        "창원대학교":{
            "X":"342.423",
            "Y":"123.523"
        } # 북마크 리스트
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
                "창원시청":{
                    "X":"123.123",
                    "Y":"345.345"
                }
            },
            "dest": {
                "창원대학교":{
                    "X": "342.423",
                    "Y": "123.523"
                }
            }
        }
        """
        defaultRoute = {
            "depart": {

            },
            "dest": {

            }
        }
        defaultJson = json.dumps(defaultCookie, ensure_ascii=False)
        startend = json.dumps(defaultRoute, ensure_ascii=False)
        resp = make_response(render_template("index.html", weather=main_weather["weather"]))
        resp.set_cookie('recentlist', defaultJson)
        resp.set_cookie('booklist', defaultJson)
        resp.set_cookie('routeinfo',startend)
        return resp
    else:
        print(recentList)
        print(request.cookies.get('routeinfo'))
        return render_template("index.html", weather=main_weather["weather"])


@app.route('/main', methods=['POST', 'GET'])
def result_Page():
    if request.method == 'POST':
        main_weather = weatherInfo()
        return render_template("index.html", weather=main_weather["weather"])
    else:
        main_weather = weatherInfo()
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
    # print(weather)
    return render_template("weather.html", weather=weather["weather"], temp=weather["temp"])


@app.route('/searchRecent', methods=['POST'])
def recent_search():
    sel = request.form['sel']
    print(sel)
    recentList = eval(request.cookies.get('recentlist'))
    if sel in 'depart':  # 출발지
        return render_template("search_recent.html", recentDepList=recentList["depart"], sel=sel)

    if sel in 'dest':  # 목적지
        return render_template("search_recent.html", recentDesList=recentList["dest"], sel=sel)


@app.route('/searchBookmark', methods=['POST'])
def recent_bookmark():
    sel = request.form['sel']
    print(sel)
    bookList = eval(request.cookies.get('booklist'))
    if sel in 'depart':  # 출발지
        return render_template("search_bookmark.html", recentDepList=bookList["depart"], sel=sel)

    if sel in 'dest':  # 목적지
        return render_template("search_bookmark.html", recentDesList=bookList["dest"], sel=sel)


@app.route('/nubijaSelect')#, methods=['POST'])
def nubijaTerminalSelect():
    name = "창원시청"  # request.form['name']
    x = 128.6818020  # request.form['x']
    y = 35.2279269  # request.form['y']
    distList = dict()
    req = requests.get('https://www.nubija.com/terminal/terminalState.do')
    html = req.text
    terminalInfo = []
    soup = BeautifulSoup(html, 'html.parser')
    stic = soup.find_all("a", {"href": re.compile("javascript:showMapInfoWindow.")})

    for k in stic:
        k = k.get("href").replace("javascript:showMapInfoWindow(", "").replace(");", "").replace("\'", "").split(", ")
        terminalInfo.append([k[1], k[2]])

    with open('static/terminalinfo.json') as json_nubiloc:
        json_locdata = json.load(json_nubiloc)

        for i in json_locdata:
            dist = math.pow((y - json_locdata[i][0]), 2) + math.pow((x - json_locdata[i][1]), 2)
            distList[i] = math.sqrt(dist)

        rankTemp = sorted(distList.items(), key=lambda t: t[1])
        print(rankTemp)

        with open('static/terminalName.json') as json_nubiname:
            json_nubidata = json.load(json_nubiname)

            for j in range(0, 3):
                print(json_nubidata[rankTemp[int(j)][0]])
                print(json_locdata[rankTemp[int(j)][0]])
                print(terminalInfo[j])

    return render_template('Nubija_terminal_select.html')


@app.route('/searchText', methods=['POST'])
def search_text():
    sel = request.form['sel']
    name = request.form['seartext']
    x = str(128.6818020)  # request.form['x']
    y = str(35.2279269)  # request.form['y']
    params = {'query': name, "coordinate": x + "," + y}
    headers = {"X-NCP-APIGW-API-KEY-ID": IDkey, "X-NCP-APIGW-API-KEY": SecretKey}
    base_search_addr = "https://naveropenapi.apigw.ntruss.com/map-place/v1/search"
    res = requests.get(base_search_addr, params=params, headers=headers)
    code = res.status_code

    if code == 200:
        result = res.json()["places"]
        print(result)
        if sel in 'depart':  # 출발지
            return render_template("search_text.html", result=result, sel=sel)

        if sel in 'dest':  # 목적지
            return render_template("search_text.html", result=result, sel=sel)

    else:
        print(code)


@app.route('/naviNubija', methods=['POST'])
def navi_nibija():
    x1 = str(127.1)
    y1 = str(37.3)
    x2 = str(127.1054328)  # request.form['x']
    y2 = str(37.3595963)  # request.form['y']
    params = {'start': x1 + "," + y1, "goal": x2 + "," + y2}
    headers = {"X-NCP-APIGW-API-KEY-ID": IDkey, "X-NCP-APIGW-API-KEY": SecretKey}
    base_search_addr = "https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving"
    res = requests.get(base_search_addr, params=params, headers=headers)
    code = res.status_code
    if code == 200:
        tem = []
        js = res.json()["route"]["traoptimal"][0]["guide"]
        for i in js:
            tem.append(i["instructions"])
        # print(tem)
        return render_template("navigation_nubija.html", tem=tem)
    else:
        print(code)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
