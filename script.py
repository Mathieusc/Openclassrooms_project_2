import requests
from bs4 import BeautifulSoup

def get_books_urls():
	""" This function will return a list of all the links of each books
	from books.toscrape.com"""

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
	return links

def get_books_data():


# print(len(links)) >>> 1000
# so we have all the books from the website
books_urls = get_books_urls()
#print(books_urls)


"""
Note to myself:
It might be useful to add a pause with time.sleep(seconds) with the os
module to avoid being blocked while scraping through all the pages from a
website, or use a proxy, or with requests.timeout parameter
It doesn't seem to be an issue with this website tho.
"""

#-----------------------------------------------------------------------------
# Save all the urls inside a txt file for now.
# I will create a CSV file later

""" 
Create the file
with open('urls.txt', 'w') as file:
	for link in links:
		file.write(link + '\n')

Read the file
with open('urls.txt', 'r') as file:
	for row in file:
		print(row)
"""