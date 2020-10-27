import re
import requests
import csv
from bs4 import BeautifulSoup

with open('urls.txt', 'r') as in_file:
	with open('books.csv', 'w', encoding='utf-8') as out_file:
		fieldnames = ['product_page_url', 'universal_product_code', 'title',\
'price_including_tax', 'price_excluding_tax', 'number_available',\
'product_description', 'category', 'review_rating', 'image_url']
		csv_writer = csv.DictWriter(out_file, fieldnames=fieldnames,\
		quoting=csv.QUOTE_ALL)
		csv_writer.writeheader()

		for lines in in_file:
			url = lines.strip()
			print(url)

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

				book_availability = soup.find('p'\
					, {'class': 'instock availability'})
				print(book_availability.text.strip())

				book_description = soup.find('h2').find_next()
				print(book_description.text)

				book_category = soup.find('li', {'class': 'active'})\
				.find_previous_sibling()
				print(book_category.text.strip())

				book_rating = soup.find(class_=re.compile('^star-'))
				if book_rating.attrs['class'][1] == 'One':
					book_rating_converted = '1'
					print(book_rating_converted)
				elif book_rating.attrs['class'][1] == 'Two':
					book_rating_converted = '2'
					print(book_rating_converted)
				elif book_rating.attrs['class'][1] == 'Three':
					book_rating_converted = '3'
					print(book_rating_converted)
				elif book_rating.attrs['class'][1] == 'Four':
					book_rating_converted = '4'
					print(book_rating_converted)
				elif book_rating.attrs['class'][1] == 'Five':
					book_rating_converted = '5'
					print(book_rating_converted)

				book_picture = soup.find('img')
				print('http://books.toscrape.com/' \
					+ book_picture.attrs['src'].replace('../', ''))
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



	



