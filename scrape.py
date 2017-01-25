import sys, getopt, os
from google_search import create_search_url
from google_search import make_selenium_search
from google_search import get_links
from utils import download_image
from logger_config import log
import trends


search = None
path = None
print_links = False


def usage_message():
    print "This script scrapes Google images for a clothing with specific tags"
    print "usage: tag [-s=<search_query>] [-d=<path>] [-l]"
    print "run -h or --help for more"
    exit()


def print_man():
    print "This script scrapes Google images for a clothing with specific tags"
    print "usage: tag [-s=<search_query>] [-d=<path>] [-l]"
    print "Options:"
    print "\t-s specify Google search query otherwise defaults used"
    print "\t-d specify Directory to save images in"
    print "\t-l print out image links"
    exit()

log('scrape')

args = sys.argv[1:]
if len(args) < 1:
    usage_message()

f_arg = args[0]
if f_arg == '-h' or f_arg == '--help':
    print_man()

#grab tag as first arg
tag = f_arg
try:
    opts, args = getopt.getopt(args[1:], "s:d:l")
except getopt.GetoptError:
    print "Error getting args"
    usage_message()

for opt, arg in opts:
    if opt == '-s':
        search = arg
    if opt == '-d':
        path = arg
    if opt == '-l':
        print_links = True

def search_fashion_term(search, tag):
    """
    takes in a search term and returns the links
    """
    url = create_search_url(search, tag)
    html = make_selenium_search(url)
    links = get_links(html)

    return links

links = []
print "scraping commenced..."
if not search:
    fashion_searches = trends.get_related_words("clothing")
    fashion_searches += trends.get_related_words("fashion")
    for s in fashion_searches:
        print "term -> " + s
        links += search_fashion_term(s, tag)
        print "links: " + str(len(links))
else:
    print "searching for " + search + " filtered by the " + tag + " tag"
    links += search_fashion_term(search, tag)

num_links = len(links)
print "Found " + str(num_links) + " links"
if num_links == 0:
    exit()

if print_links:
    for l in links:
        print l

if path:
    print "Saving images to file"

    # make the folder
    if not os.path.exists(path):
        os.makedirs(path)

    link_num = 0
    links = list(set(links)) # clears any duplicate links
    for l in links:
        filename = tag + str(link_num)
        s = '/'
        filepath = s.join((path, filename))
        download_image(l, filepath)
        link_num += 1
