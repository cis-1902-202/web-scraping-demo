URL = "https://books.toscrape.com"


import requests
from bs4 import BeautifulSoup
import json


def get_html_document(url):
    html = requests.get(url)
    return html.text


def get_beautiful_soup_node(url):
    return BeautifulSoup(get_html_document(url), features="html.parser")


def get_information_from_book(book_url):
    book_node = get_beautiful_soup_node(book_url)

    def get_title():
        node = book_node.find("div", attrs={"class": "product_main"})
        node = node.find("h1")
        return node.text

    def get_description():
        node = book_node.find("div", attrs={"id": "product_description"})
        # print(node)
        node = node.next_sibling.next_sibling
        return node.text

    def get_price():
        node = book_node.find("p", attrs={"class": "price_color"})
        return node.text

    title = get_title()
    description = get_description()
    price = get_price()

    return {"title": title, "description": description, "price": price}


def get_book_url(book_node):
    a_tag = book_node.find("a")
    href = a_tag.get("href")
    return URL + "/" + href


def get_book_data(book_node):
    book_url = get_book_url(book_node)
    data = get_information_from_book(book_url)
    return data


def main():
    tree = get_beautiful_soup_node(URL)
    books = tree.find_all("article", attrs={"class": "product_pod"})
    res = [get_book_data(book) for book in books]
    with open("main.json", "w") as f:
        f.write(json.dumps(res, indent=4))


if __name__ == "__main__":
    main()
