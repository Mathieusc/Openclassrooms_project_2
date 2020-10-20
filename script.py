import requests
from bs4 import BeautifulSoup

"""
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

# print(len(links)) >>> 1000
# so we have all the books from the website
print(links)
"""

"""
Note to myself:
It might be useful to add a pause with time.sleep(seconds) with the os
module to avoid being blocked while scraping through all the pages from a
website, or use a proxy...
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

url = "http://books.toscrape.com/catalogue/1000-places-to-see-before-you-die_1/index.html"