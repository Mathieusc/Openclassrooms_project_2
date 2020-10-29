import requests
from bs4 import BeautifulSoup

def get_books_category():
	""" This function will return a list containing all the urls of each books
	category from every pages of books.toscrape.com"""

	books_genres = []
	url = "http://books.toscrape.com/index.html"
	response = requests.get(url)

	if response.ok:
		# precise lxml to avoid the 'GuessedAtParserWarning' message
		soup = BeautifulSoup(response.text, 'lxml')
		category = soup.find('ul', {'class': 'nav nav-list'}).findAll('a')
		for hrefs in category:
			books_genres.append('http://books.toscrape.com/'\
			+ hrefs.attrs['href'])
		books_genres.pop(0)

	return books_genres

books_category = get_books_category()
print(books_category)