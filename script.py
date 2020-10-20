import requests
from bs4 import BeautifulSoup


links = []

for i in range(51):

	url = "http://books.toscrape.com/catalogue/page-" + str(i) + ".html"
	response = requests.get(url)

	if response.ok:
		#print('Page: ' + str(i) + '\n')
		# precise lxml or 'GuessedAtParserWarning'
		soup = BeautifulSoup(response.text, 'lxml')
		articles = soup.findAll('article')

		for article in articles:
			a = article.find('a')
			# use brackets to select attributs from an href tag (like a list)
			link = a['href']
			links.append('http://books.toscrape.com/catalogue/' + link)

print(links)

"""
Note to myself:
It might be useful to add a pause with time.sleep(seconds) with the os
module to avoid being blocked while scraping through all the pages from a
website, or use a proxy...
It doesn't seem to be an issue with this website tho.
"""