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




 
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from bs4 import BeautifulSoup
import sqlite3 ,time 
from time import gmtime, strftime
from logger import setup_logger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class product_extrection():
    def __init__(self, driver_path ):
            self.log = setup_logger()
            self.db_path = 'digikala.db'
            self.log.info('Initializing Web Scraper...')
            self.driver = self.initialize_driver(driver_path)
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()

    def initialize_driver(self, driver_path):
        try:
            service = Service(driver_path)
            driver = webdriver.Firefox(service=service)
            self.log.info('Web driver initialized successfully')
            return driver
        except Exception as e:
            self.log.error(f'Error initializing web driver: {e}')
            raise

    def get_seller_source_page( self,):
        print(f'start to scroll seller [] page ')
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
        wait = WebDriverWait(self.driver, wait_time)
        element = wait.until(EC.presence_of_element_located((By.XPATH, element_xpath)))
        desired_y = (element.size['height'] / 2) + element.location['y']
        current_y = (self.driver.execute_script('return window.innerHeight') / 2) + self.driver.execute_script('return window.pageYOffset')
        scroll_y_by = desired_y - current_y
        self.driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
        return element

    def load_page(self,url):
        self.driver.get(url)
        time.sleep(2)
        self.get_seller_source_page( )
            # Introduction
        time.sleep(1)
        Introduction_element = self.scroll_to_element("//span[@data-cro-id='pdp-more-detail']",10)
        time.sleep(1)
        Introduction_element.click()
            # expert check
        expert_check_element = self.scroll_to_element("//span[@data-cro-id='pdp-expert-see-more']",10)
        time.sleep(1)
        expert_check_element.click()
            # Specifications
        Specifications_element = self.scroll_to_element("//span[@class='inline-flex items-center cursor-pointer styles_Anchor--secondary__3KsgY text-button-2']/span[text()='مشاهده بیشتر']",10)
        time.sleep(1)
        Specifications_element.click()
            # opinions of users
        opinions_of_users_element = self.scroll_to_element("//button[@class='relative flex items-center user-select-none styles_btn__Q4MvL text-button-2 styles_btn--medium__4GoNC styles_btn--text__W2jhM styles_btn--primary__y0GEv rounded-medium text-secondary-500']",10)
        time.sleep(1)
        opinions_of_users_element.click()
            # questions
        questions_element = self.scroll_to_element("//span[@data-cro-id='pdp-question-all']",10)
        time.sleep(1)
        questions_element.click() 
        return self.driver.page_source
    
    def make_soup(self,page_source):
        return BeautifulSoup(page_source,"html.parser")
    def safe_find(self,soup,finds, tag, attrs):
        try:
            if finds == 'find':
                return soup.find(tag, attrs)
            elif finds == 'find_all':
                return soup.find_all(tag, attrs)
        except AttributeError:
            return 'element not found'
    
    def product_elements_extrection(self,soup):
      


        specific_text = 'پیشنهاد فروشندگان'
        element = soup.select_one("span:-soup-contains('{}')".format(specific_text)).find_parent('div',{'class':'flex flex-col relative overflow-hidden w-full pt-2 lg:border-complete-200 lg:rounded-medium lg:mt-4 pb-3 styles_PdpProductContent__sectionBorder__39zAX'})
        if element:
            seller_offer = element.find_all("a",{'class':'block cursor-pointer relative bg-neutral-000 overflow-hidden grow py-3 px-4 lg:px-2 h-full border-complete-l'})
        else:
            seller_offer = 'offer not found'   


        return { 
                  
                  'main_product_details' : self.safe_find(soup,'find','div',{'class':'styles_InfoSection__leftSection__0vNpX'}).parent if self.safe_find(soup,'find','div',{'class':'styles_InfoSection__leftSection__0vNpX'}) else 'element not found'  ,
                  
                  'buy_box'  : self.safe_find(soup,'find','div',{'data-testid':'buy-box'}),

                  'image_box' : self.safe_find(soup,'find','div',{'class':'flex flex-col items-center lg:max-w-92 xl:max-w-145 lg:block mb-2'}).find_all('picture') if self.safe_find(soup,'find','div',{'class':'flex flex-col items-center lg:max-w-92 xl:max-w-145 lg:block mb-2'}) else 'images element not found',

                  'other_seller_box':self.safe_find(soup,'find','div',{'id':'sellerSection'}).find_all('div',{'class':'rounded-medium styles_SellerListItemDesktop__sellerListItem__u9p3q p-4'}) if self.safe_find(soup,'find','div',{'id':'sellerSection'}) else "no found other seller for this product",

                  'Similar_products' : self.safe_find(soup,'find_all','a',{'data-cro-id':'related-products'}) ,

                  'related_videos' : self.safe_find(soup,'find_all','div',{"data-cro-id":"magnet_click_on_video"}), 
                  
                  'Introduction_box': self.safe_find(soup,'find','div',{'id':'PdpShortReview'}).parent.find('div',{'class':'text-body-1 text-neutral-800'}).text if self.safe_find(soup,'find','div',{'id':'PdpShortReview'}) else 'Introduction element not found',

                  'expert_check_box': self.safe_find(soup,'find','div',{'id':'expertReview'}).parent if self.safe_find(soup,'find','div',{'id':'expertReview'}) else 'expert check box element not found',

                  'Specifications_box': self.safe_find(soup,'find_all','div',{'class':'w-full flex last styles_SpecificationAttribute__valuesBox__gvZeQ'}),

                  'reviews_box': self.safe_find(soup,'find_all','article',{'class':'py-3 lg:mt-0 flex items-start br-list-vertical-no-padding-200'}),

                  'question_box': self.safe_find(soup,'find_all','article',{'class':'br-list-vertical-no-padding-200 py-3'}),

                  'Bought_next_to_it': self.safe_find(soup,'find_all','a',{'data-cro-id':"also_bought_products"}),                            
                  'seller_offer': seller_offer      
        }


    def test_run(self,):
        with open('page_source.html','r',encoding='utf-8') as file :
            page_source=file.read()
        soup = self.make_soup(page_source)
        elements = self.product_elements_extrection(soup)
        for review in elements['seller_offer']:
            print(review)
            print('\n')
        print(len(elements['seller_offer']))
    def run(self,url):  
        # load the page -> DONE
        # scroll to fotter back to top -> DONE
        # scroll to the links -> click on them -> DONE
        # get the page suorce code -> DONE

        # start to extract info 
        # return data 
        # store data to the database
        # start next page 
         
        page_source = self.load_page(url)
        print(page_source)
        with open('page_source.html','w',encoding='utf-8') as file :
            file.write(page_source)

if __name__=="__main__":
    geko_path = r'geckodriver.exe'
    product_url = 'https://www.digikala.com/product/dkp-6903697/%D8%AA%D8%A8%D9%84%D8%AA-%D8%A7%D9%BE%D9%84-%D9%85%D8%AF%D9%84-ipad-9th-generation-102-inch-wi-fi-2021-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-64-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA/'
    scraper = product_extrection(geko_path,)
    scraper.test_run()