import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
#def create_search_url():
#    return "http://shop.nordstrom.com/c/womens-formal-dresses?origin=leftnav&cm_sp=Left%20Navigation-_-Formal"

def macys_make_selenium_search(url):
    """
    use selenium to google image search and returns the page html
    """

    #CHROME DRIVER
    #chromedriver = "/Users/tomlarge/Desktop/FashionSense/nordstrom_scraper/chromedriver"
    #os.environ["webdriver.chrome.driver"] = chromedriver
    #browser = webdriver.Chrome()

    #PHANTOM JS
    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.User-Agent'] = USER_AGENT
    browser = webdriver.PhantomJS()

    # wait for dom to load
    browser.execute_script('return document.readyState;')

    imglinks = []
    pagenum = 1
    page_url = url

    print "SCRAPING..."

    browser.get(page_url)
    #### GETTING NUMBER OF IMAGES AVAILABLE FOR CATEGORY #####
    total_images_div = browser.find_element_by_class_name('productCount')
    total_images = int(total_images_div.text)
    total_pages_div = browser.find_elements_by_class_name('paginationSpacer')
    pages_list = []
    total_pages = 0

    for i in range(len(total_pages_div)):
        try:
             temp = int(total_pages_div[i].text)
        except:
             continue

        if temp > total_pages:
            total_pages = temp


    print "Gathering at least", total_images, "images from", total_pages, "pages"
    ############################################################
    while pagenum <= total_pages:
        print "On page:", pagenum
        browser.get(page_url)
        html = browser.page_source
        imglinks.extend(macys_get_links(html))

        if page_url.find("Pageindex/") != -1:
            page_url = page_url.split("Pageindex/"+str(pagenum))
            pagenum += 1
            page_url = page_url[0] + "Pageindex/"+str(pagenum)+page_url[1]

        else:
            pagenum += 1
            idx = page_url.find("?id")
            page_url = page_url[0:idx] + "/Pageindex/" + str(pagenum) + page_url[idx:]

        time.sleep(5)

    browser.quit()

    return imglinks

def macys_get_links(html):
    """
    given html finds all links on search page
    """

    soup = BeautifulSoup(html, "html.parser")
    #image_div = browser.find_element_by_class_name('fullColorOverlayOff')
    image_divs = soup.findAll("img", { "class" : "thumbnailImage" })
    print len(image_divs)
    links = []
    #ctr = 0
    for i in image_divs:
        links += [i['data-src']]
    return links
