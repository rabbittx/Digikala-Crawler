from seller_product_data_extractor import SellerProductDataExtractor
import csv  , os ,re
from logger import setup_logger
from driver_manager import DriverManager
from db_handler import DataBaseHandler
from product_details_extractor import ProductDetailsExtractor
import os
import configparser

class ConfigManager:
    def __init__(self, config_file='config.ini'):
        self.config_file = config_file
        self.config = configparser.ConfigParser()

        if not self.config.read(self.config_file):
            self._create_default_config()

    def _create_default_config(self):
        self.config['Paths'] = {'GeckoPath': input('Enter path of Gecko driver (eq:path/to/geckodriver.exe): '), 'DBPath': input('Enter path to database (eq:path/to/database.db) :')}

        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def get_gecko_path(self):
        return self.config.get('Paths', 'GeckoPath')

    def get_db_path(self):
        return self.config.get('Paths', 'DBPath')

    def set_gecko_path(self, path):
        self.config.set('Paths', 'GeckoPath', path)
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def set_db_path(self, path):
        self.config.set('Paths', 'DBPath', path)
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

class WebScraperPanel:
    def __init__(self,driver_path,db_path,log ):
        self.log = log
        self.db_path = db_path
        self.driver_path = driver_path
        self.db_handler = DataBaseHandler(db_path,log=self.log)
        self.db_handler.create_tables()
        self.scroll_count = 3
    def get_driver(self):
        self.log.info('[-] in need headless browser  ? Enter yes / y / No / n')
        headless = input('enter option headless (yes / y / No / n) :').lower()
        if headless in ['yes', 'y']:
            headless_mode = True
            self.log.info('[!] browser set to headless [!] (it will work on background)')
        else :
            headless_mode = False
            self.log.info('[!] browser will open soon [!] (headless browser set to False )')
        if not hasattr(self, '_driver'):
            self._driver = DriverManager(driver_path=self.driver_path, log=self.log,headless_mode=headless_mode)
            self.webscraper = SellerProductDataExtractor(driver=self.get_driver(),db_handler=self.db_handler,log=log)
            self.product_extraction_scraper = ProductDetailsExtractor(db_handler=self.db_handler,driver=self.get_driver(),log=self.log)
        return self._driver
    
    def display_menu(self):
        self.log.info("----------- welcome to digikala web crawler -------------")
        self.log.info("1) start to crawl for category .")
        self.log.info("2) start to crawl for single seller .")
        self.log.info("3) start to crawl single seller product with all specifications .")
        self.log.info("4) start crawl single product with all specifications .")
        self.log.info("5) start crawl all products on database with all specifications .")
        self.log.info("6) CSV export menu .")
        self.log.info("7) check data in database .")
        self.log.info("8) quit .")
        user_pick = input("enter your choose : ")
        return user_pick
    
    def get_url_input(self, mode):
            while True:
                fmode = mode.replace('_',' ')
                if mode == 'single_product':
                    self.log.info(f'[-] enter the url of {fmode} you want to crawle with it id .')
                    self.log.info('[-] Example : https://www.digikala.com/product/dkp-11194944')
                elif mode == 'single_seller':
                    self.log.info(f'enter the url of {fmode} you want to crawle with it id .')
                    self.log.info('[-] Example : https://www.digikala.com/seller/6xwus/')
                elif mode == 'category':
                    self.log.info(f'enter the url of {fmode} you want to crawle .')
                    self.log.info('[-] Example : https://www.digikala.com/search/?q=iphone')
                    self.log.info('[-] Example : https://www.digikala.com/search/category-mobile-phone/xiaomi/')
                    self.log.info('[-] Example : https://www.digikala.com/search/')

                url = input(f'Enter {fmode} URL : ')
                if  url == 'exit' :
                    self.start() 
                    break
                if mode == 'single_product':
                    if ('product' not in url and not re.search(r'https://www\.digikala\.com/product/dkp-\d+/$', url) ):
                        self.log.warning('[!] URL is not belong to any product check it and Please try again.')
                        continue
                elif mode == 'single_seller':
                    pattern = re.compile(r'https://www\.digikala\.com/seller/[A-Za-z0-9]+/$')
                    if  (not pattern.match(url)):
                        self.log.warning("[!] URL is not belong to any seller check it and Please try again.")
                        continue
                elif mode == 'category':
                    pattern = re.compile(r'search/\?q=|/category-|/search/')
                    if not ('search/?q=' in url or '/category-' in url or '/search/' in url):
                        self.log.warning('[!] Wrong category URL, try one more time')
                    self.scroll_count = input("Please enter the number of page scroll rates (Example 5 ) : ")
                    try:
                        self.scroll_count = int(self.scroll_count)
                    except ValueError:
                        self.log.error("[!] ERROR - The number of scrolling times must be a number. By default, it is set to 3.")
                        continue
                break
            return url
    
    def show_sllers(self):
        row_info = self.db_handler.get_row_info(fields=['seller_id', 'seller_name'], table_name='sellers',condition=None,return_as_list=False)
        if len(row_info) == 0 :
            self.log.warning("[!] Warning: There are no sellers in the database.")
            return None
        for index, row in enumerate(row_info):
            self.log.info(f"[-] ID {index} : {row[0]}, Name: {row[1]}")
        while True:
            try:
                self.log.info('[-] to exit the option enter  "exit"')

                user_pick = input('choose the seller ID you want to crawl products from: ')
                if  user_pick == 'exit': self.start()
                elif 0 <= int(user_pick) < len(row_info):
                    break
                else:
                    self.log.error('[!] Error: Invalid option, please try again.')
            except ValueError:
                self.log.error('[!] Error: Invalid input , please try again with number.')
        return row_info[int(user_pick)]

    def unified_scraper(self, mode):
        url = None
        self.log.info('[-] to exit the option enter  "exit"')
        if mode in ['single_product', 'single_seller', 'category']:
            url = self.get_url_input(mode)
        if mode == 'seller_products' :
            selected_seller = self.show_sllers()


        self.get_driver()
            
        if mode == 'all_products':
            seller_products = self.db_handler.get_row_info(['product_link', 'product_price'], 'products')
            available_products = [product[0] for product in seller_products if product[1] != 'product unavailable']
            self.log.info(f'[-] {len(available_products)} available products found on database ')
            for index, link in enumerate(available_products):
                self.log.info(f'[-] Starting to crawl - {index + 1}/{len(available_products)}')
                self.product_extraction_scraper.run(link)
                
        elif mode == 'single_product':
            self.log.info(f'[-] Starting to crawl - {url.split("/")[4]}')
            self.product_extraction_scraper.run(url)

        elif mode == 'seller_products':
            
            self.log.info(f'[-] You chose {selected_seller[1]} with ID {selected_seller[0]}')    
            seller_products = self.db_handler.get_row_info(['product_link', 'product_price'], 'products', ['seller_name', selected_seller[1]])
            available_products = [product[0] for product in seller_products if product[1] != 'product unavailable']
            self.log.info(f'{len(available_products)} available products found for {selected_seller[1]}')
            for index, link in enumerate(available_products):
                self.log.info(f'[-] Starting to crawl - {index + 1}/{len(available_products)}')
                self.product_extraction_scraper.run(link)

        elif mode == 'single_seller':
            self.webscraper.check_seller(url)
            self.log.info("[-] Data extraction was done successfully.")
            
        elif mode == 'category':
            self.webscraper.check_category(url,self.scroll_count)
            self.log.info("[-] Data extraction was done successfully.")  
            
        else:
            raise ValueError("[!] Invalid mode selected")

    def export_table_to_csv(self,):
        def remove_old_file(filename):
            if os.path.exists(filename):
                os.remove(filename)
                self.log.info(f'[-] {filename} remove successfully')

        def save_to_csv(data, headers, filename):
            with open(filename, mode='w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                writer.writerows(data)
            self.log.info(f'[-] {filename} export successfully')

        def export_to_csv(table_name,seller_id=None,condition=None):
            csv_file_name = f'{table_name}'
            if seller_id != None :
                csv_file_name = f'{seller_id}-{table_name}'
            remove_old_file(f'{csv_file_name}-database.csv')
            data = self.db_handler.get_row_info(['*'],table_name,condition)
            headers = self.db_handler.get_column_names(table_name)
            save_to_csv(data, headers, f'{csv_file_name}-database.csv')      
        
        if os.path.exists(self.db_path):
            self.log.info('----------- CSV export menu ---------')
            self.log.info('Choose the data you wish to export .')
            self.log.info('1) export sellers table data .')
            self.log.info('2) export seller\'s products data with ID .')
            self.log.info('3) export all seller products table .')
            self.log.info('4) export single seller\'s product information with all specifications .')
            self.log.info('5) export all seller\'s products with all specifications .')
            self.log.info('6) export all table data .')
            self.log.info('7) back to crawler menu .')
            choose = input('Select the option you need : ')

            if choose == '1':
                export_to_csv('sellers',seller_id=None,condition=None)
            elif choose == '2' :            
                selected_seller = self.show_sllers()
                export_to_csv('products',selected_seller[0],['seller_name', selected_seller[1]])
            elif choose == '3':
                export_to_csv('products',seller_id=None)
            elif choose == '4':

                selected_seller = self.show_sllers()
                export_to_csv('products_extraction',selected_seller[0],['seller_name', selected_seller[1]])
            elif choose == '5':
                export_to_csv('products_extraction',seller_id=None)
            elif choose == '6':
                export_to_csv('sellers',seller_id=None)
                export_to_csv('products',seller_id=None)
                export_to_csv('products_extraction',seller_id=None)
            elif choose == '7':
                pass
        else :
            self.log.error(f'[!] ERROR - database at {self.db_path} not found !. check database path .')    

    def database_report(self):
        seller_count = len(self.db_handler.get_row_info(fields='*',table_name='sellers',condition=None,return_as_list=True))
        product_count = len(self.db_handler.get_row_info(fields='*',table_name='products',condition=None,return_as_list=True))
        products_extrection_count = len(self.db_handler.get_row_info(fields='*',table_name='products_extraction',condition=None,return_as_list=True))
        seller_historical_count = len(self.db_handler.get_row_info(fields='*',table_name='sellers_history',condition=None,return_as_list=True))
        products_historical_count = len(self.db_handler.get_row_info(fields='*',table_name='products_history',condition=None,return_as_list=True))
        products_extrection_historical_count = len(self.db_handler.get_row_info(fields='*',table_name='products_extraction_history',condition=None,return_as_list=True))
        self.log.info(f"==================== DATABASE TABLES INFO ==================")
        self.log.info(f"[-] {seller_count} sellers in the table.")
        self.log.info(f"[-] {product_count} products in the table.")
        self.log.info(f"[-] {products_extrection_count} products with all specifications in the table.")
        self.log.info(f"[-] {seller_historical_count} historical sellers in the table.")
        self.log.info(f"[-] {products_historical_count} historical products in the table.")
        self.log.info(f"[-] {products_extrection_historical_count} products with all specifications in the historical table.")
        self.log.info(f"==================== DATABASE TABLES INFO ==================")          

    def start(self):
        while True:
            choose = self.display_menu()
            if choose == "1":
                self.unified_scraper('category')
            elif choose == "2" :
                self.unified_scraper('single_seller')
            elif choose == "3" :
                self.unified_scraper('seller_products')
            elif choose == "4" :
                self.unified_scraper('single_product')
            elif choose == "5" :
                self.unified_scraper('all_products')
            elif choose == "6":
               self.export_table_to_csv()
               self.log.info('[-] CSV file created successfully')
            elif choose == "7":
                self.database_report()
            elif choose == "8":
                if hasattr(self, '_driver'):
                    self._driver.close_driver()
                self.log.info("[-] Exit the program.")
                break
            else:
                self.log.error("[!] ERROR - Invalid option, please try again.")
    
if __name__ == "__main__":
    # TODO add testing unit -> (TODO)
    # TODO add flask GUI -> (TODO) 
    # TODO add API endpoint -> (TODO) 
    # TODO add data analysis -> (TODO)
    # TODO  add seller category field to sellers table (TODO) 

    # BUG : when exit option and try to exit the crawler it run get_driver() - get scroll for category 
    log = setup_logger()
    config_manager = ConfigManager()

    WebScraperPanel(driver_path=config_manager.get_gecko_path(), db_path=config_manager.get_db_path(), log=log).start()

