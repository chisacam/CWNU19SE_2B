# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import re
import requests
import urllib.request
import json

req = requests.get('https://www.nubija.com/terminal/terminalState.do')
html = req.text
terminalInfo = []
soup = BeautifulSoup(html, 'html.parser')
stic = soup.find_all("a", {"href":re.compile("javascript:showMapInfoWindow.")})
for i in stic:
    i = i.get("href").replace("javascript:showMapInfoWindow(", "").replace(");", "").replace("\'", "").split(", ")
    terminalInfo.append([i[1],i[2]])
print(terminalInfo)