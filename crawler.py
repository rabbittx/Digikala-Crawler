from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import sqlite3

class WebScraper:
    
    def __init__(self, driver_path, category_url):
        self.driver = self.initialize_driver(driver_path)
        self.category_url = category_url
        self.conn = sqlite3.connect('seller_data.db')
        self.cursor = self.conn.cursor()
        
    def initialize_driver(self, driver_path):
        service = Service(driver_path)
        return webdriver.Firefox(service=service)
    
    def has_desired_text(self,tags,find_text):
        for element in tags:
            if find_text in element.text :
                return element

    def get_seller_source_page(self, url):
        self.driver.get(url)
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
        details_elemnt = self.driver.find_element(By.XPATH,"//p[text()='جزئیات بیشتر']/..")
        time.sleep(1)
        details_elemnt.click()
        return self.driver.page_source

    def seller_details(self,soup):
        return {
                'seller_name':soup.find('h1',{'class':'text-h5 text-neutral-900 whitespace-nowrap'}).text,
                'membership_period':soup.find('div',{'class':'w-full flex flex-col mr-5'}).find('p',{'class':'text-body-2'}).text,
                'satisfaction_with_goods':soup.find('p',string='رضایت از کالاها').find_parent('div').find('p').text,
                'seller_performance':soup.find('p',string='عملکرد فروشنده').find_parent('div').find('p').text,
                'people_have_given_points':self.has_desired_text(soup.find_all('p',),'نفر امتیاز داده‌اند').string.replace('نفر امتیاز داده‌اند',''),
                'timely_supply':soup.find('p', string='تامین به موقع').find_previous_sibling('p').string,
                'obligation_to_send':soup.find('p', string='تعهد ارسال').find_previous_sibling('p').string,
                'no_return':soup.find('p', string='بدون مرجوعی').find_previous_sibling('p').string,
                'introduction_of_the_seller':soup.find('span',string='معرفی فروشنده').find_parent('div').find_parent('div').find_next_sibling('div').text if soup.find('span',string='معرفی فروشنده') else 'info unavailable ',
            }
    
    def extract_product_details(self,product):
        img_element = product.find('picture').find('img', {'class': 'w-full rounded-medium inline-block'})
        rate_element = product.find('div',{'class':'mb-1 flex items-center justify-between'}).find('p',{'class':'text-body2-strong text-neutral-700'})
        price_element = product.find('span',{'data-testid':'price-final'})
        price_discount_percent_element = product.find('span',{'data-testid':'price-discount-percent'})
        element_price_discount = product.find('div',{'data-testid':'price-no-discount'})
        try:
            product_special_sale = 'special sale' if 'SpecialSell.svg' in (product.find('div', {'class': 'flex items-center justify-start mb-1'}).find('img').get('src', '')) else 'unavailable special sale'
        except AttributeError:
            product_special_sale = 'unavailable special sale'
        return {
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
   
    def update_or_insert_seller(self, seller_data):
        self.cursor.execute('''
            INSERT INTO sellers (seller_id, seller_name, membership_period, satisfaction_with_goods, seller_performance, people_have_given_points, timely_supply, obligation_to_send, no_return, introduction_of_the_seller)
            VALUES (:seller_id, :seller_name, :membership_period, :satisfaction_with_goods, :seller_performance, :people_have_given_points, :timely_supply, :obligation_to_send, :no_return, :introduction_of_the_seller)
            ON CONFLICT(seller_id) DO UPDATE SET
            seller_name = excluded.seller_name,
            membership_period = excluded.membership_period,
            satisfaction_with_goods = excluded.satisfaction_with_goods,
            seller_performance = excluded.seller_performance,
            people_have_given_points = excluded.people_have_given_points,
            timely_supply = excluded.timely_supply,
            obligation_to_send = excluded.obligation_to_send,
            no_return = excluded.no_return,
            introduction_of_the_seller = excluded.introduction_of_the_seller
            ''', seller_data)

    def update_or_insert_product(self, product_data):
        self.cursor.execute('''
            INSERT INTO products (seller_name, product_id, product_link, product_image, product_rate, product_name, product_price, product_price_discount_percent, product_price_discount, product_special_sale, stock)
            VALUES (:seller_name, :product_id, :product_link, :product_image, :product_rate, :product_name, :product_price, :product_price_discount_percent, :product_price_discount, :product_special_sale, :stock)
            ON CONFLICT(product_id) DO UPDATE SET
            seller_name = excluded.seller_name,
            product_link = excluded.product_link,
            product_image = excluded.product_image,
            product_rate = excluded.product_rate,
            product_name = excluded.product_name,
            product_price = excluded.product_price,
            product_price_discount_percent = excluded.product_price_discount_percent,
            product_price_discount = excluded.product_price_discount,
            product_special_sale = excluded.product_special_sale,
            stock = excluded.stock
            ''', product_data)

    def save_to_database(self,  data):
        self.update_or_insert_seller(data[0])
        for product in data[1]:
            product['seller_name'] = data[0]['seller_name']
            self.update_or_insert_product(product)


    def scan_product_category_page(self,url):
        
        self.driver.get(url)
        time.sleep(5)
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        for _ in range(2): # set range to 5 , 15 , 30 fast , normal , long
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        time.sleep(1)
        return self.driver.page_source

    def get_product(self,page_source):
        soup = BeautifulSoup(page_source,'html.parser')
        product_element_link = soup.find_all('a',{'class':'block cursor-pointer relative bg-neutral-000 overflow-hidden grow py-3 px-4 lg:px-2 h-full styles_VerticalProductCard--hover__ud7aD'})
        product_link = []
        for element in product_element_link:
            link = 'https://www.digikala.com' + element['href']
            if link not in product_link:
                product_link.append(link)
        return product_link

    def find_seller_ids(self,product_link):
        seller_ids = []
        for link in product_link:
            self.driver.get(link)
            time.sleep(5)
            div_element = self.driver.find_element(By.XPATH, '//div[@class="flex flex-col lg:mr-3 lg:mb-3 lg:gap-y-2 styles_InfoSection__buyBoxContainer__3nOwP"]')
            link_element = div_element.find_element(By.XPATH, './/a[@class="styles_Link__RMyqc"]')
            href_value = link_element.get_attribute('href').split('/')[-2]
            if href_value not in seller_ids:
                seller_ids.append(href_value)
        return seller_ids
    
    def close_resources(self):
        self.conn.commit()
        self.conn.close()
        self.driver.quit()

    def run(self):
        page_source = self.scan_product_category_page(self.category_url)
        product_link = self.get_product(page_source)
        base_seller_id = self.find_seller_ids(product_link)
        for seller in base_seller_id:
            url = f'https://www.digikala.com/seller/{seller}/'
            page_data = self.scan(self.get_seller_source_page(url))
            page_data[0]['seller_id'] = seller
            self.save_to_database(page_data)
        self.close_resources()

if __name__== "__main__":
    # TODO adding loggin 
    # TODO create panle 
    # TODO 
    geko_path = r'geckodriver.exe'
    category_url = 'https://www.digikala.com/search/category-notebook-netbook-ultrabook/asus/'
    scraper = WebScraper(geko_path,category_url)
    scraper.run()
