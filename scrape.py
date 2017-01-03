import requests
import shutil
from bs4 import BeautifulSoup


def download_image(url, path):
    """
    given the url of an image dowload image to specified path
    """

    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)


def search_tag(search, tag):
    """
    makes a request to google image search and returns the page html
    """

    search_query = search.replace(' ','+')
    search_tag = tag.replace(' ','+')

    url = 'https://www.google.com/search?q='+ search_query +'&espv=2&biw=1183&bih=595&site=webhp&source=lnms&tbm=isch&sa=X&ved=0ahUKEwi43K3ez6TRAhWl6YMKHaAIB7MQ_AUIBigB#tbm=isch&q='+ search_query +'&chips=q:'+ search_query +',g_1:' + search_tag

    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    r = requests.get(url, headers=headers)

    html = r.text

    return html


def get_links(html):
    """
    given html finds all links on google search page
    """

    soup = BeautifulSoup(html, "html.parser")

    divs = soup.findAll("div", { "class" : "rg_meta" })

    links = []
    for div in divs:
        link = str(div).partition('"ou":"')[-1]
        link = link.rpartition('","ow"')[0]
        links.append(link)

    return links


if __name__ == "__main__":

    search = raw_input('What would you like th search to be?\n')
    tag = raw_input('What tag would you like to search?\n')

    html = search_tag(search, tag)
    links = get_links(html)

    print "Links found:"
    print links
