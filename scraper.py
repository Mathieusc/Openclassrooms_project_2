"""
    Documentation du module
"""

import requests
import re
import csv
import os
import shutil
from bs4 import BeautifulSoup
import concurrent.futures
import urllib.request
from scraper_functions import (
    create_book_dict_categories_urls,
    get_number_of_pages, 
    get_books_urls,
    get_books_data,
    write_books_for_category_to_csv,
    download_book_image,)

def main():
    all_categories = create_book_dict_categories_urls()
    # Creating a dictionary with each categories associated with their urls.
    print(f"All categories: ({len(all_categories)} total)\n", all_categories)
    # Looping through each categories
    for category_name, index_url in all_categories.items():
        # 1 - getting all the pages from one category if they exists.
        nb_of_pages = get_number_of_pages(index_url)
        print("\nPages urls:\n", nb_of_pages, "\n")
        # 2 - getting all the urls from all the books from all the pages of one
        # category.
        books_urls = get_books_urls(nb_of_pages)
        print(f"Books urls: ({len(books_urls)} total)\n", [books_urls], "\n")
        # 4 - getting all the books data.
        books_data = [book for book in get_books_data(books_urls)]
        print("Books data:\n", [book for book in books_data])

        print(f"Total books: {len(books_data)}")
        # 5 - Write all the data inside a csv file.
        book_csv = write_books_for_category_to_csv(category_name, books_data)
        # 6 - Download the images of each books from the category.
        book_pictures = download_book_image(category_name, books_data)
if __name__ == '__main__':
    main()