from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from getpass import getpass
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
import time
geko_path = r'geckodriver.exe'
base_url = "https://www.digikala.com/seller/a9h3m/"



service = Service(geko_path)
driver = webdriver.Firefox(service=service)
driver.get(base_url)
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
    page_source = driver.page_source

with open('soucre.html','w',encoding='utf-8') as file :
    file.write(str(page_source))
