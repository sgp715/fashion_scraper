import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'


def create_search_url(search, tag):
    """
    given the search and tag generate the url
    """

    search_query = search.replace(' ','+')
    search_tag = tag.replace(' ','+')

    clothing_tag = "clothing"
    url = 'https://www.google.com/search?q='+ search_query +'&espv=2&biw=1183&bih=595&site=webhp&source=lnms&tbm=isch&sa=X&ved=0ahUKEwi43K3ez6TRAhWl6YMKHaAIB7MQ_AUIBigB#tbm=isch&q='+ search_query +'&chips=q:'+ search_query +',g_1:' + clothing_tag + ',g_2:' + search_tag

    return url


def make_request_search(url):
    """
    makes a request to google image search and returns the page html
    """

    headers={'User-Agent': USER_AGENT}
    r = requests.get(url, headers=headers)

    html = r.text

    return html


def make_selenium_search(url):
    """
    use selenium to google image search and returns the page html
    """

    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.User-Agent'] = USER_AGENT
    browser = webdriver.PhantomJS()
    browser.get(url)

    # wait for dom to load
    browser.execute_script('return document.readyState;')


    """
    So, to get the maximum number of images for a search, you can scroll until
    you see the 'show more results' button. Then you can click it and scroll all
    the way down again. But, it will not offer to show more results again (that seems
    to give ~900 images total).
    """
    height = -1
    while True:

        # scroll and set new height
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        new_height = browser.execute_script("return document.body.scrollHeight;")

        # if it was the same we have hit the bottom and are done
        if height == new_height:
            break

        try:
            browser.find_element_by_id('smb').click()
        except:
            pass

        height = new_height

        # give time for images to load
        time_for_scroll = 3
        time.sleep(time_for_scroll) # TODO: find a less janky way

    html = browser.page_source

    browser.quit()

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
