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
    while True:
        print "SCRAPING..."
        print page_url

        browser.get(page_url)
        #### GETTING NUMBER OF IMAGES AVAILABLE FOR CATEGORY #####
        total_images_div = browser.find_element_by_class_name('productCount')
        total_images = int(total_images_div.text)

        ############################################################
        print "Gathering a total of", total_images, "images."
        html = browser.page_source
        imglinks.extend(macys_get_links(html))

        if len(imglinks) >= total_images-10:
            print "GOT ALL IMAGES"
            break

        page_url = url.split("Pageindex/"+str(pagenum))
        pagenum += 1
        page_url = page_url[0] + "Pageindex/"+str(pagenum)+page_url[1]

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
    links = []
    #ctr = 0
    for i in image_divs:
        links += [i['data-src']]
    return links
