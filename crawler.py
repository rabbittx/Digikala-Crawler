from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from bs4 import BeautifulSoup
import sqlite3 ,time 
from time import gmtime, strftime
from logger import setup_logger
from driver_manager import DriverManager
from db_handler import DataBaseHandler
import json

class WebScraper:
    
    def __init__(self, driver_path ,db_path):
        self.log = setup_logger()
        self.driver = DriverManager(self.log,driver_path)
        self.db_handler = DataBaseHandler(db_path,self.log)

    def has_desired_text(self,tags,find_text):
        for element in tags:
            if find_text in element.text :
                return element

    def seller_details(self,soup):
        self.log.info('start to ectrext seller details')
        return { 'crawl_date' : strftime("%Y-%m-%d %H:%M:%S", gmtime()),
                'seller_name':soup.find('h1',{'class':'text-h5 text-neutral-900 whitespace-nowrap'}).text,
                'membership_period':soup.find('div',{'class':'w-full flex flex-col mr-5'}).find('p',{'class':'text-body-2'}).text,
                'satisfaction_with_goods':soup.find('p',string='رضایت از کالاها').find_parent('div').find('p').text,
                'seller_performance':soup.find('p',string='عملکرد فروشنده').find_parent('div').find('p').text,
                'people_have_given_points':self.has_desired_text(soup.find_all('p',),'نفر امتیاز داده‌اند').string.replace('نفر امتیاز داده‌اند','') if self.has_desired_text(soup.find_all('p',),'نفر امتیاز داده‌اند') else ' Uncertain number of votes',
                'timely_supply':soup.find('p', string='تامین به موقع').find_previous_sibling('p').string,
                'obligation_to_send':soup.find('p', string='تعهد ارسال').find_previous_sibling('p').string,
                'no_return':soup.find('p', string='بدون مرجوعی').find_previous_sibling('p').string,
                'introduction_of_the_seller':soup.find('span',string='معرفی فروشنده').find_parent('div').find_parent('div').find_next_sibling('div').text if soup.find('span',string='معرفی فروشنده') else ' info unavailable ',
            }
    
    def extract_product_details(self,product):
        try :
            img_element = product.find('picture').find('img', {'class': 'w-full rounded-medium inline-block'})
        except Exception as e :
            self.log.error(f'Error during find product picture {e}')
        try :
            rate_element = product.find('div',{'class':'mb-1 flex items-center justify-between'}).find('p',{'class':'text-body2-strong text-neutral-700'})
        except Exception as e : 
            self.log.error(f'Error during find product rate {e}')
        try : 
            price_element = product.find('span',{'data-testid':'price-final'})
        except Exception as e : 
            self.log.error(f'Error during find product price {e}')
        try :
            price_discount_percent_element = product.find('span',{'data-testid':'price-discount-percent'})
        except Exception as e : 
            self.log.error(f'Error during find product price discount percent {e}')
        try :    
            element_price_discount = product.find('div',{'data-testid':'price-no-discount'})
        except Exception as e :
            self.log.error(f'Error during find product price discount {e}')
        try:
            product_special_sale = 'special sale' if 'SpecialSell.svg' in (product.find('div', {'class': 'flex items-center justify-start mb-1'}).find('img').get('src', '')) else 'unavailable special sale'
        except AttributeError:
            product_special_sale = 'unavailable special sale'
    
        return {
            'crawl_date' : strftime("%Y-%m-%d %H:%M:%S", gmtime())  ,
            'product_id':product.find('a')['href'].split('/')[2],
            'product_link': "https://www.digikala.com"+product.find('a')['href'],
            'product_image':img_element['src'] if img_element else 'image not found' ,
            'product_rate':rate_element.text if rate_element else 'rate not found',
            'product_name':product.find('h3').text,
            'product_price':price_element.text.replace(',','') if price_element else "product unavailable",
            'product_price_discount_percent':price_discount_percent_element.text if price_discount_percent_element else "unavailable discount percent",
            'product_price_discount':element_price_discount.text if element_price_discount else "unavailable discount price" ,
            'product_special_sale':product_special_sale,
            'stock':self.has_desired_text(product.find('p'),'باقی مانده').replace('تنها ','').replace(' عدد در انبار باقی مانده','') if self.has_desired_text(product.find('p'),'باقی مانده') else 'Quantity unspecified',
        }

    def scan(self,page_source):
        soup = BeautifulSoup(page_source,'html.parser')
        return self.seller_details(soup),[self.extract_product_details(product) for product in soup.find_all('div', {'class':'product-list_ProductList__item__LiiNI'})]
   

    def get_product(self,page_source):
        try:
            soup = BeautifulSoup(page_source,'html.parser')
            product_element_link = soup.find_all('a',{'class':'block cursor-pointer relative bg-neutral-000 overflow-hidden grow py-3 px-4 lg:px-2 h-full styles_VerticalProductCard--hover__ud7aD'})
            product_link = []
            for element in product_element_link:
                link = 'https://www.digikala.com' + element['href']
                if link not in product_link:
                    product_link.append(link)
            self.log.info(f'Found {len(product_link)} product links')
            return product_link
        except Exception as e:
            self.log.error(f'Error while extracting product links: {e}')
            raise
    
    def run_category(self,category_url,scroll_count):
        try :
            self.log.info('Starting scraper run for category ...')
            page_source = self.driver.scan_product_category_page(category_url,scroll_count)
            product_link = self.get_product(page_source)
            base_seller_id = self.driver.find_seller_ids(product_link)
            for seller in base_seller_id:
                url = f'https://www.digikala.com/seller/{seller}/' 
                page_data = self.scan(self.driver.get_seller_source_page(url))
                page_data[0]['seller_id'] = seller
                self.run(page_data)
            self.log.info('Scraper run completed successfully')
        except Exception as e:
            self.log.error(f'Error during scraper run: {e}')
            raise
    
    def run_single(self,seller_url):
        try :
            self.log.info('Starting scraper run for single seller ...')
            page_data = self.scan(self.driver.get_seller_source_page(seller_url))
            page_data[0]['seller_id'] = seller_url.split('/')[-2]
            print(page_data)
            self.db_handler.run(page_data)
            self.log.info('Scraper run completed successfully')
        except Exception as e:
            self.log.error(f'Error during scraper run: {e}')
            raise

    def open_category_page(self,url):
        self.driver.get(url)
        time.sleep(3) #wait until the page is loaded
        self.driver.scan_product_category_page(scroll_count=5)


    def check_category(self,url,scroll_count):
        self.driver.open_page(url)
        self.driver.scroll_page(scroll_count)
        page_source = self.driver.get_page_source()
        prodcut_links = self.driver.get_prdoucts_on_page(page_source,return_value='products_link')
        sellers_id = []
        for link in prodcut_links:
            self.driver.open_page(link)
            seller_id = self.driver.get_seller_id()
            if seller_id not in sellers_id and seller_id != None:
                sellers_id.append(seller_id)
        for seller in sellers_id:
            seller_link = f'https://www.digikala.com/seller/{seller}'
            self.log.info(f'[!] try to open seller page with id=[{seller}]')
            self.driver.open_page(seller_link)
            self.driver.scroll_page(scroll_count=True)
            self.driver.click_on_element_by_xpath("//p[text()='جزئیات بیشتر']/..")
            seller_page_source_code = self.driver.get_page_source()
            seller_info = self.seller_details(seller_page_source_code)
            seller_info['seller_id'] = seller
            self.db_handler.run(data=seller_info,column_name='seller_id',table_name='sellers')
            self.driver.click_on_element_by_xpath("//div[@role='dialog']//div[@class='flex cursor-pointer']")
            product_elements = self.driver.get_prdoucts_on_page(seller_page_source_code,return_value='products_element')
            for product in product_elements:
                product_info = self.extract_product_details(product)
                product_info['seller_name'] = seller_info['seller_name']
                self.db_handler.run(data=product_info,column_name='product_id',table_name='products')
        
    def check_seller(self,url):
        pass


# new_run => (category_url/seller_url):
        # if input category_url -> 
            # open page -> 
                # extrect products ->
                    # open products page ->
                        # extrect seller info -> 
                            # open seller page ->
                                # extrect seller data -> store seller data to table 
        # if input seller_url -->
            # open seller page -->
                # extrect seller info -->
                    # store data to table 
        


if __name__== "__main__":
    # TODO replace time.sleep with WebDriverWait -> (TODO)
    # TODO error handling -> (testing)
    # TODO historical data -> (DONE) 
    # TODO extract the full data of product -> (TODO)
    # TODO add testing unit -> (TODO)
    # TODO add flask GUI -> (TODO) 
    # TODO add API endpoint -> (TODO) 
    # TODO add data analysis -> (TODO)
    
    
    geko_path = r'geckodriver.exe'
    db_path = r'digikala.db'
    category_url = 'https://www.digikala.com/search/category-notebook-netbook-ultrabook/asus/'
    scraper = WebScraper(driver_path=geko_path,db_path=db_path)
    scraper.check_category(category_url,0)
