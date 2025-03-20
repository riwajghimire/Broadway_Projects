import requests
from bs4 import BeautifulSoup
import json

URL = "https://books.toscrape.com/"


def scrape_books(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed To Fetch Data...")
        return
    response.encoding = response.apparent_encoding # used to remove special characters of euros
    soup = BeautifulSoup(response.text,"html.parser")
    books = soup.find_all("article", class_="product_pod")
    print(books)
    scraped_books = []
    for book in books:
        title = book.h3.a['title'] # title in [] beacuse its not a tag but an attribute
        price_text = book.find("p", class_="price_color").text
        currency = price_text[0]
        price = price_text[1:]
        dict = {
            "title":title,
            "currency":currency,
            "price":price

        }
        scraped_books.append(dict)
    with open("data.json", "w",encoding='utf-8') as f:
            json.dump(scraped_books,f,indent=4,ensure_ascii=False)


scrape_books(URL)
