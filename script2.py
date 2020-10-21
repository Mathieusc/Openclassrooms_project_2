import requests
from bs4 import BeautifulSoup
import re

url = "http://books.toscrape.com/catalogue/\
1000-places-to-see-before-you-die_1/index.html"

response = requests.get(url)

if response.ok:
	soup = BeautifulSoup(response.text, 'lxml')
	book_information = soup.find('table', {'class': 'table table-striped'}).find('th', text='Product Type').find_next_sibling()
	print(book_information)