import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/"
response = requests.get(url)

if response.ok:
	# precise lxml or 'GuessedAtParserWarning'
	soup = BeautifulSoup(response.text, 'lxml')
	articles = soup.findAll('article')
	print(len(articles))