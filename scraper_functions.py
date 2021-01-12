import requests
import re
import csv
import time
from bs4 import BeautifulSoup

def get_category_index_url(urls="https://books.toscrape.com/index.html"):
    """ This function will return a list containing all the urls of each
    book's categories from every pages of books.toscrape.com"""

    response = requests.get(urls)
    response.encoding = 'UTF-8'
    books_genres = []

    if response.status_code == 200:
        # precise lxml to avoid the 'GuessedAtParserWarning' message
        soup = BeautifulSoup(response.text, 'lxml')
        category = soup.find('ul', {'class': 'nav nav-list'}).findAll('a')
        for hrefs in category:
            books_genres.append('https://books.toscrape.com/'
            + hrefs.attrs['href'])      
        books_genres.pop(0)
        books_genres.sort()

        return books_genres

def get_number_of_pages(category_index_url):
    """This function will return a list of all the pages urls from the
    category."""

    response = requests.get(category_index_url, timeout=2)
    response.encoding = 'UTF-8'

    category_book_list = []
    category_urls = []
    book_data = {"product_page_url": None,
                "universal_product_code": None,
                "title": None,
                "price_including_tax": None,
                "price_excluding_tax": None,
                "number_available": None,
                "product_description": None,
                "category": None,
                "review_rating": None,
                "image_url": None}
    # Get all the pages from the category
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        category_name = soup.find('li', {'class': 'active'})
        category_book_list.append(
        category_name.text.replace(' ', '_').lower())
        pages_number = soup.find('li', {'class': 'current'})

        if pages_number:
            number_of_page = str(pages_number.text.strip().replace(
                            'Page 1 of ', '')), category_index_url
            category_urls.append(category_index_url)
            counter = 1
            while counter < int(number_of_page[0]):
                counter += 1
                new_url = category_index_url.replace('index.html',
                 'page-' +str(counter) + '.html')
                category_urls.append(new_url)
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
            articles = soup.findAll('article', {'class': 'product_pod'})
            for article in articles:
                a = article.find('a')
                link = a['href']
                books_urls.append('http://books.toscrape.com/catalogue/'
                + link.replace('../../../', ''))
                
    return books_urls

def get_books_data(books_urls):
    # This function will get every data from the books urls."""

    for books in books_urls:
        book_data = {"product_page_url": None,
            "universal_product_code": None,
            "title": None,
            "price_including_tax": None,
            "price_excluding_tax": None,
            "number_available": None,
            "product_description": None,
            "category": None,
            "review_rating": None,
            "image_url": None}
        books.strip()
        book_data['product_page_url'] = books
        response = requests.get(books, timeout=2)
        response.encoding = "UTF-8"
        soup = BeautifulSoup(response.text, "lxml")
        book_upc = soup.find('table',
            {'class': 'table table-striped'}).find(
                'th', text='UPC').find_next_sibling()
        book_data['universal_product_code'] = book_upc.text

        book_title = soup.find('h1')
        book_data['title'] = book_title.text

        book_price_including_tax = soup.find('table', 
            {'class': 'table table-striped'}).find(
                'th', text='Price (incl. tax)').find_next_sibling()
        book_data['price_including_tax'] = book_price_including_tax.text

        book_price_excluding_tax = soup.find('table', 
            {'class': 'table table-striped'}).find(
                'th', text='Price (excl. tax)').find_next_sibling()
        book_data['price_excluding_tax'] = book_price_excluding_tax.text

        book_availability = soup.find('p'
            , {'class': 'instock availability'})
        book_data['number_available'] = book_availability.text.strip()

        book_description = soup.find('h2').find_next()
        book_data['product_description'] = book_description.text

        book_category = soup.find(
            'li', {'class': 'active'}).find_previous_sibling()
        book_data['category'] = book_category.text.strip()

        book_rating = soup.find(class_=re.compile('^star-'))
        if book_rating.attrs['class'][1] == 'One':
            book_rating_converted = '1'
            book_data['review_rating'] = book_rating_converted
        elif book_rating.attrs['class'][1] == 'Two':
            book_rating_converted = '2'
            book_data['review_rating'] = book_rating_converted
        elif book_rating.attrs['class'][1] == 'Three':
            book_rating_converted = '3'
            book_data['review_rating'] = book_rating_converted
        elif book_rating.attrs['class'][1] == 'Four':
            book_rating_converted = '4'
            book_data['review_rating'] = book_rating_converted
        elif book_rating.attrs['class'][1] == 'Five':
            book_rating_converted = '5'
            book_data['review_rating'] = book_rating_converted

        book_picture = soup.find('img')
        book_data['image_url'] = 'http://books.toscrape.com/' \
            + book_picture.attrs['src'].replace('../', '')

        yield book_data


def write_books_for_category_to_csv(category_name, book_list):
    """Write all the data from the books into a csv file."""
    
    csv_colums = ["product_page_url",
                "universal_product_code",
                "title",
                "price_including_tax",
                "price_excluding_tax",
                "number_available",
                "product_description",
                "category",
                "review_rating",
                "image_url"]

    with open(f"{category_name}.csv", "w", encoding='UTF-8') as inputfile:
        writer = csv.DictWriter(inputfile, fieldnames=csv_colums,
        quoting=csv.QUOTE_ALL, delimiter=',' )
        writer.writeheader()
        for row in csv_colums:
            writer.writerows(book_list)