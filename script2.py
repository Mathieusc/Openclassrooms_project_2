# coding: UTF-8
import re
import requests
import csv
from bs4 import BeautifulSoup

def data_csv():
	with open('books_urls.txt', 'r') as in_file:
		with open('books.csv', 'w', encoding='UTF-8') as out_file:

			fieldnames = ['product_page_url', 'universal_product_code', 'title',\
	'price_including_tax', 'price_excluding_tax', 'number_available',\
	'product_description', 'category', 'review_rating', 'image_url']

			csv_writer = csv.DictWriter(out_file, fieldnames=fieldnames,\
			quoting=csv.QUOTE_ALL)
			csv_writer.writeheader()

			for lines in in_file:
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

scraper_de_fou = data_csv()
for e in scraper_de_fou:
	print(e)

def data_csv_sorted_by_categories():
	




	



