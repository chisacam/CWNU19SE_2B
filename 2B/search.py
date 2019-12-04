from flask import make_response
from flask import render_template
import json
import requests


class Search:
    def __init__(self):
        self.IDkey = "jpfybhk69d"
        self.SecretKey = "RuIMY0ILxMIf6ZZCyA9BIb2syBOXqnJrVEYzP5GX"
        self.defaultRoute = {
            "depart": {

            },
            "dest": {

            }
        }

    def search_text(self, targetsel, targetname, targetx, targety):
        sel = targetsel
        name = targetname
        x = targetx
        y = targety
        params = {'query': name, "coordinate": x + "," + y}
        headers = {"X-NCP-APIGW-API-KEY-ID": self.IDkey, "X-NCP-APIGW-API-KEY": self.SecretKey}
        base_search_addr = "https://naveropenapi.apigw.ntruss.com/map-place/v1/search"
        res = requests.get(base_search_addr, params=params, headers=headers)
        code = res.status_code

        if code == 200:
            test = res.json()
            textResult = res.json()["places"]
            if sel in 'depart':  # 출발지
                return render_template("search_text.html", result=textResult, sel=sel, name=name, hiddenLong=x, hiddenLat=y)

            if sel in 'dest':  # 목적지
                return render_template("search_text.html", result=textResult, sel=sel, name=name, hiddenLong=x, hiddenLat=y)

        else:
            print(code)

    def navi_nubija(self, routeinfo, recent):
        route = routeinfo
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
        headers = {"X-NCP-APIGW-API-KEY-ID": self.IDkey, "X-NCP-APIGW-API-KEY": self.SecretKey}
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

                recentList = recent
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
                temp2 = json.dumps(self.defaultRoute, ensure_ascii=False)
                resp = make_response(render_template("navigation_nubija.html", tem=tem, icons=icons,
                                                     start=name1, end=name2, isError=False))
                resp.set_cookie("routeinfo", temp2)
                resp.set_cookie("recentlist", temp)
                return resp
            else:
                temp2 = json.dumps(self.defaultRoute, ensure_ascii=False)
                resp = make_response(render_template("navigation_nubija.html", tem=[["네이버API에러"], ["길찾기실패"]],
                                                     icons=[iconaddr + "else.svg"], start=name1, end=name2,
                                                     isError=True, errorInfo=js['message']))
                resp.set_cookie("routeinfo", temp2)
                return resp
        else:
            print(code)
