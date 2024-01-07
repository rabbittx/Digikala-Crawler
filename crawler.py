from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import sqlite3

class WebScraper:
    
    def __init__(self, driver_path, base_seller):
        self.driver = self.initialize_driver(driver_path)
        self.base_seller = base_seller
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

    def close_resources(self):
        self.conn.commit()
        self.conn.close()
        self.driver.quit()

    def run(self):
        for seller in self.base_seller:
            url = f'https://www.digikala.com/seller/{seller}/'
            page_data = self.scan(self.get_seller_source_page(url))
            page_data[0]['seller_id'] = seller
            self.save_to_database(page_data)
        self.close_resources()

if __name__== "__main__":
    geko_path = r'geckodriver.exe'
    base_seller = ["a9h3m",'cajwj','cgxgh','cwe4n','cskc4','f7k6y','5ajh7']
    scraper = WebScraper(geko_path, base_seller)
    scraper.run()
