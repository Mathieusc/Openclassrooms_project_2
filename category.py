import requests
import re
import csv
from bs4 import BeautifulSoup

def get_books_categories_urls():
	""" This function will return a list containing all the urls of each books
	category from every pages of books.toscrape.com"""

	url = "http://books.toscrape.com/index.html"
	response = requests.get(url, timeout=2)
	response.encoding = 'UTF-8'

	books_genres = []
	if response.status_code == 200:
		# precise lxml to avoid the 'GuessedAtParserWarning' message
		soup = BeautifulSoup(response.text, 'lxml')
		category = soup.find('ul', {'class': 'nav nav-list'}).findAll('a')
		for hrefs in category:
			books_genres.append('http://books.toscrape.com/'\
			+ hrefs.attrs['href'])		

		# pages_number = soup.find('li', {'class': 'current'}).text.strip()\
		# .replace('Page 1 of ', '')
		# pages_number = int(pages_number)
		books_genres.pop(0)

		return books_genres

books_category = get_books_categories_urls()

def writes_urls():
	with open('urls.txt', 'w', encoding='UTF-8') as file:
		for link in books_category:
			file.write(link + '\n')

writes_urls()

def get_number_of_pages():
	"""This function will return the number of pages from each category
	as an integer."""

	for lines in books_category:
		response = requests.get(lines, timeout=2)
		response.encoding = 'UTF-8'

		if response.status_code == 200:
			soup = BeautifulSoup(response.text, 'lxml')
			pages_number = soup.find('li', {'class': 'current'})

			if pages_number != None:
				yield str(pages_number.text.strip().replace('Page 1 of ', '')), lines

number_of_pages = get_number_of_pages()

def get_all_pages_from_categories():
	"""This function will return the urls of each pages from one book's
	category."""
	
	for number, category_name in number_of_pages:
		counter = 2
		number = int(number)
		while counter <= number:
			new_url = category_name.replace('index.html', 'page-' +str(counter) + '.html')
			counter = int(counter)
			counter += 1
			yield new_url


# for e in categories_pages_url:
# 	print(e)

def get_all_books_urls_per_categories():
	""" This function will return a list containing all the urls of each books
	from every pages of books.toscrape.com sorted by every categories in
	alphabetical order.."""

	all_urls = []
	for lines in books_category:
		all_urls.append(lines)
		response = requests.get(lines, timeout=2)
		response.encoding = 'UTF-8'

		if response.status_code == 200:
			soup = BeautifulSoup(response.text, 'lxml')
			pages_number = soup.find('li', {'class': 'current'})

			if pages_number:
				categories_pages_url = get_all_pages_from_categories()
				for links in categories_pages_url:
					all_urls.append(links)

	all_urls.sort()
	return all_urls

all_books_urls_sorted = get_all_books_urls_per_categories()
print(type(all_books_urls_sorted))
#print(all_books_urls_sorted)

def write_urls_sorted_by_categories():
	with open('categories_urls_sorted.txt', 'w', encoding='UTF-8') as file:
		for lines in all_books_urls_sorted:
			file.write(lines + '\n')

create_urls_sorted = write_urls_sorted_by_categories()

