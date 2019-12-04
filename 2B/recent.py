from flask import make_response
from flask import render_template
import json


class Recent:
    def loadRecentPlaceList(self, targetsel, hiddenlat, hiddenlong, recentlist, booklist, isservicetime):
        sel = targetsel
        hiddenLat = hiddenlat
        hiddenLong = hiddenlong
        recentList = recentlist
        bookList = booklist
        recentDepartLen = len(recentList["depart"])
        recentDestLen = len(recentList["dest"])
        bookDepartLen = len(bookList["depart"])
        bookDestLen = len(bookList["dest"])
        if bookDepartLen != 0:
            for checkRecent in range(0, recentDepartLen):
                for key, value in recentList["depart"][checkRecent].items():
                    for checkBook in range(0, bookDepartLen):
                        if key in bookList["depart"][checkBook]:
                            recentList["depart"][checkRecent][key]["isBook"] = "Yes"
                            break
                        else:
                            recentList["depart"][checkRecent][key]["isBook"] = "Nope"
        else:
            for checkRecent in range(0, recentDepartLen):
                for key, value in recentList["depart"][checkRecent].items():
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
        else:
            for checkRecent in range(0, recentDestLen):
                for key, value in recentList["dest"][checkRecent].items():
                    recentList["dest"][checkRecent][key]["isBook"] = "Nope"

        if sel in 'depart':  # 출발지
            setCookie = json.dumps(recentList, ensure_ascii=False)
            resp = make_response(render_template("search_recent.html", resultList=recentList["depart"], sel=sel,
                                                 isServiceTime=isservicetime, hiddenLong=hiddenLong, hiddenLat=hiddenLat))
            resp.set_cookie('recentlist', setCookie)
            return resp

        if sel in 'dest':  # 목적지
            setCookie = json.dumps(recentList, ensure_ascii=False)
            resp = make_response(render_template("search_recent.html", resultList=recentList["dest"], sel=sel,
                                                 isServiceTime=isservicetime, hiddenLong=hiddenLong, hiddenLat=hiddenLat))
            resp.set_cookie('recentlist', setCookie)
            return resp
