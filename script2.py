import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/catalogue/\
1000-places-to-see-before-you-die_1/index.html"

response = requests.get(url)

if response.ok:
	soup = BeautifulSoup(response.text, 'lxml')
	book_information = soup.find('table', {'class': 'table table-striped'})
	print(book_information.text)