import sys, getopt, os
from google_search import google_create_search_url
from google_search import google_make_selenium_search
from google_search import google_get_links
from nordstrom_search import nordstrom_make_selenium_search
from nordstrom_search import nordstrom_get_links
from utils import download_image
from logger_config import log
import trends


def usage_message():
    print "This script scrapes Nordstrom website or Google images for a clothing with specific tags"
    print "Nordstrom usage: search_type url [-p path]"
    print "Google usage: search_type tag [-s=<search_query>] [-d=<path>] [-l]"
    print "run -h or --help for more"
    exit()


def print_man():
    print "This script scrapes Nordstrom website or Google images for a clothing with specific tags"
    print "Nordstrom usage: search_type url path"
    print "Google usage: search_type tag [-s=<search_query>] [-d=<path>] [-l]"
    print "search_type:"
    print "\tnord specify Nordstrom search"
    print "\tgoogle specify Google search"
    print "Google options:"
    print "\t-s specify Google search query otherwise defaults used"
    print "\t-d specify Directory to save images in"
    print "\t-l print out image links"
    exit()

log('scrape')

args = sys.argv[1:]

if len(args) < 1:
    usage_message()

search_type = args[0]


nordstrom = False
google = False

if search_type == "google": #might need fixing due to changes made
    tag = args[0]
    path = tag

    options = args[2:]
    print "using Google search"
    google = True

    if "-p" in options:
        # TODO: specify path
        pass

elif search_type == "nord":
    if len(args) < 2:
        usage_message()

    nordstrom = True
    url = args[1]
    #path = args[2] TODO
    path = './scraped_images'
def google_search(search, tag):
    """
    takes in a search term and returns the links
    """
    url = google_create_search_url(search, tag)
    html = google_make_selenium_search(url)
    links = google_get_links(html)

    return links

def nordstrom_search(url):
    """
    takes in a url and returns the links
    """
    links = nordstrom_make_selenium_search(url)

    return links

links = []
print "scraping commenced..."
# if n is set use Nordstrom search
if nordstrom:
    print "searching Nordstrom"
    links += nordstrom_search(url)

else:
    print "searching for Google fashion filtered by the " + tag + " tag"
    links += google_search("fashion", tag)


num_links = len(links)
print "Found " + str(num_links) + " links"
if num_links == 0:
    exit()

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
        if google:
            filename = tag + str(link_num)
        else:
            filename = str(link_num)
        s = '/'
        filepath = s.join((path, filename))
        download_image(l, filepath)
        link_num += 1
