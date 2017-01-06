# FASHION SCRAPER

## Description
Scrapes google search for images based on a query and a tag

## Install
1. install all pyhon requirements
```
$ pip install -r requirements.txt
```
2. download and install [NodeJS](https://nodejs.org/en/download/)
3. install PhantomJS
```
$ sudo npm install -g phantomjs
```

## Usage
* to get some help you can type
```
$ python scrape.py --help
This script scrapes Google images for a clothing with specific tags
usage: tag [-s=<search_query>] [-d=<path>] [-l]
Options:
    -s specify Google search query otherwise defaults used
    -d specify Directory to save images in
    -l print out image links
```

## Examples
* to scrape with the vintage tag (and some default search values)
```
$ python scrape.py vintage
```
* to scrape with the vintage tag and the fashion search value
```
$ python scrape.py vintage -s fashion
```
* to scrape the vintage tag and print all the links found
```
$ python scrape.py vintage -l
```
* to scrape the vintage tag and save the images to the vintage directory
```
$ python scrape.py vintage -d vintage
```
