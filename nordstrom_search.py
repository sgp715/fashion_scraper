import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
#def create_search_url():
#    return "http://shop.nordstrom.com/c/womens-formal-dresses?origin=leftnav&cm_sp=Left%20Navigation-_-Formal"

def nordstrom_make_selenium_search(url):
    """
    use selenium to google image search and returns the page html
    """

    #chromedriver = "/Users/tomlarge/Desktop/FashionSense/nordstrom_scraper/chromedriver"
    #os.environ["webdriver.chrome.driver"] = chromedriver
    #browser = webdriver.Chrome()
    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.User-Agent'] = USER_AGENT
    browser = webdriver.PhantomJS()

    # wait for dom to load
    browser.execute_script('return document.readyState;')

    imglinks = []
    pagenum = 1
    while True:
        print "SCRAPING..."
        page_url = url+"&page="+str(pagenum)
        print page_url
        browser.get(page_url)
        pagenum += 1

        time.sleep(5)

        #### GETTING NUMBER OF IMAGES AVAILABLE FOR CATEGORY #####
        total_images_div = browser.find_element_by_class_name('product-results-nav')
        total_images_str = total_images_div.find_elements_by_xpath("//button")
        for i in total_images_str:
            if i.text[0:9] == "All Items":
                total_images_str = i.text[10:]
                total_images = ""
                break

        for i in range(len(total_images_str)):
            if total_images_str[i] != "(" and total_images_str[i] != ")":
                total_images += total_images_str[i]

        total_images = int(total_images)
        ############################################################
        print "Gathering a total of", total_images, "images."
        html = browser.page_source
        imglinks.extend(nordstrom_get_links(html))

        if len(imglinks) >= total_images-10:
            print "GOT ALL IMAGES"
            break
        time.sleep(5)

    browser.quit()

    return imglinks

def nordstrom_get_links(html):
    """
    given html finds all links on google search page
    """

    soup = BeautifulSoup(html, "html.parser")

    images = soup.findAll("img", { "class" : "product-photo" })

    links = []
    #ctr = 0
    for i in images:
        #if ctr == n:
        #    break
        links.append(i['src'])
    #    ctr += 1

    return links
