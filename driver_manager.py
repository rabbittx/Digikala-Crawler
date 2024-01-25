import time
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Union
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options

# TODO driver Option need to add 
# TODO fix chrome driver (work with firefox and chrome)  
class DriverManager:
    def __init__(self, driver_path,log):
        self.log = log
        self.driver_path =driver_path
        self.log.info('Initializing Web Scraper...')
        self.driver = self.initialize_driver(headless=True) # to make driver headless set it to True 
   
    def initialize_driver(self, headless=False):
        try:
            options = Options()

            if headless:
                options.add_argument("--headless")

            service = Service(self.driver_path)
            driver = webdriver.Firefox(service=service, options=options)

            driver.maximize_window()
            self.log.info('Web driver initialized successfully')
            return driver
        except Exception as e:
            self.log.error(f'Error initializing web driver: {e}')
            raise

    def get_prdouct_source_page( self,):
        current_url_id = self.driver.current_url.split('/')[4]
        print(f'start to scroll prdouct [{current_url_id}] page ')
        time.sleep(5)
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)

    def scroll_to_element(self,element_xpath,wait_time):
        self.wait = WebDriverWait(self.driver, wait_time) # TODO duplicate [01]
        element = self.wait.until(EC.presence_of_element_located((By.XPATH, element_xpath)))
        desired_y = (element.size["height"] / 2) + element.location["y"]
        current_y = (self.driver.execute_script('return window.innerHeight') / 2) + self.driver.execute_script('return window.pageYOffset')
        scroll_y_by = desired_y - current_y
        self.driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
        return element
    
    def load_page(self,url):
            self.driver.get(url)
            self.wait = WebDriverWait(self.driver, 20) # TODO duplicate [01]
            time.sleep(2)
            self.get_prdouct_source_page( )
            try:
                # Introduction
                time.sleep(1)
                if self.wait.until(EC.presence_of_element_located((By.XPATH, "//span[@data-cro-id='pdp-more-detail']"))) :
                    Introduction_element = self.scroll_to_element("//span[@data-cro-id='pdp-more-detail']",20)
                    time.sleep(1)
                    Introduction_element.click()
            except :
                self.log.info('more Introduction element not found')  
            try:
            # expert check
                if self.wait.until(EC.presence_of_element_located((By.XPATH, "//span[@data-cro-id='pdp-expert-see-more']"))) :
                    expert_check_element = self.scroll_to_element("//span[@data-cro-id='pdp-expert-see-more']",20)
                    time.sleep(1)
                    expert_check_element.click()
            except :
                self.log.info('more expert check element not found')
            try:
            # Specifications
                if self.wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='inline-flex items-center cursor-pointer styles_Anchor--secondary__3KsgY text-button-2']/span[text()='مشاهده بیشتر']"))) :
                    Specifications_element = self.scroll_to_element("//span[@class='inline-flex items-center cursor-pointer styles_Anchor--secondary__3KsgY text-button-2']/span[text()='مشاهده بیشتر']",20)
                    time.sleep(1)
                    Specifications_element.click()
            except :
                self.log.info('more Specifications element not found')
            try:
            # opinions of users
                if self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@class='relative flex items-center user-select-none styles_btn__Q4MvL text-button-2 styles_btn--medium__4GoNC styles_btn--text__W2jhM styles_btn--primary__y0GEv rounded-medium text-secondary-500']"))) :
                    opinions_of_users_element = self.scroll_to_element("//button[@class='relative flex items-center user-select-none styles_btn__Q4MvL text-button-2 styles_btn--medium__4GoNC styles_btn--text__W2jhM styles_btn--primary__y0GEv rounded-medium text-secondary-500']",20)
                    time.sleep(1)
                    opinions_of_users_element.click()
            except :
                self.log.info('more opinions of users element not found')
            try:
            # questions
                if self.wait.until(EC.presence_of_element_located((By.XPATH, "//span[@data-cro-id='pdp-question-all']"))) :
                    questions_element = self.scroll_to_element("//span[@data-cro-id='pdp-question-all']",20)
                    time.sleep(1)
                    questions_element.click() 
            except :
                self.log.info('more question element not found')

            return self.driver.page_source

    def open_page(self,url:str):
        self.driver.get(url)
        time.sleep(5)
        self.log.info('[+] page open successfully ')

    def click_on_element_by_xpath(self,xpath):
        elemnt = self.driver.find_element(By.XPATH,xpath)
        time.sleep(1)
        elemnt.click()
        self.log.info('[+] click on element successfully ')   

    def scroll_down(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5) # find element to use WebDriverWait() instead of of time.sleep()
                         # metod 1 for category and seller page 
                            # get product elements len() if new_product_count > product_count keep scrolling 

    def scroll_to_top(self):
        self.driver.execute_script("window.scrollTo(0, 0);")    

    def scroll_page(self, scroll_count: Union[int, bool]):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        if scroll_count is True:
            while True:
                self.scroll_down()
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            self.log.info('[+] page scrolling successfully ')

        elif isinstance(scroll_count, int):
            for _ in range(scroll_count):
                self.scroll_down()
            self.log.info('[+] page scrolling successfully ')
        else:
            raise ValueError("Invalid input. scroll_count must be an [integer] or [True] value.")
        self.scroll_to_top()

    def get_page_source(self):
        return BeautifulSoup(self.driver.page_source, 'html.parser')
        
    def get_prdoucts_on_page(self,page_source,return_value):
        product_in_page = page_source.find_all('div',{'class':'product-list_ProductList__item__LiiNI'})
        if 'products_element' in return_value:
            self.log.info('[+] products element extrection successfully ')
            return product_in_page
        elif 'products_link'in return_value:
            product_link = []
            for link in product_in_page:
                try:
                    href = f"https://www.digikala.com{link.find('a')['href']}"
                    if href not in product_link:
                        product_link.append(href)
                except:
                    self.log.error('product link not found') 
            self.log.info('[+] products link extrection successfully ')   
            return product_link
        else :
            raise KeyError("Key Error : check your return_value parameter ")
    
    def get_seller_id(self):
         
        page_source = self.get_page_source()
        try : 
            buy_box =  page_source.find('div',{'data-testid':'buy-box'})
            if 'ناموجود' in buy_box.find('p').text:
                return 'No_seller'
            seller_info = buy_box.find('div',{'data-cro-id':'pdp-seller-info-cta'})
            href = seller_info.find_parent('a',{'class':'styles_Link__RMyqc'})
            seller_id = href['href'].split('/')[-2]
            self.log.info('[+] seller id extrection successfully ')   
            return seller_id
        except Exception as e :
            print(f"Can't find seller id , error : {e}")


    def close_driver(self):
        if self.driver:
            self.driver.quit()
