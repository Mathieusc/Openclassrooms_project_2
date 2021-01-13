"""
    This program will download every books from books.toscrape.com and will
    create a .csv file for each categories. These last will be sorted into
    their corresponding directories and every book's pictures will be
    downloaded into an image directory aswell !
"""

from scraper_functions import (
    create_book_dict_categories_urls,
    get_number_of_pages,
    get_books_urls,
    get_books_data,
    write_books_for_category_to_csv,
    download_book_image,)

def main():
    category_counter = 49
    books_counter = 1000
    all_categories = create_book_dict_categories_urls()
    # Creating a dictionary with each categories associated with their urls.
    print(f"Scrapping all the books from books.toscrape.com\n\
    Total Categories: {len(all_categories)}\n\
    Total Books: {books_counter}")
    # Looping through each categories, 6 steps total:
    for category_name, index_url in all_categories.items():
        # 1 - getting all the pages from one category if they exists.
        nb_of_pages = get_number_of_pages(index_url)
        # 2 - getting all the urls from all the books from all the pages of one
        # category.
        books_urls = get_books_urls(nb_of_pages)
        # 4 - getting all the books data.
        books_data = [book for book in get_books_data(books_urls)]
        print(f"Gathering books from the category: {category_name}\n\
    Total books to scrape: {len(books_urls)}")
        # 5 - Write all the data inside a csv file.
        write_books_for_category_to_csv(category_name, books_data)
        print("Writing data into a csv file...")
        # 6 - Download the images of each books from the category.
        print("Downloading pictures...")
        download_book_image(category_name, books_data)
        print("Download complete !")
        books_counter -= len(books_urls)
        print(f"{category_name} category done, {category_counter} categories \
and {books_counter} books remaining !")
        print("-------------------------------------------------------------")
        category_counter -= 1


if __name__ == '__main__':
    main()
