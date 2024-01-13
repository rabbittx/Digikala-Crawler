# get all products_id from products table 
# remove duplicate ids 
# get all product links 
# start to scan product page 
# Specifications =  {key:value} 
                    # Numberـofـsellersـofـtheـproduct = '5' else '0' 
                    # Warranty = string or 0  
                    # Digiclub points = int 
                    # Comments = list - >  rate , name , role , recommendation ,comment text , seller , color , like , dislike 
                    # Questions = {question:answer} -> 



# load the page 
# scroll to fotter back to top 
# scroll to the links -> click on them 
# get the page suorce code 
# start to extract info 
# return data 
# store data to the database
# start next page 
 
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from bs4 import BeautifulSoup
import sqlite3 ,time 
from time import gmtime, strftime
from logger import setup_logger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service = Service(r'geckodriver.exe')
driver = webdriver.Firefox(service=service)


def get_seller_source_page( ):
    print(f'start to scroll seller [] page ')
    time.sleep(5)
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)
   

def scroll_to_element(element_xpath,wait_time):
    wait = WebDriverWait(driver, wait_time)
    element = wait.until(EC.presence_of_element_located((By.XPATH, element_xpath)))
    desired_y = (element.size['height'] / 2) + element.location['y']
    current_y = (driver.execute_script('return window.innerHeight') / 2) + driver.execute_script('return window.pageYOffset')
    scroll_y_by = desired_y - current_y
    driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
    return element

# # Introduction
# element = scroll_to_element("//span[@data-cro-id='pdp-more-detail']",10)
# # expert check
# element2 = scroll_to_element("//span[@data-cro-id='pdp-expert-see-more']",10)
# # Specifications
# element3 = scroll_to_element("//span[@class='inline-flex items-center cursor-pointer styles_Anchor--secondary__3KsgY text-button-2']/span[text()='مشاهده بیشتر']",10)
# # opinions of users
# element4 = scroll_to_element("//button[@class='relative flex items-center user-select-none styles_btn__Q4MvL text-button-2 styles_btn--medium__4GoNC styles_btn--text__W2jhM styles_btn--primary__y0GEv rounded-medium text-secondary-500']",10)
# # questions
# element5 = scroll_to_element("//span[@data-cro-id='pdp-question-all']",10)


def load_page(driver,url):
    driver.get(url)
    time.sleep(5)
    get_seller_source_page( )
        # Introduction
    Introduction_element = scroll_to_element("//span[@data-cro-id='pdp-more-detail']",10)
    Introduction_element.click()
        # expert check
    expert_check_element = scroll_to_element("//span[@data-cro-id='pdp-expert-see-more']",10)
    expert_check_element.click()
        # Specifications
    Specifications_element = scroll_to_element("//span[@class='inline-flex items-center cursor-pointer styles_Anchor--secondary__3KsgY text-button-2']/span[text()='مشاهده بیشتر']",10)
    Specifications_element.click()
        # opinions of users
    opinions_of_users_element = scroll_to_element("//button[@class='relative flex items-center user-select-none styles_btn__Q4MvL text-button-2 styles_btn--medium__4GoNC styles_btn--text__W2jhM styles_btn--primary__y0GEv rounded-medium text-secondary-500']",10)
    opinions_of_users_element.click()
        # questions
    questions_element = scroll_to_element("//span[@data-cro-id='pdp-question-all']",10)
    questions_element.click() 
    return driver.page_source
    

page_source = load_page(driver,'https://www.digikala.com/product/dkp-6903697/%D8%AA%D8%A8%D9%84%D8%AA-%D8%A7%D9%BE%D9%84-%D9%85%D8%AF%D9%84-ipad-9th-generation-102-inch-wi-fi-2021-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-64-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA/')
print(page_source)
with open('page_source','w',encoding='utf-8') as file :
    file.write(page_source)

