import os
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

mongodb_uri = os.getenv("MONGODB_URI")
cluster = MongoClient(mongodb_uri)
db = cluster["testdb"]
collection = db["advertisements"]

url = "https://krisha.kz/arenda/kvartiry/almaty/?das[flat.floor][to]=500000"
req = requests.get(url)
src = req.text

#Если нужно сохранить страницу

#Сохраняет html
# with open("index.html", "w", encoding="utf-8") as file:
#     file.write(src)

#Считывает html
# with open("index.html", encoding="utf-8") as file:
#     src = file.read()

soup = BeautifulSoup(src, "lxml")

img_tags = soup.find_all("img", class_="a-image__img")
img_src_list = [img_tag.get('src') for img_tag in img_tags]

card_titles = [elem.text.strip() for elem in soup.find_all("div", class_="a-card__header-left")]
disc_a_list = [elem.text.strip() for elem in soup.find_all("div", class_="a-card__wrapper-subtitle")]
disc_b_list = [elem.text.strip() for elem in soup.find_all("div", class_="a-card__text-preview")]
price_tags = [elem.text.strip() for elem in soup.find_all("div", class_="a-card__price")]

min_length = min(len(img_src_list), len(card_titles), len(disc_a_list), len(disc_b_list), len(price_tags))

data_list = []
for i in range(min_length):
    data = {
        "img_src": img_src_list[i],
        "card_title": card_titles[i],
        "disc_a": disc_a_list[i],
        "disc_b": disc_b_list[i],
        "price": price_tags[i]
    }
    data_list.append(data)

collection.insert_many(data_list)

cluster.close()