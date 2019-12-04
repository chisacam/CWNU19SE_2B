# 시스템 요구 라이브러리 import
from flask import Flask, redirect, url_for
from flask import render_template
from flask import jsonify
import json
from flask import request
from flask import make_response
import datetime
from OpenSSL import SSL

# 분리한 클래스들 import
import bookmark
import recent
import nubija
import weather
import search

# 클래스 객체 선
weatherClass = weather.Weather()
nubijaClass = nubija.Nubija()
bookmarkClass = bookmark.BookMark()
searchClass = search.Search()
recentClass = recent.Recent()


# 현재 시간 정수형태로 반환
def timeCheck():
    KST = datetime.timezone(datetime.timedelta(hours=9))
    now = datetime.datetime.now(KST)
    nowTime = now.strftime('%H')
    return int(nowTime)

# 현재 시간이 0100~0359 사이일경우 False, 아니면 True 반환
def checkServiceTime():
    if timeCheck() in [1, 2, 3]:
        return False
    else:
        return True


app = Flask(__name__)

# 서비스 처음 사용시 기본값으로 생성할 최근기록, 북마크 쿠키
defaultCookie = {
    "depart": [

    ],
    "dest": [

    ]
}
# 서비스 처음 사용시, 그리고 경로안내후 초기화시 사용할 출발, 목적지 쿠키
defaultRoute = {
    "depart": {

    },
    "dest": {

    }
}


# 메인페이지 접속시 현재 날씨상태를 아이콘으로 받아와 함께 렌더링
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


# 출발지 또는 도착지 지정 후 돌아오는 페이지. 지정된곳에 따라 구분해서 쿠키에 추가후 메인페이지와 동일하게 날씨 정보도 함께 렌더링
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


# 메인페이지에 누비자 터미널 위치 마커 표시를 위한 json 로드용 주소
@app.route('/js')
def jse():
    geoInfo = open('static/terminalInfo.json', 'r', encoding='UTF8')
    nameInfo = open('static/terminalName.json', 'r', encoding='UTF8')
    nameInfo = json.loads(nameInfo.read())
    nameInfo = json.dumps(nameInfo, ensure_ascii=False)
    geoInfo = json.loads(geoInfo.read())
    geoInfo = json.dumps(geoInfo, ensure_ascii=False)
    return jsonify(namedata=nameInfo, geodata=geoInfo)


# 날씨 정보(아이콘, 온도) 확인을 위한 페이지. 해당 정보를 받은 다음 함께 반환.
@app.route('/weather')
def Weather_page():
    main_weather = weatherClass.weatherInfo()
    return render_template("weather.html", weather=main_weather["weather"], temp=main_weather["temp"])


# 최근기록을 불러오는 페이지. 단, 최근 기록을 보내기전 북마크 포함여부도 함께 체크
@app.route('/searchRecent', methods=['POST'])
def recent_search():
    sel = request.form['sel']
    hiddenLat = request.form['hiddenLat']
    hiddenLong = request.form['hiddenLong']
    recentList = eval(request.cookies.get('recentlist'))
    bookList = eval(request.cookies.get('booklist'))
    return recentClass.loadRecentPlaceList(sel, hiddenLat, hiddenLong, recentList, bookList, checkServiceTime())


# 단순히 북마크 리스트를 반환하는 페이지
@app.route('/searchBookmark', methods=['POST'])
def recent_bookmark():
    sel = request.form['sel']
    hiddenLat = request.form['hiddenLat']
    hiddenLong = request.form['hiddenLong']
    bookList = eval(request.cookies.get('booklist'))
    return bookmarkClass.loadBookmarkPlaceList(sel, hiddenLat, hiddenLong, bookList)


# 최근기록이나 북마크 리스트중에서 북마크를 추가, 제거할때 호출되는 페이지. 해당하는 목록을 추가, 제거하는 기능 수행 후 최종 리스트를 반환
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


# 텍스트 검색이나 위치기반 검색후 근처 누비자 터미널 3개를 짧은 거리순으로 반환
@app.route('/nubijaSelect', methods=['POST'])
def nubijaSelect():
    sel = request.form['sel']
    x = float(request.form['selX'])
    y = float(request.form['selY'])
    hiddenLat = request.form['hiddenLat']
    hiddenLong = request.form['hiddenLong']
    return nubijaClass.nubijaTerminalSelect(sel, x, y, hiddenLat, hiddenLong, checkServiceTime())


# 유저의 위치, 또는 창원시청 위치를 기반으로 유저 검색어에 해당하는 장소 이름과 위치 리스트를 반환
@app.route('/searchText', methods=['POST'])
def searchtext():
    sel = request.form['sel']
    name = request.form['seartext']
    x = request.form['hiddenLong']
    y = request.form['hiddenLat']
    return searchClass.search_text(sel, name, x, y)


# 쿠키에 출발지, 목적지가 모두 기록되면 자동으로 라우팅 되어 실행되는 페이지. 지정된 장소간 이동 경로 안내와 안내에 해당하는 아이콘 위치 리스트를 반환.
@app.route('/naviNubija', methods=['GET'])
def navinubija():
    route = eval(request.cookies.get('routeinfo'))
    recent = eval(request.cookies.get('recentlist'))
    return searchClass.navi_nubija(route, recent)


# 출발지나 목적지중 하나(둘다 선택시는 자동으로 navi로 넘어감)만 선택 후, 반대쪽 위치로 변경하고 싶을때 사용하는 페이지.
# 호출시 경로 쿠키에서 비어있는 부분에 이미 기록된 부분을 이동시킴.
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


# https 연결을 위한 부분
contextSSL = ('server.crt', 'server.key')


# flask 웹서버 실행, 그리고 외부접근 가능 옵션과 디버깅 기능 추가.
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, ssl_context=contextSSL)
