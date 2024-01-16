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




from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from bs4 import BeautifulSoup, Tag, ResultSet
import unicodedata
import sqlite3 ,time 
from time import gmtime, strftime
from logger import setup_logger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
class product_extrection():
    def __init__(self, driver_path ):
            self.log = setup_logger()
            self.db_path = 'digikala.db'
            self.log.info('Initializing Web Scraper...')
            self.driver = self.initialize_driver(driver_path)
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()

  
        
    def clean_text(self, text):
        ## TODO test with unicodedata
       
        # تعریف پترن با اضافه کردن \n و \n\n به پترن اصلی
        pattern = '[^ا-یآ-ی۰-۹a-zA-Z0-9\s:/\.\-،%(),\n _]'
        # تابع برای بررسی اینکه آیا یک رشته شبیه به URL است یا نه
        def is_url(s):
            return re.match(r'https?://\S+\.\S+', s)

        if isinstance(text, str):
            # اگر رشته شبیه به URL باشد، بدون تغییر باقی می‌ماند
            if is_url(text):
                return text
            # در غیر این صورت، حذف کاراکترهای ناخواسته
            return re.sub(pattern, '', text.replace('\n','').replace('\n\n','').replace('\r','').replace('\xa0',' '))
        elif isinstance(text, list):
            # اعمال تابع بر روی هر عنصر از لیست
            return [self.clean_text(i) for i in text]
        elif isinstance(text, dict):
            # اعمال تابع بر روی هر مقدار از دیکشنری
            return {k: self.clean_text(v) for k, v in text.items()}
    
    def initialize_driver(self, driver_path):
        try:
            service = Service(driver_path)
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
        self.wait = WebDriverWait(self.driver, wait_time)
        element = self.wait.until(EC.presence_of_element_located((By.XPATH, element_xpath)))
        desired_y = (element.size["height"] / 2) + element.location["y"]
        current_y = (self.driver.execute_script('return window.innerHeight') / 2) + self.driver.execute_script('return window.pageYOffset')
        scroll_y_by = desired_y - current_y
        self.driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
        return element


    def check_with_multi_class_name(self,element,field_name,tag_name,attrs_name,attrs_list):

        for class_combo in attrs_list:
            price_span = element.find(tag_name, {attrs_name: class_combo})
            if price_span:
                field = price_span.get_text(strip=True)
                break
            else:
                field = f"{field_name} Not available"

        return field


    def load_page(self,url):
        self.driver.get(url)
        self.wait = WebDriverWait(self.driver, 20)
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
    
    def safe_extraction(self,element_name ,element, extraction_function):
        try:
            return extraction_function(element)
        except Exception as e:
            self.log.error(f'NOT FOUND - {element_name} - {e}')
            return f'{element_name} not found'
        
    def product_elements_extrection(self,soup):
        specific_text = 'پیشنهاد فروشندگان'
        element = soup.select_one("span:-soup-contains('{}')".format(specific_text)).find_parent('div',{'class':'flex flex-col relative overflow-hidden w-full pt-2 lg:border-complete-200 lg:rounded-medium lg:mt-4 pb-3 styles_PdpProductContent__sectionBorder__39zAX'}) if  soup.select_one("span:-soup-contains('{}')".format(specific_text)) else 'element not found'
        
        if isinstance(element, BeautifulSoup):
            seller_offer = element.find_all("a",{'class':'block cursor-pointer relative bg-neutral-000 overflow-hidden grow py-3 px-4 lg:px-2 h-full border-complete-l'})
        else:
            seller_offer = 'offer not found'   
        product_elements = {}
        product_elements["main_product_details"] = self.safe_find(soup,'find','div',{'class':'styles_InfoSection__leftSection__0vNpX'}).parent if self.safe_find(soup,'find','div',{'class':'styles_InfoSection__leftSection__0vNpX'}) else 'element not found'       
        product_elements["buy_box"] = self.safe_find(soup,'find','div',{'data-testid':'buy-box'})
        product_elements["image_box"] = self.safe_find(soup,'find','div',{'class':'flex flex-col items-center lg:max-w-92 xl:max-w-145 lg:block mb-2'}).find_all('picture') if self.safe_find(soup,'find','div',{'class':'flex flex-col items-center lg:max-w-92 xl:max-w-145 lg:block mb-2'}) else 'images element not found'
        product_elements["other_seller_box"] =self.safe_find(soup,'find','div',{'id':'sellerSection'}).find_all('div',{'class':'rounded-medium styles_SellerListItemDesktop__sellerListItem__u9p3q p-4'}) if self.safe_find(soup,'find','div',{'id':'sellerSection'}) else "no found other seller for this product"
        product_elements["similar_products"] = self.safe_find(soup,'find_all','a',{'data-cro-id':'related-products'}) 
        product_elements["related_videos"] = self.safe_find(soup,'find_all','div',{"data-cro-id":"magnet_click_on_video"})                  
        product_elements["introduction_box"] = self.safe_find(soup,'find','div',{'id':'PdpShortReview'}).parent.find('div',{'class':'text-body-1 text-neutral-800'}).text if self.safe_find(soup,'find','div',{'id':'PdpShortReview'}) else 'Introduction element not found'
        product_elements["expert_check_box"] = self.safe_find(soup,'find','div',{'id':'expertReview'}).parent if self.safe_find(soup,'find','div',{'id':'expertReview'}) else 'expert check box element not found'
        product_elements["specifications_box"] = self.safe_find(soup,'find_all','div',{'class':'flex flex-col lg:flex-row pb-6 lg:py-4 styles_SpecificationBox__main__JKiKI'})
        product_elements["reviews_box"] = self.safe_find(soup,'find_all','article',{'class':'py-3 lg:mt-0 flex items-start br-list-vertical-no-padding-200'})
        product_elements["question_box"] = self.safe_find(soup,'find_all','article',{'class':'br-list-vertical-no-padding-200 py-3'})
        product_elements["also_bought_items"] = self.safe_find(soup,'find_all','a',{'data-cro-id':"also_bought_products"})                            
        product_elements["seller_offer"] = seller_offer      
        return product_elements
    
   
    def main_product_details_extrection(self,element):
        if isinstance(element ,(Tag, ResultSet)):

            details={}
            details["product_title"] = self.safe_extraction('product title',element, lambda e: e.find('h1',{'data-testid':'pdp-title'}).text)
            details["product_main_title"] = self.safe_extraction('product main title',element, lambda e: e.find('span',{'class':'text-neutral-300 ml-2 text-body-2'}).text)
            details["user_review"] = self.safe_extraction('user review',element, lambda e: e.find('p',{'class':'ml-2 text-neutral-600 text-body-2'}).text)
            details["colors"] = self.safe_extraction('colors',element, lambda e: [element_color.text for element_color in e.find('div',{"class":"border-complete-t lg:border-none mt-3 lg:mt-0"}).find_all('div',{'data-popper-placement':"bottom"})])
            details["insurer"] = self.safe_extraction('Insurer',element, lambda e: e.find('div',{'class':'bg-neutral-000 flex border-complete-200 rounded-medium'}).find('p',{'class':'text-body2-strong text-neutral-700'}).text)
            details["discount_percent"] = self.safe_extraction('discount percent',element, lambda e: e.find('div',{'class':'bg-neutral-000 flex border-complete-200 rounded-medium'}).find('span',{'data-testid':'price-discount-percent'}).text)
            details["price_before_discount"] = self.safe_extraction('Price before discount',element, lambda e: e.find('div',{'class':'bg-neutral-000 flex border-complete-200 rounded-medium'}).find('div',{'class':'text-body-2 text-neutral-300 line-through'}).text)
            details["final_price"] = self.safe_extraction('final price',element, lambda e: e.find('div',{'class':'bg-neutral-000 flex border-complete-200 rounded-medium'}).find('span',{'data-testid':'price-final'}).text)
            self.log.info('[+] main details extrection succsusfully')
            return details
        else :
            return {}
        
    def product_buy_box_extrection(self,element):
        if isinstance(element ,(Tag, ResultSet)):

            details={}
            details["other_sellers"]= self.safe_extraction('other sellers',element, lambda e: e.find('span',{'data-cro-id':'pdp-other-seller'}).text)
            details["satisfaction_with_the_product"]= self.safe_extraction('satisfaction with the product',element, lambda e: e.find('div',{"data-cro-id":"pdp-seller-info-cta"}).find('p',{'class':'ml-1 text-body2-strong'}).text)
            details["warranty"]= self.safe_extraction('warranty',element, lambda e: e.find('div',{'data-cro-id':'pdp-shipment-info'}).find_previous('p',{'class':'text-button-2 text-neutral-700'}).text)
            details["digiclub_points"]= self.safe_extraction('digiclub points',element, lambda e: e.find('div',{'data-cro-id':'pdp-shipment-info'}).find_next('p',{'class':'text-button-2 text-neutral-700'}).text)
            details["discount_percent"] = self.safe_extraction('discount percent',element, lambda e: e.find('span',{'data-testid':'price-discount-percent'}).text)
            details["price_before_discount"] = self.safe_extraction('Price before discount',element, lambda e: e.find('span',{'data-testid':'price-no-discount'}).text)
            details["final_price"] = self.safe_extraction('final price',element, lambda e: e.find('span',{'data-testid':'price-discount-percent'}).text)
            details["prdouct_stock"] = self.safe_extraction('prdouct stock', element, lambda e: e.find('p',{"class":"text-primary-500 text-body2-strong mb-3"}).text)
          
           
            self.log.info('[+] buy box extrection succsusfully')
            return details
        else :
            return {}
        
    def product_image_extrection(self,element):
        if isinstance(element ,(Tag, ResultSet)):
            return {'product_images' :self.safe_extraction('images',element, lambda e: [image.find('img')["src"] for image in e])}
        else :
            return {}
        
    def other_seller_box_extrection(self,element):
        class_combinations = [
                                'text-h4 ml-1 text-neutral-800',  # کلاس‌ها به صورت معمول
                                'text-neutral-800 ml-1 text-h4',  # کلاس‌ها به صورت معکوس یا با تغییرات دیگر
                                # هر ترکیب دیگری که ممکن است وجود داشته باشد
                            ]
        
        if isinstance(element ,(Tag, ResultSet)):
            other_sellers = []
            for seller in element:
                seller_info = {}
                seller_info["seller_name"] = self.safe_extraction('seller name', seller, lambda e: e.find('p',{'class':'text-neutral-700 ml-2 text-subtitle'}).text)
                seller_info["seller_page_link"] = self.safe_extraction('seller page link', seller, lambda e: e.find('a',{'class':'styles_Link__RMyqc'})["href"])
                seller_info["warranty"] = self.safe_extraction('seller warranty', seller, lambda e: e.find('p',{'class':'text-subtitle text-neutral-700'}).text)
                seller_info["discount_percent"] = self.safe_extraction('discount percent', seller, lambda e: e.find('span',{"data-testid":"price-discount-percent"}).text)
                seller_info["price_before_discount"] = self.safe_extraction('Price before discount', seller, lambda e: e.find('span',{'class':'line-through text-body-2 ml-1 text-neutral-300'}).text)
                # seller_info["final_price"] = self.safe_extraction('final price', seller, lambda e: e.find('span',{'class':'text-h4 ml-1 text-neutral-800'}).text)
                seller_info["final_price"] = self.check_with_multi_class_name(seller,'final price','span','class',class_combinations)
                
                
                other_sellers.append(seller_info)
            self.log.info('[+] other seller extrection succsusfully')
            return other_sellers
        else : return []

    def similar_products_extrection(self,element):
        
        if isinstance(element ,(Tag, ResultSet)):
            similar_products = []
            for product in element:
                similar_products_info={}
                similar_products_info["product_link"] = 'https://www.digikala.com' + self.safe_extraction('product link', product, lambda e: e["href"])
                similar_products_info["product_name"] = self.safe_extraction('product name', product, lambda e: e.find('h3').text)
                similar_products_info["final_price"] = self.safe_extraction('final price', product, lambda e: e.find('span',{"data-testid":"price-final"}).text)
                similar_products_info["prdouct_stock"] = self.safe_extraction('prdouct stock', product, lambda e: e.find('p',{"class":"text-caption text-primary-700"}).text)
                similar_products_info["discount_percent"] = self.safe_extraction('discount percent', product, lambda e: e.find('span',{'data-testid':"price-discount-percent"}).text)
                similar_products_info["price_before_discount"] = self.safe_extraction('price before discount', product, lambda e: e.find('span',{'data-testid':"price-no-discount"}).text)
                similar_products.append(similar_products_info)
            self.log.info('[+] similar products extrection succsusfully')
            return similar_products
        else :
            return []    
    def related_videos_extrection(self,element):
        if isinstance(element ,(Tag, ResultSet)):

            related_videos = []
            for video in element:
                related_videos_info = {}
                related_videos_info["video_title"] = self.safe_extraction('video title', video.parent, lambda e: e.find('div',{'class','mt-2 text-body-1 inline-block ellipsis overflow-hidden whitespace-nowrap styles_MagnetPostCard__title__8g7dy'}).text)
                related_videos_info["producer"] = self.safe_extraction('producer', video.parent, lambda e: e.find('span',{'class','mr-2 text-neutral-400 text-body-2'}).text)
                related_videos_info["producer_link"] = 'https://www.digikala.com' +  self.safe_extraction('producer link', video.parent, lambda e: e.find('a',{'class','styles_Link__RMyqc'})["href"]) 
                related_videos_info["thumbnail"] = self.safe_extraction('thumbnail', video, lambda e: e.find('img',{'class','w-full inline-block'})["src"])
                related_videos.append(related_videos_info)
            self.log.info('[+] related videos extrection succsusfully')
            return related_videos
        else : return []

    def expert_check_box_extrection(self,element):
        
        if isinstance(element ,(Tag, ResultSet)):
            expert_check = []
            for expert in element.find_all('section'):
                expert_check_info = {}
                expert_check_info["titles"] = self.safe_extraction('titles', expert, lambda e: e.find('p',{'class':'grow text-h5 text-neutral-900'}).text)
                expert_check_info["expert_text"] = self.safe_extraction('expert text', expert, lambda e: e.find('p',{'class':'text-body-1 text-neutral-800'}).text)
                if expert_check_info["expert_text"] == '' :
                    expert_check_info["expert_text"] = self.safe_extraction('expert text', expert, lambda e: e.find('img',{'class':'w-full lg:block sm:block xs:block inline-block'})['src'])
                expert_check.append(expert_check_info)
            self.log.info('[+] expert check extrection succsusfully')
            return expert_check
        else :
            return []
        
    def specifications_box_extrection(self,element):
        if isinstance(element ,(Tag, ResultSet)):

            specifications= {}
            for ele in element:
                spec_list = []
                main_title = ele.find('p',{'class':'w-full lg:ml-12 text-h5 text-neutral-700 shrink-0 mb-3 lg:mb-0 styles_SpecificationBox__title__ql60s'}).text
                box = ele.find_all('div',{'class':'w-full flex last styles_SpecificationAttribute__valuesBox__gvZeQ'})
                for i in box : 
                    title = i.find('p',{'class':'ml-4 text-body-1 text-neutral-500 py-2 lg:py-3 lg:p-2 shrink-0 styles_SpecificationAttribute__value__CQ4Rz'}).text
                    speci = i.find_all('p',{'class':'flex items-center w-full text-body-1 text-neutral-900 break-words'})
                    sep = []
                    for item in speci : 
                        sep.append(item.text.replace('\n\n','').replace('\r',''))
                    
                    spec_list.append({self.clean_text(title).replace('\n\n',''):self.clean_text(sep)})
                specifications[main_title] = spec_list
            return specifications
        else : return {}


    

    def reviews_box_extrection(self,element):
        class_combinations_review_title = [
                                            'inline-block  text-caption-strong',  # کلاس‌ها به صورت معمول
                                            'text-neutral-900 text-h5 pb-3',
                                            # کلاس‌ها به صورت معکوس یا با تغییرات دیگر
                                            # هر ترکیب دیگری که ممکن است وجود داشته باشد
                                          ]
        class_combinations_review_dislike = [
                                            'dp-question-dislike',
                                            'pdp-comment-dislike',
                                          ]
        class_combinations_review_like = [
                                            'dp-question-like',
                                            'pdp-comment-like',
                                          ]


        if isinstance(element ,(Tag, ResultSet)):

            review_data = []
            for reivew in element:
                review_info = {}
                review_info["user_rating"] = self.safe_extraction('user rating', reivew, lambda e: e.find('div',{'class':'p-1 rounded-small text-caption-strong text-neutral-000 flex justify-center items-center px-2 bg-rating-4-5 styles_commentRate__main__YKGC5'}).text)            
                review_info["review_date"] = self.safe_extraction('review date', reivew, lambda e: e.find('p',{'class':'text-caption text-neutral-400 inline'}).text)   
                review_info["user_role"]  = self.safe_extraction('review date', reivew, lambda e: e.find('div',{'class':'inline-flex items-center mr-2 Badge_Badge__QIekq Badge_Badge--small__ElV6O px-2 text-caption-strong'}).text) 
                review_info["review_offer"] = self.safe_extraction('review offer', reivew, lambda e: e.find('p',{'class':'text-body-2'}).text)            
                review_info["review_comment"] = self.safe_extraction('review comment', reivew, lambda e: e.find('p',{'class':'text-body-1 text-neutral-900 mb-1 pt-3 break-words'}).text)  
                review_info["review_seller"] = self.safe_extraction('review seller', reivew, lambda e: e.find('p',{'class':'text-caption text-neutral-700 inline'}).text)
                review_info["review_color"] = self.safe_extraction('review color', reivew, lambda e: e.find('div',{'class':'ml-2 inline-block rounded-circle styles_PdpCommentContentFooter__purchasedItem--color__GOLKc'}).parent.text.replace(review_info["review_seller"],''))
                # review_info["review_like"] = self.safe_extraction('review like', reivew, lambda e: e.find('button',{"data-cro-id":"pdp-comment-like"}).text)
                # review_info["review_dislike"] = self.safe_extraction('review dislike', reivew, lambda e: e.find('button',{"data-cro-id":"pdp-comment-dislike"}).text)
                review_feedback = self.safe_extraction('review feedback', reivew, lambda e: e.find_all('div',{"class":"flex items-center pt-2px"}))
                review_info["review_feedback"] = [
                f"{'+' if 'var(--color-icon-rating-4-5)' in feedback.find('svg')['style'] else '-'} {feedback.text.replace('n','')}".replace('\n','')
                for feedback in review_feedback]
                review_info['review_title'] = self.check_with_multi_class_name(reivew,'review title','p','class',class_combinations_review_title)
                review_info['review_like'] = self.check_with_multi_class_name(reivew,'review like','button','data-cro-id',class_combinations_review_like)
                review_info['review_dislike'] = self.check_with_multi_class_name(reivew,'review dislike','button','data-cro-id',class_combinations_review_dislike)
                
                

                review_data.append(review_info)
            self.log.info('[+] review info extrection succsusfully')
            return review_data
        else : return []

    def  question_box_extrection(self,element):
        class_combinations_question_dislike = [
                                            'dp-question-dislike',
                                            'pdp-comment-dislike',
                                          ]
        class_combinations_question_like = [
                                            'dp-question-like',
                                            
                                            'pdp-comment-like',
                                          ]
        if isinstance(element ,(Tag, ResultSet)):

            questions = []
            for quest in element:
                question_info = {}
                question_info["question_title"] = self.safe_extraction('question title', quest, lambda e: e.find('p',{'class':'text-subtitle w-full'}).text)     
                question_info["question_answer"] = self.safe_extraction('question answer', quest, lambda e: e.find('p',{'class':'text-body-1'}).text)
                question_info["answer_user_name"] = self.safe_extraction('answer user name', quest, lambda e: e.find('p',{'class':'text-caption text-neutral-400'}).text)
                question_info["answer_user_role"] = self.safe_extraction('answer user role', quest, lambda e: e.find('p',{'class':'inline-block  text-caption-strong'}).text)
                # question_info["question_like"] = self.safe_extraction('question like', quest, lambda e: e.find('button',{"data-cro-id":"dp-question-like"}).text)
                # question_info["question_dislike"] = self.safe_extraction('question dislike', quest, lambda e: e.find('button',{"data-cro-id":"dp-question-dislike"}).text)
                
                
                
                
                
                        
                question_info["question_like"] = self.check_with_multi_class_name(quest,'question like','button','data-cro-id',class_combinations_question_like)
                question_info["question_dislike"] = self.check_with_multi_class_name(quest,'question dislike','button','data-cro-id',class_combinations_question_dislike)
 
                
                
                questions.append(question_info)
            self.log.info('[+] question info extrection succsusfully')
            return questions
        else : return []

    def also_bought_items_extrection(self,element):
        if isinstance(element ,(Tag, ResultSet)):

            also_bought_items = []
            for item in element :
                also_bought_item_info = {}
                also_bought_item_info["also_bought_item_title"] = self.safe_extraction('also bought item title', item, lambda e: e.find('h3').text)
                
                also_bought_item_info["also_bought_item_image"] = self.safe_extraction('also bought item link', item, lambda e: e.find('img')["src"])
                also_bought_item_info["also_bought_item_link"] = 'https://www.digikala.com'+ self.safe_extraction('also bought item image', item, lambda e: e["href"])

                also_bought_item_info["also_bought_item_final_price"] = self.safe_extraction('also bought item final price', item, lambda e: e.find('span',{"data-testid":"price-final"}).text)
                
                also_bought_item_info["also_bought_item_discount_percent"] = self.safe_extraction('also bought item discount percent', item, lambda e: e.find('span',{"data-testid":"price-no-discount"}).text)
                
                also_bought_item_info["also_bought_item_price_before_discount"] = self.safe_extraction('also bought item price before discount', item, lambda e: e.find('span',{"data-testid":"price-no-discount"}).text)
                also_bought_items.append(also_bought_item_info)
                

            self.log.info('[+] also bought items extrection succsusfully')
            return also_bought_items
        else : return []

    def seller_offer_extrection(self,element):
        if isinstance(element ,(Tag, ResultSet)):

            seller_offers_items = []
            for offer in element:
                seller_offers_info = {}
                seller_offers_info["seller_offers_title"] = self.safe_extraction('seller offers title', offer, lambda e: e.find('h3').text)
                
                seller_offers_info["seller_offers_image"] = self.safe_extraction('seller offers link', offer, lambda e: e.find('img',{'class':'w-full rounded-medium inline-block'})["src"])
                seller_offers_info["seller_offers_link"] = 'https://www.digikala.com'+ self.safe_extraction('seller offers image', offer, lambda e: e["href"])

                seller_offers_info["seller_offers_final_price"] = self.safe_extraction('seller offers final price', offer, lambda e: e.find('span',{"data-testid":"price-final"}).text)
                
                seller_offers_info["seller_offers_discount_percent"] = self.safe_extraction('seller offers discount percent', offer, lambda e: e.find('span',{"data-testid":"price-discount-percent"}).text)
                
                seller_offers_info["seller_offers_price_before_discount"] = self.safe_extraction('seller offers price before discount', offer, lambda e: e.find('span',{"data-testid":"price-no-discount"}).text)
                seller_offers_items.append(seller_offers_info)


            return seller_offers_items
        else : return []

    def page_extrection(self,page_source,prdouct_id):
        # with open('page_source.html','r',encoding='utf-8') as file :
        #     page_source = file.read()

        soup = self.make_soup(page_source)
        elements = self.product_elements_extrection(soup)
        main_product_details = self.clean_text(self.main_product_details_extrection(elements["main_product_details"]))
        buy_box = self.clean_text(self.product_buy_box_extrection(elements["buy_box"]))
        product_images = self.clean_text(self.product_image_extrection(elements["image_box"]))
        other_seller = self.clean_text(self.other_seller_box_extrection(elements["other_seller_box"]))
        similar_products = self.clean_text(self.similar_products_extrection(elements["similar_products"]))
        related_videos = self.clean_text(self.related_videos_extrection(elements["related_videos"]))
        introduction_box = self.clean_text(elements["introduction_box"])
        expert_check = self.clean_text(self.expert_check_box_extrection(elements["expert_check_box"]))
        specifications_box = self.clean_text(self.specifications_box_extrection(elements["specifications_box"]))
        reviews = self.clean_text(self.reviews_box_extrection(elements["reviews_box"]))
        question_box = self.clean_text(self.question_box_extrection(elements["question_box"]))
        also_bought_items = self.clean_text(self.also_bought_items_extrection(elements["also_bought_items"]))
        seller_offer = self.clean_text(self.seller_offer_extrection(elements["seller_offer"]))
        prodcut_info= {}
        
        

        prodcut_info["main_product_details"] = main_product_details
        prodcut_info["buy_box"] = buy_box
        prodcut_info["product_images"] = product_images
        prodcut_info["other_seller"] = other_seller
        prodcut_info["similar_products"] = similar_products
        prodcut_info["related_videos"] = related_videos
        prodcut_info["introduction_box"] = [introduction_box]
        prodcut_info["expert_check"] = expert_check
        prodcut_info["specifications_box"] = specifications_box
        prodcut_info["reviews"] = reviews
        prodcut_info["question_box"] = question_box
        prodcut_info["also_bought_items"] = also_bought_items
        prodcut_info["seller_offer"] = seller_offer
        with open(f'{prdouct_id}.json','w',encoding='utf-8') as info:
            info.write(str(prodcut_info))

    def run(self,url):  
        # load the page -> DONE
        # scroll to fotter back to top -> DONE
        # scroll to the links -> click on them -> DONE
        # get the page suorce code -> DONE

        # start to extract info -> DOING
        # return data -> DOING 

        # store data to the database -> NEXT STEP

        # start next page -> DOING 
         
        page_source = self.load_page(url)
        ids = url.split('/')[4]
        self.page_extrection(page_source,ids)
       

