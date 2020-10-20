import requests
from bs4 import BeautifulSoup

links = []

for i in range(51):

	url = "http://books.toscrape.com/catalogue/page-" + str(i) + ".html"
	response = requests.get(url)

	if response.ok:
		# precise lxml or 'GuessedAtParserWarning'
		soup = BeautifulSoup(response.text, 'lxml')
		articles = soup.findAll('article')

		for article in articles:
			a = article.find('a')
			# use brackets to select attributs from an href tag (like a list index)
			link = a['href']
			links.append('http://books.toscrape.com/catalogue/' + link)

			print(links)