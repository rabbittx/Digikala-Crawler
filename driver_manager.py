# TODO install driver here 
import time
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class DriverManager:
    def __init__(self,log, driver_path):
        self.log = log
        self.driver_path =driver_path
        self.log.info('Initializing Web Scraper...')
        self.driver = self.initialize_driver()
    def initialize_driver(self,):
        try:
            service = Service(self.driver_path)
            driver = webdriver.Firefox(service=service)
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



    def close_driver(self):
        if self.driver:
            self.driver.quit()

