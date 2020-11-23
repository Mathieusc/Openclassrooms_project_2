# coding: UTF-8
import requests
from bs4 import BeautifulSoup

def get_books_categories_urls():
	""" This function will return a list containing all the urls of each books
	category from every pages of books.toscrape.com"""

	url = "http://books.toscrape.com/index.html"
	response = requests.get(url, timeout=5)
	response.encoding = 'UTF-8'

	books_genres = []
	if response.status_code == 200:
		# precise lxml to avoid the 'GuessedAtParserWarning' message
		soup = BeautifulSoup(response.text, 'lxml')
		category = soup.find('ul', {'class': 'nav nav-list'}).findAll('a')
		for hrefs in category:
			books_genres.append('http://books.toscrape.com/'\
			+ hrefs.attrs['href'])		

		pages_number = soup.find('li', {'class': 'current'}).text.strip()\
		.replace('Page 1 of ', '')
		pages_number = int(pages_number)
		books_genres.pop(0)

		return books_genres

books_category = get_books_categories_urls()
for e in books_category:
	print(e)
print(type(books_category))

def get_books_categories_name():
	"""This function will return a list of all the categories of each books
	from books.toscrape.com"""

	books_categories = []
	url = "http://books.toscrape.com/index.html"
	response = requests.get(url, timeout=5)
	response.encoding = 'UTF-8'

	if response.status_code == 200:
		soup = BeautifulSoup(response.text, 'lxml')
		categories = soup.find('ul', {'class': 'nav nav-list'}).findAll('a')
		for names in categories:
			# print(names.text.strip().replace('Books', ''))
			books_categories.append(names.text.strip())
		books_categories.pop(0)

		return books_categories



categories_name = get_books_categories_name()
print(categories_name)
