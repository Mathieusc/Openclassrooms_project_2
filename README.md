# Openclassrooms Project 2

Web scraping program that will download the data of all the books from https://books.toscrape.com

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Download Python if it is not already installed on your system:


https://www.python.org/downloads/


### Installing

Install pip, the package installer for Python:

```
pip install pip
```

Download the zip file from the project and extract it. (or clone it with git if you have it)

Go to the directory of the project from a terminal.
(or shift right click from the project directory, open terminal)

```
git clone https://github.com/Mathieusc/Project_2
cd path_of_folder\Project_2
```

Create and activate the virtual environment on Linux:
```
python -m venv env
source env/bin/activate
```
On Windows:
```
python -m venv env
.\env\Scripts\Activate.ps1
```

Install the modules used for the project:

```
pip install -r requirements.txt
```

## Running the tests

To run the program simply run scraper.py with Python:

```
python scraper.py
```

The program will scrape through each category from the website,
download the data of all the books into a .csv file and download
all the images of all the books into their respective directories!

## Known issue

On Windows, one picture cannot be downloaded, the following error raises:
FileNotFoundError on [this book](https://books.toscrape.com/catalogue/at-the-existentialist-cafe-freedom-being-and-apricot-cocktails-with-jean-paul-sartre-simone-de-beauvoir-albert-camus-martin-heidegger-edmund-husserl-karl-jaspers-maurice-merleau-ponty-and-others_459/index.html)
Used a try except for this picture for now to keep the program running.


## Built With

* [Python](https://www.python.org/) - Programming language
* [Sublim Text](https://www.sublimetext.com/) - Text editor

## Author

* **Mathieu Schweitzer** - *alias* - [Mathieusc](https://github.com/Mathieusc)


