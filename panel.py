from seller_product_data_extractor import SellerProductDataExtractor
import csv  , os ,re
from logger import setup_logger
from driver_manager import DriverManager
from db_handler import DataBaseHandler
from product_details_extractor import ProductDetailsExtractor
class WebScraperPanel:
    def __init__(self,driver_path,db_path,log ):
        self.log = log
        self.db_path = db_path
        self.driver_path = driver_path
        self.db_handler = DataBaseHandler(db_path,log=self.log)
        self.db_handler.create_tables()

    def get_driver(self):
        if not hasattr(self, '_driver'):
            self._driver = DriverManager(driver_path=self.driver_path, log=self.log)
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

    def run_scraper_category(self):
        while True :
            category_url = input("enter category url to crawl: ")
            print(category_url)
            if 'search/?q=' in category_url or '/category-' in category_url or '/search/' in category_url:
                break
            else:
                self.log.info('wrong category url, try one more time')       
        scroll_count = input("Please enter the number of page scroll rates (Example 5 ) : ")
        try:
            scroll_count = int(scroll_count)
        except ValueError:
            self.log.error("The number of scrolling times must be a number. By default, it is set to 3.")
            scroll_count = 3
        self.webscraper.check_category(category_url,scroll_count)
        self.log.info("Data extraction was done successfully.")

    def run_scraper_single(self):
        seller_page_url = input("enter seller page url to crawl: ")
        self.webscraper.check_seller(seller_page_url)
        self.log.info("Data extraction was done successfully.")

    def run_seller_scraper_product(self):
        row_info = self.db_handler.get_row_info(fields=['seller_id', 'seller_name'], table_name='sellers',condition=None,return_as_list=False)
        for index, row in enumerate(row_info):
            self.log.info(f"ID {index} : {row[0]}, Name: {row[1]}")
        while True:
            try:
                user_pick = int(input('choose the seller ID you want to crawl products from: '))
                if 0 <= user_pick < len(row_info):
                    break
                else:
                    self.log.info('Invalid choose, please try again.')
            except ValueError:
                self.log.info('Invalid input, please enter a number.')
        selected_seller = row_info[user_pick]
        self.log.info(f'You chose {selected_seller[1]} with ID {selected_seller[0]}')    
        seller_products = self.db_handler.get_row_info(['product_link', 'product_price'], 'products', ['seller_name', selected_seller[1]])
        available_products = [product[0] for product in seller_products if product[1] != 'product unavailable']
        self.log.info(f'{len(available_products)} available products found for {selected_seller[1]}')
        for index, link in enumerate(available_products):
            self.log.info(f'Starting to crawl - {index + 1}/{len(available_products)}')
            self.product_extraction_scraper.run(link)

    def run_single_scraper_product(self):
        while True:
            url = input('Enter product URL: ')
            if 'product' not in url:
                self.log.info('URL must contain the word "product". Please try again.')
                continue
            if not re.search(r'dkp-\d+', url):
                self.log.info('URL must contain a product ID in the format "dkp-xxxxxx". Please try again.')
                continue
            break        
        self.log.info(f'Starting to crawl - {url.split("/")[4]}')
        self.product_extraction_scraper.run(url)

    def scraper_all_product_on_db(self,):
        seller_products = self.db_handler.get_row_info(['product_link', 'product_price'], 'products')
        available_products = [product[0] for product in seller_products if product[1] != 'product unavailable']
        self.log.info(f'{len(available_products)} available products found on database ')
        for index, link in enumerate(available_products):
            self.log.info(f'Starting to crawl - {index + 1}/{len(available_products)}')
            self.product_extraction_scraper.run(link)

    def export_table_to_csv(self,):
        def remove_old_file(filename):
            if os.path.exists(filename):
                os.remove(filename)
                self.log.info(f'{filename} remove successfully')

        def save_to_csv(data, headers, filename):
            with open(filename, mode='w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                writer.writerows(data)
            self.log.info(f'{filename} export successfully')

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
                row_info = self.db_handler.get_row_info(['seller_id', 'seller_name'], 'sellers') 
                for index, row in enumerate(row_info):
                    self.log.info(f"ID {index} : {row[0]}, Name: {row[1]}")
                    seller_id = row[0]
                while True:
                    try:
                        user_pick = int(input('choose the seller ID you want to export products from: '))
                        if 0 <= user_pick < len(row_info):
                            break
                        else:
                            self.log.info('Invalid choose, please try again.')
                    except ValueError:
                        self.log.info('Invalid input, please enter a number.')                
                selected_seller = row_info[user_pick]
                export_to_csv('products',seller_id,['seller_name', selected_seller[1]])
            elif choose == '3':
                export_to_csv('products',seller_id=None)
            elif choose == '4':
                row_info = self.db_handler.get_row_info(['seller_id', 'seller_name'], 'sellers') 
                for index, row in enumerate(row_info):
                    self.log.info(f"ID {index} : {row[0]}, Name: {row[1]}")
                    seller_id = row[0]
                while True:
                    try:
                        user_pick = int(input('choose the seller ID you want to export products extraction from: '))
                        if 0 <= user_pick < len(row_info):
                            break
                        else:
                            self.log.info('Invalid choose, please try again.')
                    except ValueError:
                        self.log.info('Invalid input, please enter a number.')
                selected_seller = row_info[user_pick]
                export_to_csv('products_extraction',seller_id,['seller_name', selected_seller[1]])
            elif choose == '5':
                export_to_csv('products_extraction',seller_id=None)
            elif choose == '6':
                export_to_csv('sellers',seller_id=None)
                export_to_csv('products',seller_id=None)
                export_to_csv('products_extraction',seller_id=None)
            elif choose == '7':
                pass
        else :
            self.log.error(f'database at {self.db_path} not found !. check database path .')    

    def database_report(self):
        seller_count = len(self.db_handler.get_row_info(fields='*',table_name='sellers',condition=None,return_as_list=True))
        product_count = len(self.db_handler.get_row_info(fields='*',table_name='products',condition=None,return_as_list=True))
        products_extrection_count = len(self.db_handler.get_row_info(fields='*',table_name='products_extraction',condition=None,return_as_list=True))
        seller_historical_count = len(self.db_handler.get_row_info(fields='*',table_name='sellers_history',condition=None,return_as_list=True))
        products_historical_count = len(self.db_handler.get_row_info(fields='*',table_name='products_history',condition=None,return_as_list=True))
        products_extrection_historical_count = len(self.db_handler.get_row_info(fields='*',table_name='products_extraction_history',condition=None,return_as_list=True))
        self.log.info(f"==================== DATABASE TABLES INFO ==================")
        self.log.info(f"{seller_count} sellers in the table.")
        self.log.info(f"{product_count} products in the table.")
        self.log.info(f"{products_extrection_count} products with all specifications in the table.")
        self.log.info(f"{seller_historical_count} historical sellers in the table.")
        self.log.info(f"{products_historical_count} historical products in the table.")
        self.log.info(f"{products_extrection_historical_count} products with all specifications in the historical table.")
        self.log.info(f"==================== DATABASE TABLES INFO ==================")          

    def start(self):
        while True:
            choose = self.display_menu()
            if choose == "1":
                self.get_driver()
                self.run_scraper_category()
            elif choose == "2" :
                self.get_driver()
                self.run_scraper_single()
            elif choose == "3" :
                self.get_driver()
                self.run_seller_scraper_product()
            elif choose == "4" :
                self.get_driver()
                self.run_single_scraper_product()
            elif choose == "5" :
                self.get_driver()
                self.scraper_all_product_on_db()
            elif choose == "6":
               self.export_table_to_csv()
               self.log.info(' [!] CSV file created successfully')
            elif choose == "7":
                self.database_report()
            elif choose == "8":
                if hasattr(self, '_driver'):
                    self._driver.close_driver()
                self.log.info("Exit the program.")
                break
            else:
                self.log.error("Invalid option, please try again.")
    
if __name__ == "__main__":
    # TODO add testing unit -> (TODO)
    # TODO add flask GUI -> (TODO) 
    # TODO add API endpoint -> (TODO) 
    # TODO add data analysis -> (TODO)
    # TODO  add seller category field to sellers table (TODO) 

    gecko_path = r'geckodriver.exe' # path to geckodriver.exe
    db_path = 'digikala_database.db'
    log = setup_logger()
    WebScraperPanel(driver_path=gecko_path,db_path=db_path,log=log).start()

