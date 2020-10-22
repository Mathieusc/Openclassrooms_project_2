import re
import requests
from bs4 import BeautifulSoup
import urllib3

url = "http://books.toscrape.com/catalogue/the-wedding-dress_864/index.html"

response = requests.get(url)

if response.ok:
	soup = BeautifulSoup(response.text, 'lxml')
	book_upc = soup.find('table', 
		{'class': 'table table-striped'})\
		.find('th', text='UPC').find_next_sibling()
	print(book_upc.text)

	book_title = soup.find('h1')
	print(book_title.text)

	book_price_including_tax = soup.find('table', 
		{'class': 'table table-striped'})\
		.find('th', text='Price (incl. tax)').find_next_sibling()
	print(book_price_including_tax.text)

	book_price_excluding_tax = soup.find('table', 
		{'class': 'table table-striped'})\
		.find('th', text='Price (excl. tax)').find_next_sibling()
	print(book_price_excluding_tax.text)

	book_availability = soup.find('p', {'class': 'instock availability'})
	print(book_availability.text.strip())

	book_description = soup.find('h2').find_next()
	#print(book_description.text)

	book_category = soup.find('li', {'class': 'active'})\
	.find_previous_sibling()
	print(book_category.text.strip())

	#book_rating = soup.find(class_=re.compile('^star-rating\ .'))
	#print(book_rating)

	book_rating = soup.find('p', {'class': re.compile(r'^star-rating\s[A-Z]')})
	#print(book_rating)

	http = urllib3.PoolManager()
	images = soup.findAll('img')
	for image in images:
		print(image['src'])



	



