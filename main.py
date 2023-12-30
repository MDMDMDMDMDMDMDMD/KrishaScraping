import requests
from bs4 import BeautifulSoup

url = "https://krisha.kz/arenda/kvartiry/?das[live.rooms]=3&das[price][to]=500000"

req = requests.get(url)
src = req.text
# print(src)

with open("index.html", "w", encoding="utf-8") as file:
    file.write(src)