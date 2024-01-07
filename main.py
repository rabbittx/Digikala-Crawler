from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
import time
from check_page import seller_details,extract_product_details
from bs4 import BeautifulSoup
import sqlite3

def scan_sellers(url):
    driver.get(url)
    time.sleep(5)

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # اسکرول به انتهای صفحه
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # انتظار برای بارگذاری محتوای جدید
        time.sleep(5)

        # محاسبه ارتفاع جدید و مقایسه با ارتفاع قبلی
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    driver.execute_script("window.scrollTo(0, 0);")

    details_elemnt = driver.find_element(By.XPATH,"//p[text()='جزئیات بیشتر']/..")
    time.sleep(1)
    details_elemnt.click()
    page_source = driver.page_source


    soup = BeautifulSoup(page_source,'html.parser')
    seller_detail = seller_details(soup)
    product_details = [extract_product_details(product) for product in soup.find_all('div', {'class':'product-list_ProductList__item__LiiNI'})]
    # save info in database 
    cursor.execute('''
        INSERT INTO sellers (seller_name, membership_period, satisfaction_with_goods, seller_performance, people_have_given_points, timely_supply, obligation_to_send, no_return, introduction_of_the_seller)
        VALUES (:seller_name, :membership_period, :satisfaction_with_goods, :seller_performance, :people_have_given_points, :timely_supply, :obligation_to_send, :no_return, :introduction_of_the_seller)
        ''', seller_detail)
    
    for product in product_details:
        product['seller_name'] = seller_detail['seller_name']
        cursor.execute('''
        INSERT INTO products (seller_name,product_id, product_link, product_image, product_rate, product_name, product_price, product_price_discount_percent, product_price_discount, product_special_sale, stock)
        VALUES (:seller_name,:product_id, :product_link, :product_image, :product_rate, :product_name, :product_price, :product_price_discount_percent, :product_price_discount, :product_special_sale, :stock)
        ''', product)

# Commit and close
geko_path = r'geckodriver.exe'
base_url = ["https://www.digikala.com/seller/a9h3m/",'https://www.digikala.com/seller/cajwj/','https://www.digikala.com/seller/cgxgh/','https://www.digikala.com/seller/cwe4n/','https://www.digikala.com/seller/cskc4/','https://www.digikala.com/seller/f7k6y/']

# base_url = ["https://www.digikala.com/seller/a9h3m/"]
service = Service(geko_path)
driver = webdriver.Firefox(service=service)
conn = sqlite3.connect('seller_data.db')
cursor = conn.cursor()


for url in base_url:
    scan_sellers(url)
conn.commit()
conn.close()