def books_data_csv_sorted_by_categories():
	for links in all_books_urls_sorted:
		with open('books.csv', 'w', encoding='UTF-8') as out_file:

			fieldnames = ['product_page_url', 'universal_product_code', 'title',\
	'price_including_tax', 'price_excluding_tax', 'number_available',\
	'product_description', 'category', 'review_rating', 'image_url']

			csv_writer = csv.DictWriter(out_file, fieldnames=fieldnames,\
			quoting=csv.QUOTE_ALL)
			csv_writer.writeheader()

			for lines in all_books_urls_sorted:
				url = lines.strip()
				print(url)

				response = requests.get(url, timeout=5)
				response.encoding = 'UTF-8'

				if response.status_code == 200:
					soup = BeautifulSoup(response.text, 'lxml')
					
					book_upc = soup.find('table', 
						{'class': 'table table-striped'})\
						.find('th', text='UPC').find_next_sibling()
					yield book_upc.text

					book_title = soup.find('h1')
					yield book_title.text

					book_price_including_tax = soup.find('table', 
						{'class': 'table table-striped'})\
						.find('th', text='Price (incl. tax)').find_next_sibling()
					yield book_price_including_tax.text

					book_price_excluding_tax = soup.find('table', 
						{'class': 'table table-striped'})\
						.find('th', text='Price (excl. tax)').find_next_sibling()
					yield book_price_excluding_tax.text

					book_availability = soup.find('p'\
						, {'class': 'instock availability'})
					yield book_availability.text.strip()

					book_description = soup.find('h2').find_next()
					yield book_description.text

					book_category = soup.find('li', {'class': 'active'})\
					.find_previous_sibling()
					yield book_category.text.strip()

					book_rating = soup.find(class_=re.compile('^star-'))
					if book_rating.attrs['class'][1] == 'One':
						book_rating_converted = '1'
						yield book_rating_converted
					elif book_rating.attrs['class'][1] == 'Two':
						book_rating_converted = '2'
						yield book_rating_converted
					elif book_rating.attrs['class'][1] == 'Three':
						book_rating_converted = '3'
						yield book_rating_converted
					elif book_rating.attrs['class'][1] == 'Four':
						book_rating_converted = '4'
						yield book_rating_converted
					elif book_rating.attrs['class'][1] == 'Five':
						book_rating_converted = '5'
						yield book_rating_converted

					book_picture = soup.find('img')
					yield 'http://books.toscrape.com/' \
						+ book_picture.attrs['src'].replace('../', '')
					book_picture_url = 'http://books.toscrape.com/' \
						+ book_picture.attrs['src'].replace('../', '')

					rows = [
				{'product_page_url': url,\
				'universal_product_code': book_upc.text,\
				'title': book_title.text,\
				'price_including_tax': book_price_including_tax.text,\
				'price_excluding_tax': book_price_excluding_tax.text,\
				'number_available': book_availability.text.strip(),\
				'product_description': book_description.text,\
				'category': book_category.text.strip(),\
				'review_rating': book_rating_converted,\
				'image_url': book_picture_url}]

					csv_writer.writerows(rows)

# ultimate_scraping = books_data_csv_sorted_by_categories()
# print(ultimate_scraping)

def get_books_data():
	"""This function will scrape every data that we need to write into a file
	from every books from the website."""

	for lines in books_category:
		url = lines.strip()
		yield url

		response = requests.get(url, timeout=5)
		response.encoding = 'UTF-8'

		if response.status_code == 200:
			soup = BeautifulSoup(response.text, 'lxml')
			
			book_upc = soup.find('table', 
				{'class': 'table table-striped'})\
				.find('th', text='UPC').find_next_sibling()
			yield book_upc.text

			book_title = soup.find('h1')
			yield book_title.text

			book_price_including_tax = soup.find('table', 
				{'class': 'table table-striped'})\
				.find('th', text='Price (incl. tax)').find_next_sibling()
			yield book_price_including_tax.text

			book_price_excluding_tax = soup.find('table', 
				{'class': 'table table-striped'})\
				.find('th', text='Price (excl. tax)').find_next_sibling()
			yield book_price_excluding_tax.text

			book_availability = soup.find('p'\
				, {'class': 'instock availability'})
			yield book_availability.text.strip()

			book_description = soup.find('h2').find_next()
			yield book_description.text

			book_category = soup.find('li', {'class': 'active'})\
			.find_previous_sibling()
			yield book_category.text.strip()

			book_rating = soup.find(class_=re.compile('^star-'))
			if book_rating.attrs['class'][1] == 'One':
				book_rating_converted = '1'
				yield book_rating_converted
			elif book_rating.attrs['class'][1] == 'Two':
				book_rating_converted = '2'
				yield book_rating_converted
			elif book_rating.attrs['class'][1] == 'Three':
				book_rating_converted = '3'
				yield book_rating_converted
			elif book_rating.attrs['class'][1] == 'Four':
				book_rating_converted = '4'
				yield book_rating_converted
			elif book_rating.attrs['class'][1] == 'Five':
				book_rating_converted = '5'
				yield book_rating_converted

			book_picture = soup.find('img')
			yield 'http://books.toscrape.com/' \
				+ book_picture.attrs['src'].replace('../', '')
			book_picture_url = 'http://books.toscrape.com/' \
				+ book_picture.attrs['src'].replace('../', '')

# books_data = get_books_data()
# for data in books_data:
# 	print(data)
