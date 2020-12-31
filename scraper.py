"""
    Documentation du module
"""

import requests
import re
import csv
from bs4 import BeautifulSoup
from scraper_functions import (
    get_category_index_url,
    get_number_of_pages, 
    get_books_urls,
    get_books_data,
    write_books_for_category_to_csv)


def get_books_for_category(category_url):
    # for books in category_url:
    book_list = []
    for book in get_book(category_url):
        book_list.append(book)
    print(book_list)

    # Récupérer les données de tous les livres sur toutes les pages de la catégorie

    pass

def main():
    # Using only one category for now as a test, the program needs to loop
    # through all of them in the end.
    add_a_comment = "https://books.toscrape.com/catalogue/category/books/add-a-comment_18/index.html"
    all_categories = get_category_index_url()
    print("All categories: \n", all_categories)
    # 1 - getting all the pages from one category if they exists.
    nb_of_pages = get_number_of_pages(all_categories[6])
    print("Pages urls:\n", nb_of_pages, "\n")

    # 2 - getting all the urls from all the books from all the pages of one
    # category.
    books_urls = get_books_urls(nb_of_pages)
    print("Books urls:\n", [books_urls], "\n")

    books_data = [book for book in get_books_data(books_urls)]
    print("Books data:\n", [book for book in books_data])

    # Write all the data inside a csv file.
    book_csv = write_books_for_category_to_csv("add_a_comment", books_data)

if __name__ == '__main__':
    main()