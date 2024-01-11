import os
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Connect to MongoDB using the provided URI
mongodb_uri = os.getenv("MONGODB_URI")
cluster = MongoClient(mongodb_uri)
db = cluster["testdb"]
collection = db["advertisements"]

# URL of the website to scrape
url = "https://krisha.kz/arenda/kvartiry/almaty/?das[flat.floor][to]=500000"

# Make a request to the website and get the HTML content
req = requests.get(url)
src = req.text

# Uncomment the following block if you want to save the HTML content to a file
# with open("index.html", "w", encoding="utf-8") as file:
#     file.write(src)

# Uncomment the following block if you want to read the HTML content from a file
# with open("index.html", encoding="utf-8") as file:
#     src = file.read()

# Create a BeautifulSoup object for parsing HTML
soup = BeautifulSoup(src, "lxml")

# Extract image sources, card titles, subtitles, text previews, and prices
img_tags = soup.find_all("img", class_="a-image__img")
img_src_list = [img_tag.get('src') for img_tag in img_tags]

card_titles = [elem.text.strip() for elem in soup.find_all("div", class_="a-card__header-left")]
disc_a_list = [elem.text.strip() for elem in soup.find_all("div", class_="a-card__wrapper-subtitle")]
disc_b_list = [elem.text.strip() for elem in soup.find_all("div", class_="a-card__text-preview")]
price_tags = [elem.text.strip() for elem in soup.find_all("div", class_="a-card__price")]

# Determine the minimum length to avoid index out of range errors
min_length = min(len(img_src_list), len(card_titles), len(disc_a_list), len(disc_b_list), len(price_tags))

# Create a list of dictionaries containing the scraped data
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

# Insert the scraped data into the MongoDB collection
collection.insert_many(data_list)

# Close the MongoDB connection
cluster.close()