from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
import time
from check_page import scan
geko_path = r'geckodriver.exe'
base_url = ["https://www.digikala.com/seller/a9h3m/",'https://www.digikala.com/seller/cajwj/','https://www.digikala.com/seller/cgxgh/','https://www.digikala.com/seller/cwe4n/','https://www.digikala.com/seller/cskc4/','https://www.digikala.com/seller/f7k6y/']


service = Service(geko_path)
driver = webdriver.Firefox(service=service)

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

    info = scan(page_source)
    # save info in database 
    print(info)

for url in base_url:
    scan_sellers(url)