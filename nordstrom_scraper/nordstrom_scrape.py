import sys, getopt, os
from nordstrom_search import create_search_url
from nordstrom_search import make_selenium_search
from nordstrom_search import get_links
from utils import download_image

def search():
    """
    takes in a search term and returns the links
    """
    url = create_search_url()
    links = make_selenium_search(url)

    return links

links = []
print "scraping commenced..."
#n = 1000
links += search()

num_links = len(links)
print "Found " + str(num_links) + " links"
if num_links == 0:
    exit()

for l in links:
        print l

path = "/Users/tomlarge/Desktop/FashionSense/nordstrom_scraper/scraped_images"
print "Saving images to file"

# make the folder
if not os.path.exists(path):
    os.makedirs(path)

link_num = 0
links = list(set(links)) # clears any duplicate links
for l in links:
    filename = str(link_num)
    s = '/'
    filepath = s.join((path, filename))
    download_image(l, filepath)
    link_num += 1
