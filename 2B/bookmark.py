from flask import make_response
from flask import render_template
import json


class BookMark:
    def loadBookmarkPlaceList(self, targetsel, hiddenlat, hiddenlong, booklist):
        sel = targetsel
        hiddenLat = hiddenlat
        hiddenLong = hiddenlong
        bookList = booklist
        if sel in 'depart':  # 출발지
            return render_template("search_bookmark.html", resultList=bookList["depart"], sel=sel,
                                   hiddenLong=hiddenLong, hiddenLat=hiddenLat)

        if sel in 'dest':  # 목적지
            return render_template("search_bookmark.html", resultList=bookList["dest"], sel=sel,
                                   hiddenLong=hiddenLong, hiddenuserLat=hiddenLat)

    def manageBookmark(self, targetsel, targetname, targetx, targety, hiddenlat, hiddenlong, booklist):
        sel = targetsel
        name = targetname
        y = targetx
        x = targety
        hiddenLong = hiddenlong
        hiddenLat = hiddenlat
        resp = make_response()
        isInDepart = False
        isInDest = False
        bookmarkCheck = booklist
        departLen = len(bookmarkCheck["depart"])
        destLen = len(bookmarkCheck["dest"])
        if sel in 'depart':
            if departLen == 0:
                bookmarkCheck["depart"].append({
                    name: {
                        "x": x,
                        "y": y
                    }
                })
            else:
                check = 0
                while True:
                    if name in bookmarkCheck["depart"][check]:
                        del bookmarkCheck["depart"][check]
                        isInDepart = True
                    if check < len(bookmarkCheck["depart"]) - 1:
                        check += 1
                        continue
                    break

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
                check = 0
                while True:
                    if name in bookmarkCheck["dest"][check]:
                        del bookmarkCheck["dest"][check]
                        isInDest = True
                    if check < len(bookmarkCheck["dest"]) - 1:
                        check += 1
                        continue
                    break

                if isInDest is False:
                    bookmarkCheck["dest"].append({
                        name: {
                            "x": x,
                            "y": y
                        }
                    })
            resp = make_response(render_template('search_bookmark.html', resultList=bookmarkCheck["dest"], sel=sel,
                                                 hiddenLong=hiddenLong, hiddenLat=hiddenLat))
        resultBook = json.dumps(bookmarkCheck, ensure_ascii=False)
        resp.set_cookie('booklist', resultBook)
        return resp
