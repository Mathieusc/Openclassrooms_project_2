import requests
import re
import csv
import os
from bs4 import BeautifulSoup


def create_book_dict_categories_urls():
    """This function will return a dictionary with all books categories
    associated with their urls."""

    books_dict = {}
    url = "http://books.toscrape.com/index.html"
    response = requests.get(url, timeout=5)
    response.encoding = "UTF-8"

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        categories = soup.find("ul", {"class": "nav nav-list"}).findAll("a")
        for names in categories:
            category_name = names.text.strip()
            if category_name != "Books":
                books_dict[category_name] = (
                    "https://books.toscrape.com/" + names.attrs["href"]
                )

        return books_dict


def get_number_of_pages(category_index_url):
    """This function will return a list of all the pages urls from the
    category."""

    response = requests.get(category_index_url, timeout=2)
    response.encoding = "UTF-8"

    category_book_list = []
    category_urls = []
    # Getting all the pages from the category
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        category_name = soup.find("li", {"class": "active"})
        category_book_list.append(category_name.text.replace(" ", "_").lower())
        pages_number = soup.find("li", {"class": "current"})

        if pages_number:
            number_of_page = (
                str(pages_number.text.strip().replace("Page 1 of ", "")),
                category_index_url,
            )
            category_urls.append(category_index_url)
            counter = 1
            while counter < int(number_of_page[0]):
                counter += 1
                new_url = category_index_url.replace(
                    "index.html", "page-" + str(counter) + ".html"
                )
                category_urls.append(new_url)
        else:
            category_urls.append(category_index_url)

    return category_urls


def get_books_urls(category_urls):
    """This function will return a list of all the books urls from the
    category."""

    books_urls = []
    for lines in category_urls:
        lines.strip()
        response = requests.get(lines, timeout=2)
        response.encoding = "UTF-8"

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
            articles = soup.findAll("article", {"class": "product_pod"})
            for article in articles:
                a = article.find("a")
                link = a["href"]
                books_urls.append(
                    "http://books.toscrape.com/catalogue/"
                    + link.replace("../../../", "")
                )

    return books_urls


def get_books_data(books_urls):
    # This function will gather all the data from the books urls."""

    for books in books_urls:
        book_data = {
            "product_page_url": None,
            "universal_product_code": None,
            "title": None,
            "price_including_tax": None,
            "price_excluding_tax": None,
            "number_available": None,
            "product_description": None,
            "category": None,
            "review_rating": None,
            "image_url": None,
        }
        books.strip()
        book_data["product_page_url"] = books
        response = requests.get(books, timeout=2)
        response.encoding = "UTF-8"
        soup = BeautifulSoup(response.text, "lxml")
        book_upc = (
            soup.find("table", {"class": "table table-striped"})
            .find("th", text="UPC")
            .find_next_sibling()
        )
        book_data["universal_product_code"] = book_upc.text

        book_title = soup.find("h1")
        book_data["title"] = book_title.text

        book_price_including_tax = (
            soup.find("table", {"class": "table table-striped"})
            .find("th", text="Price (incl. tax)")
            .find_next_sibling()
        )
        book_data["price_including_tax"] = book_price_including_tax.text

        book_price_excluding_tax = (
            soup.find("table", {"class": "table table-striped"})
            .find("th", text="Price (excl. tax)")
            .find_next_sibling()
        )
        book_data["price_excluding_tax"] = book_price_excluding_tax.text

        book_availability = soup.find("p", {"class": "instock availability"})
        book_data["number_available"] = book_availability.text.strip()

        book_description = soup.find("h2").find_next()
        book_data["product_description"] = book_description.text

        book_category = soup.find(
            "li", {"class": "active"}).find_previous_sibling()
        book_data["category"] = book_category.text.strip()

        book_rating = soup.find(class_=re.compile("^star-"))
        if book_rating.attrs["class"][1] == "One":
            book_rating_converted = "1"
            book_data["review_rating"] = book_rating_converted
        elif book_rating.attrs["class"][1] == "Two":
            book_rating_converted = "2"
            book_data["review_rating"] = book_rating_converted
        elif book_rating.attrs["class"][1] == "Three":
            book_rating_converted = "3"
            book_data["review_rating"] = book_rating_converted
        elif book_rating.attrs["class"][1] == "Four":
            book_rating_converted = "4"
            book_data["review_rating"] = book_rating_converted
        elif book_rating.attrs["class"][1] == "Five":
            book_rating_converted = "5"
            book_data["review_rating"] = book_rating_converted

        book_picture = soup.find("img")
        book_data["image_url"] = "http://books.toscrape.com/"\
        + book_picture.attrs["src"].replace("../", "")

        yield book_data


def write_books_for_category_to_csv(category_name, book_list):
    """Create a directory for all categories and write all the data
    from the books into a csv file into this directory."""

    csv_colums = [
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
    # Create variables for directories, create the directory from the
    # book's category and the directory for the images.
    path = category_name
    img_path = "images"
    books_path = "books_categories"
    if not os.path.isdir(books_path):
        os.mkdir(books_path)
    try:
        os.makedirs(os.path.join(books_path, category_name, img_path))
    except FileExistsError:
        pass
    finally:
        print("Creating category directory...")
    # Create the csv into the directory from the book's category.
    with open(
        books_path
        + "/"
        + path
        + "/"
        + f"{category_name}.csv",
        "w", encoding="UTF-8"
    ) as inputfile:
        writer = csv.DictWriter(
            inputfile,
            fieldnames=csv_colums,
            quoting=csv.QUOTE_ALL,
            delimiter=","
        )
        writer.writeheader()
        writer.writerows(book_list)


def download_book_image(category_name, book_list):
    """Download all images from the category parameter and the list of
    images inside its directory as '.jpg'."""

    # Using x and y to loop through the list of dictionary.
    # x and y correspond to the first category from all categories. (50 totals)
    x = 0
    y = 0
    img_path = "images"
    books_path = "books_categories"
    try:
        for books in book_list:
            file_name = (
                book_list[x]["title"]
                .replace(":", "-")
                .replace('"', "-")
                .replace("/", "-")
                .replace("'", "-")
                .replace("*", "-")
                .replace("?", "-")
            )
            book_picture = book_list[y]["image_url"]
            response = requests.get(book_picture, stream=True)
            if response.status_code == 200:
                with open(
                    books_path
                    + "/"
                    + category_name
                    + "/"
                    + img_path
                    + "/"
                    + file_name
                    + ".jpg",
                    "wb",
                ) as file:
                    for chunk in response:
                        file.write(chunk)
                    x += 1
                    y += 1
    except FileNotFoundError as f:
        print(f)
        print("Could no gather all the images from the category.")
        pass
