from bs4 import BeautifulSoup
import requests
import re
import json
import math
from flask import render_template


class Nubija:
    def getTerminalInfo(self):
        req = requests.get('https://www.nubija.com/terminal/terminalState.do')
        html = req.text
        terminalInfo = []
        soup = BeautifulSoup(html, 'html.parser')
        stic = soup.find_all("a", {"href": re.compile("javascript:showMapInfoWindow.")})

        for k in stic:
            k = k.get("href").replace("javascript:showMapInfoWindow(", "").replace(");", "").replace("\'", "").split(", ")
            terminalInfo.append([k[1], k[2]])
        return terminalInfo

    def nubijaTerminalSelect(self, targetsel, targetx, targety, hiddenlat, hiddenlong, isservicetime):
        sel = targetsel
        x = targetx
        y = targety
        hiddenLat = hiddenlat
        hiddenLong = hiddenlong
        distList = dict()
        terminalInfo = self.getTerminalInfo()
        selectResult = []

        with open('static/terminalInfo.json', 'r', encoding='UTF8') as json_nubiloc:
            json_locdata = json.load(json_nubiloc)

            for i in json_locdata:
                dist = math.pow((y - json_locdata[i][0]), 2) + math.pow((x - json_locdata[i][1]), 2)
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

        return render_template('Nubija_terminal_select.html', selectResult=selectResult, sel=sel, hiddenLat=hiddenLat,
                               hiddenLong=hiddenLong, isServiceTime=isservicetime)
