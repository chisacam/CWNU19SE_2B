# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import re
import requests
import urllib.request
import json

req = requests.get('https://www.nubija.com/terminal/terminalState.do')
html = req.text
terminalInfo = []
terminalLocation = {}
terminalNameInfo = []
terminalNameDic = {}
soup = BeautifulSoup(html, 'html.parser')
stic = soup.find_all("a", {"href":re.compile("javascript:showMapInfoWindow.")})
for i in stic:
    i = i.get("href").replace("javascript:showMapInfoWindow(", "").replace(");", "").replace("\'", "").split(", ")
    tempList = [int(i[3]), [float(i[4][0:9]), float(i[5][0:10])]]
    terminalInfo.append(tempList)
    tempList = [i[0], int(i[3])]
    terminalNameInfo.append(tempList)
for i in terminalNameInfo:
    terminalNameDic[i[0]] = i[1]
for i in terminalInfo:
    terminalLocation[i[0]] = i[1]
jsndmp = json.dumps(terminalLocation)
jsndmp1 = json.dumps(terminalNameDic, ensure_ascii = False)
with open("terminalInfo.json", 'w',encoding='UTF8') as fa:
    fa.write(jsndmp)
with open("terminalName.json", 'w',encoding='UTF8') as fa:
    fa.write(jsndmp1)