if __name__=="__main__":
    # TODO introduction_box not in the dict need to fix return list or dict 
    geko_path = r'geckodriver.exe'
    product_url = ['https://www.digikala.com/product/dkp-6903697/%D8%AA%D8%A8%D9%84%D8%AA-%D8%A7%D9%BE%D9%84-%D9%85%D8%AF%D9%84-ipad-9th-generation-102-inch-wi-fi-2021-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-64-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA/',
                   'https://www.digikala.com/product/dkp-7857839/%D8%AA%D8%A8%D9%84%D8%AA-%D9%85%D8%A7%DB%8C%DA%A9%D8%B1%D9%88%D8%B3%D8%A7%D9%81%D8%AA-%D9%85%D8%AF%D9%84-surface-pro-8-b-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-128-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA/',
                   'https://www.digikala.com/product/dkp-4170482/%D8%AA%D8%A8%D9%84%D8%AA-%D9%86%D8%A7%D8%B1%D8%AA%D8%A8-%D9%85%D8%AF%D9%84-n28-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-32-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA/',
                   'https://www.digikala.com/product/dkp-10805903/%D8%AA%D8%A8%D9%84%D8%AA-%D9%85%D8%A7%DB%8C%DA%A9%D8%B1%D9%88%D8%B3%D8%A7%D9%81%D8%AA-%D9%85%D8%AF%D9%84-surface-pro-8-i5-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-256-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D9%88-8-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D8%B1%D9%85-%D8%A8%D9%87-%D9%87%D9%85%D8%B1%D8%A7%D9%87-%DA%A9%DB%8C%D8%A8%D9%88%D8%B1%D8%AF-black-type-signature-%D9%88-%D9%82%D9%84%D9%85-surface-slim-pen-2/',
                   'https://www.digikala.com/product/dkp-7290673/%D8%AA%D8%A8%D9%84%D8%AA-%D8%A7%D9%BE%D9%84-%D9%85%D8%AF%D9%84-ipad-9th-generation-102-inch-wi-fi-2021-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-256-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA/',
                   'https://www.digikala.com/product/dkp-2887055/%D8%AA%D8%A8%D9%84%D8%AA-%D9%84%D9%86%D9%88%D9%88-%D9%85%D8%AF%D9%84-tab-m7-7305x-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-32-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA/',
                   'https://www.digikala.com/product/dkp-12995544/%D9%84%D9%BE-%D8%AA%D8%A7%D9%BE-156-%D8%A7%DB%8C%D9%86%DA%86%DB%8C-%D8%A7%DB%8C%D8%B3%D9%88%D8%B3-%D9%85%D8%AF%D9%84-vivobook-15-oled-k513eq-l1789-i7-16gb-512ssd-mx350/',
                   'https://www.digikala.com/product/dkp-12216094/%D9%84%D9%BE-%D8%AA%D8%A7%D9%BE-18-%D8%A7%DB%8C%D9%86%DA%86%DB%8C-%D8%A7%DB%8C%D8%B3%D9%88%D8%B3-%D9%85%D8%AF%D9%84-rog-strix-scar-18-g834jy-n5049-i9-64gb-1ssd-rtx4090-%DA%A9%D8%A7%D8%B3%D8%AA%D9%88%D9%85-%D8%B4%D8%AF%D9%87-clone-1-of-12216081/',
                   'https://www.digikala.com/product/dkp-11476991/%D9%84%D9%BE-%D8%AA%D8%A7%D9%BE-156-%D8%A7%DB%8C%D9%86%DA%86%DB%8C-%D8%A7%DB%8C%D8%B3%D9%88%D8%B3-%D9%85%D8%AF%D9%84-tuf-gaming-f15-fx506hf-hn014-i5-16gb-512ssd-rtx-2050-%DA%A9%D8%A7%D8%B3%D8%AA%D9%88%D9%85-%D8%B4%D8%AF%D9%87/',
                   'https://www.digikala.com/product/dkp-7474479/%D9%84%D9%BE-%D8%AA%D8%A7%D9%BE-14-%D8%A7%DB%8C%D9%86%DA%86%DB%8C-%D8%A7%DB%8C%D8%B3%D9%88%D8%B3-%D9%85%D8%AF%D9%84-m433ua-eb406/',
                   'https://www.digikala.com/product/dkp-11675167/%D9%84%D9%BE-%D8%AA%D8%A7%D9%BE-156-%D8%A7%DB%8C%D9%86%DA%86%DB%8C-%D8%A7%DB%8C%D8%B3%D9%88%D8%B3-%D9%85%D8%AF%D9%84-creator-q-q540vj-i93050-i9-13900h-16gb-1ssd-rtx3050/',
                   'https://www.digikala.com/product/dkp-11274885/%D9%84%D9%BE-%D8%AA%D8%A7%D9%BE-16-%D8%A7%DB%8C%D9%86%DA%86%DB%8C-%D8%A7%DB%8C%D8%B3%D9%88%D8%B3-%D9%85%D8%AF%D9%84-rog-strix-g16-g614jv-as73/',
                   'https://www.digikala.com/product/dkp-10004069/%D9%84%D9%BE-%D8%AA%D8%A7%D9%BE-156-%D8%A7%DB%8C%D9%86%DA%86%DB%8C-%D8%A7%DB%8C%D8%B3%D9%88%D8%B3-%D9%85%D8%AF%D9%84-vivobook-r1502za-bq558/',\
                   'https://www.digikala.com/product/dkp-10659378/%D9%84%D9%BE-%D8%AA%D8%A7%D9%BE-156-%D8%A7%DB%8C%D9%86%DA%86%DB%8C-%D8%A7%DB%8C%D8%B3%D9%88%D8%B3-%D9%85%D8%AF%D9%84-tuf-gaming-f15-fx506hc-i5-16gb-512gb-3050-w11-%DA%A9%D8%A7%D8%B3%D8%AA%D9%88%D9%85-%D8%B4%D8%AF%D9%87/',
                   'https://www.digikala.com/product/dkp-12019914/%D9%84%D9%BE-%D8%AA%D8%A7%D9%BE-156-%D8%A7%DB%8C%D9%86%DA%86%DB%8C-%D8%A7%DB%8C%D8%B3%D9%88%D8%B3-%D9%85%D8%AF%D9%84-q530vj/',
                   'https://www.digikala.com/product/dkp-12405561/%D9%84%D9%BE-%D8%AA%D8%A7%D9%BE-133-%D8%A7%DB%8C%D9%86%DA%86%DB%8C-%D8%A7%DB%8C%D8%B3%D9%88%D8%B3-%D9%85%D8%AF%D9%84-zenbook-s-13-oled-ux5304va-nq003/',
                   'https://www.digikala.com/product/dkp-12656284/%D9%84%D9%BE-%D8%AA%D8%A7%D9%BE-145-%D8%A7%DB%8C%D9%86%DA%86%DB%8C-%D8%A7%DB%8C%D8%B3%D9%88%D8%B3-%D9%85%D8%AF%D9%84-zenbook-14x-oled-q410va-i5-8gb-512ssd/',
                   'https://www.digikala.com/product/dkp-12438500/%D9%84%D9%BE-%D8%AA%D8%A7%D9%BE-145-%D8%A7%DB%8C%D9%86%DA%86%DB%8C-%D8%A7%DB%8C%D8%B3%D9%88%D8%B3-%D9%85%D8%AF%D9%84-zenbook-pro-duo-14-ux8402ze-m3026w-clone-1-of-9943357/',
                   'https://www.digikala.com/product/dkp-12956692/%D9%84%D9%BE-%D8%AA%D8%A7%D9%BE-156-%D8%A7%DB%8C%D9%86%DA%86%DB%8C-%D8%A7%DB%8C%D8%B3%D9%88%D8%B3-%D9%85%D8%AF%D9%84-x515ep-ej743-i7-16gb-1ssd-mx330/',
                   'https://www.digikala.com/product/dkp-9210719/%D9%84%D9%BE-%D8%AA%D8%A7%D9%BE-134-%D8%A7%DB%8C%D9%86%DA%86%DB%8C-%D8%A7%DB%8C%D8%B3%D9%88%D8%B3-%D9%85%D8%AF%D9%84-rog-flow-z13-gz301ze-a/',
                   ]
    scraper = product_extrection(geko_path,)
    for link in product_url:
        scraper.run(link)


