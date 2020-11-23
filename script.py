import requests
import re
import csv
import time
from bs4 import BeautifulSoup


def get_all_books_urls():
    """This function will return a list containing all the urls of each books
    from every pages of books.toscrape.com"""

    # Looping through the 50 pages of the website
    for i in range(51):
        """
        pages_number = soup.find('li', {'class': 'current'}).text.strip()\
        .replace('Page 1 of ', '')
        pages_number = int(pages_number)
        print(pages_number)"""

        url = "http://books.toscrape.com/catalogue/page-" + str(i) + ".html"
        response = requests.get(url, timeout=5)
        response.encoding = "UTF-8"

        if response.status_code == 200:
            # precise lxml to avoid the 'GuessedAtParserWarning' message

            soup = BeautifulSoup(response.text, "lxml")
            articles = soup.findAll("article")

            for article in articles:
                a = article.find("a")
                # use brackets to select attributs from an href tag
                link = a["href"]

                yield "http://books.toscrape.com/catalogue/" + link

a = time.time()
books_urls = get_all_books_urls()
b = time.time()

print("{} secondes.".format(b-a))
# for urls in books_urls:
#     print(urls)


def get_books_data():
    """This function will scrape every data that we need to write into a file
    from every books from the website."""

    for lines in books_urls:
        url = lines.strip()
        yield url

        response = requests.get(url, timeout=5)
        response.encoding = "UTF-8"

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")

            book_upc = (
                soup.find("table", {"class": "table table-striped"})
                .find("th", text="UPC")
                .find_next_sibling()
            )
            yield book_upc.text

            book_title = soup.find("h1")
            yield book_title.text

            book_price_including_tax = (
                soup.find("table", {"class": "table table-striped"})
                .find("th", text="Price (incl. tax)")
                .find_next_sibling()
            )
            yield book_price_including_tax.text

            book_price_excluding_tax = (
                soup.find("table", {"class": "table table-striped"})
                .find("th", text="Price (excl. tax)")
                .find_next_sibling()
            )
            yield book_price_excluding_tax.text

            book_availability = soup.find("p", {"class": "instock availability"})
            yield book_availability.text.strip()

            book_description = soup.find("h2").find_next()
            yield book_description.text

            book_category = soup.find("li", {"class": "active"}).find_previous_sibling()
            yield book_category.text.strip()

            book_rating = soup.find(class_=re.compile("^star-"))
            if book_rating.attrs["class"][1] == "One":
                book_rating_converted = "1"
                yield book_rating_converted
            elif book_rating.attrs["class"][1] == "Two":
                book_rating_converted = "2"
                yield book_rating_converted
            elif book_rating.attrs["class"][1] == "Three":
                book_rating_converted = "3"
                yield book_rating_converted
            elif book_rating.attrs["class"][1] == "Four":
                book_rating_converted = "4"
                yield book_rating_converted
            elif book_rating.attrs["class"][1] == "Five":
                book_rating_converted = "5"
                yield book_rating_converted

            book_picture = soup.find("img")
            yield "http://books.toscrape.com/" + book_picture.attrs["src"].replace(
                "../", ""
            )
            book_picture_url = "http://books.toscrape.com/" + book_picture.attrs[
                "src"
            ].replace("../", "")


books_data = get_books_data()
for datas in books_data:
  print(datas)


def write_urls_into_file():
    with open("books_urls.txt", "w", encoding="UTF-8") as file:
        for link in books_urls:
            file.write(link + "\n")


def csv_writer():
    for lines in books_data:
        with open("books.csv", "w", encoding="UTF-8") as out_file:

            fieldnames = [
                "product_page_url",
                "universal_product_code",
                "title",
                "price_including_tax",
                "price_excluding_tax",
                "number_available",
                "product_description",
                "category",
                "review_rating",
                "image_url",
            ]

            csv_writer = csv.DictWriter(
                out_file, fieldnames=fieldnames, quoting=csv.QUOTE_ALL
            )
            csv_writer.writeheader()

            rows = [
                {
                    "product_page_url": url,
                    "universal_product_code": book_upc.text,
                    "title": book_title.text,
                    "price_including_tax": book_price_including_tax.text,
                    "price_excluding_tax": book_price_excluding_tax.text,
                    "number_available": book_availability.text.strip(),
                    "product_description": book_description.text,
                    "category": book_category.text.strip(),
                    "review_rating": book_rating_converted,
                    "image_url": book_picture_url,
                }
            ]

            csv_writer.writerows(rows)


"""
Note to myself:
It might be useful to add a pause with time.sleep(seconds) with the os
module to avoid being blocked while scraping through all the pages from a
website, or use a proxy, or with requests.timeout parameter.
It does not seem to be an issue with this website tho.
"""

# -----------------------------------------------------------------------------
# Save all the urls inside a txt file for now.
# I will create a CSV file later


# Create the file (writes what is in the list [links] inside a txt file)
"""
with open('urls.txt', 'w', encoding='UTF-8') as file:
    for link in books_urls:
        file.write(link + '\n')
"""

"""
Read the file
with open('urls.txt', 'r') as file:
    for row in file:
        print(row)
"""
