"""
    Documentation du module
"""

import requests
import re
import csv
import time
from bs4 import BeautifulSoup
from extract_data import *


def main():
	"""Run the whole program."""
	books_categories_name = get_books_categories_name()
	print(books_categories_name)
	print(len(books_categories_name))
	print(type(books_categories_name))
	print('\n')
	books_categories_url = get_books_categories_urls()
	print(books_categories_url)
	print(len(books_categories_url))
	print('\n')

	books_categories_list = get_books_names_urls(books_categories_name, 
									  books_categories_url)
	# print(books_categories_list[0][0], 
	#       books_categories_list[1][0])
	      							   # [0] gives the categories names
									   # [1] gives the categories urls
									   # [0][0] = Academic
									   # [1][0] = Academic url

	# ------------------------------------------------------------------------
	# Main loop of the main program
	# ------------------------------------------------------------------------
	# Find the number of pages
	number_of_pages = get_number_of_pages(books_categories_url)
	# for x in number_of_pages:
	# 	print(x)
	pages_index = get_pages_index(books_categories_url)
	# for ze in pages_index:
	# 	print(ze)
	# Create a list of books for each categories
	books_list = create_book_list(books_categories_name)
	print(books_list)
	# Loop for each pages
	all_pages = get_all_pages_from_categories(number_of_pages)
	for m in all_pages:
		print(m)
if __name__ == '__main__':
	main()