from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import sqlite3




def get_seller_source_page( driver ,url):
    driver.get(url)
    time.sleep(5)
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(2):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    time.sleep(1)
    return driver.page_source

def get_product(page_source):
    soup = BeautifulSoup(page_source,'html.parser')
    product_element_link = soup.find_all('a',{'class':'block cursor-pointer relative bg-neutral-000 overflow-hidden grow py-3 px-4 lg:px-2 h-full styles_VerticalProductCard--hover__ud7aD'})
    product_link = []
    for element in product_element_link:
        link = 'https://www.digikala.com' + element['href']
        if link not in product_link:
            product_link.append(link)
    return product_link

def find_seller_ids(product_link):
    seller_ids = []
    for link in product_link:
        driver.get(link)
        time.sleep(5)
        div_element = driver.find_element(By.XPATH, '//div[@class="flex flex-col lg:mr-3 lg:mb-3 lg:gap-y-2 styles_InfoSection__buyBoxContainer__3nOwP"]')
        link_element = div_element.find_element(By.XPATH, './/a[@class="styles_Link__RMyqc"]')
        href_value = link_element.get_attribute('href').split('/')[-2]
        if href_value not in seller_ids:
            seller_ids.append(href_value)
    return seller_ids

if __name__ =="__main__":
        
    service = Service('geckodriver.exe')

    driver = webdriver.Firefox(service=service)


    catagori_url = 'https://www.digikala.com/search/category-notebook-netbook-ultrabook/asus/'

    page_source = get_seller_source_page(driver, catagori_url)
    product_link = get_product(page_source)
    find_seller_ids(product_link)