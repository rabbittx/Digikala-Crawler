from crawler import WebScraper
import csv ,sqlite3 , os ,re
from logger import setup_logger
from driver_manager import DriverManager
from db_handler import DataBaseHandler
from products_extraction import productExtraction
class WebScraperPanel:
    def __init__(self,driver_path,db_path,log ):
        self.log = log
        self.db_path = db_path
        self.driver = DriverManager(driver_path=driver_path,log=self.log)
        self.db_handler = DataBaseHandler(db_path,log=self.log)
        self.webscraper = WebScraper(driver=self.driver,db_handler=self.db_handler,log=log)
        self.product_extraction_scraper = productExtraction(db_handler=self.db_handler,driver=self.driver,log=self.log)
        self.db_handler.create_tables()

    def display_menu(self):
        print("----------- welcome to digikala web crawler -------------")
        print("1. start to crawl for category")
        print("2. start to crawl for single seller")
        print("3. export all data in csv file ")
        print("4. crawl seller product ")
        print("5. crawl single product ")
        print("6. crawl all product on database ")
        print("7. quit")
        choice = input("enter your choice : ")
        return choice


    def run_scraper_category(self):

        while True :
            category_url = input("enter category url to crawl: ")

            if 'search/?q=' not in category_url :
                print('wrong category url try one more time') 
                continue
            break        
        
        scroll_count = input("Please enter the number of page scroll rates (Example 5 ) : ")

        try:
            scroll_count = int(scroll_count)
        except ValueError:
            print("The number of scrolling times must be a number. By default, it is set to 3.")
            scroll_count = 3
        self.webscraper.check_category(category_url,scroll_count)
        print("Data extraction was done successfully.")

    def run_scraper_single(self):
        seller_page_url = input("enter seller page url to crawl: ")
        self.webscraper.check_seller(seller_page_url)
        print("Data extraction was done successfully.")

    def run_seller_scraper_product(self):
        row_info = self.db_handler.get_row_info(['seller_id', 'seller_name'], 'sellers')
    
        for index, row in enumerate(row_info):
            self.log.info(f"ID {index} : {row[0]}, Name: {row[1]}")
        
        while True:
            try:
                user_pick = int(input('choice the seller ID you want to crawl products from: '))
                if 0 <= user_pick < len(row_info):
                    break
                else:
                    self.log.info('Invalid choice, please try again.')
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

    def scraper_all_prdouct_on_db(self,):
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
                self.log.info(f'{filename} remove succsusfully')

        def save_to_csv(data, headers, filename):
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                writer.writerows(data)
            self.log.info(f'{filename} exprot succsusfully')
        if os.path.exists(self.db_path):
            print('----------- export menu ---------')
            print('choies the data you need to export')
            print('1.sellers table data .')
            print('2.seller products table data with ID .')
            print('3.all seller products table .')
            print('4.single seller products extraction .')
            print('5.all seller products extraction .')
            print('6.all table  .')
            print('7.back to crawler menu .')
            choies = input('choies what you need : ')

            if choies == '1':
                remove_old_file('sellers_database.csv')
                data = self.db_handler.get_row_info(['*'],'sellers')
                headers = self.db_handler.get_column_names('sellers')
                save_to_csv(data, headers, 'sellers_database.csv')
                
            elif choies == '2' :
                row_info = self.db_handler.get_row_info(['seller_id', 'seller_name'], 'sellers')
            
                for index, row in enumerate(row_info):
                    self.log.info(f"ID {index} : {row[0]}, Name: {row[1]}")
                    seller_id = row[0]
                while True:
                    try:
                        user_pick = int(input('choice the seller ID you want to export products from: '))
                        if 0 <= user_pick < len(row_info):
                            break
                        else:
                            self.log.info('Invalid choice, please try again.')
                    except ValueError:
                        self.log.info('Invalid input, please enter a number.')
                selected_seller = row_info[user_pick]
                remove_old_file(f'sellers_{seller_id}_products_database.csv')

                data = self.db_handler.get_row_info(['*'], 'products', ['seller_name', selected_seller[1]])
                headers = self.db_handler.get_column_names('products')
                save_to_csv(data, headers, f'sellers_{seller_id}_products_database.csv')

            elif choies == '3':
                remove_old_file('all_seler_products_database.csv')
                data = self.db_handler.get_row_info(['*'],'products')
                headers = self.db_handler.get_column_names('products')
                save_to_csv(data, headers, 'all_seler_products_database.csv')

            elif choies == '4':
                row_info = self.db_handler.get_row_info(['seller_id', 'seller_name'], 'sellers')
            
                for index, row in enumerate(row_info):
                    self.log.info(f"ID {index} : {row[0]}, Name: {row[1]}")
                    seller_id = row[0]
                while True:
                    try:
                        user_pick = int(input('choice the seller ID you want to export products extraction from: '))
                        if 0 <= user_pick < len(row_info):
                            break
                        else:
                            self.log.info('Invalid choice, please try again.')
                    except ValueError:
                        self.log.info('Invalid input, please enter a number.')
                selected_seller = row_info[user_pick]
                remove_old_file(f'sellers_{seller_id}_products_extraction_database.csv')

                data = self.db_handler.get_row_info(['*'], 'products_extraction', ['seller_name', selected_seller[1]])
                headers = self.db_handler.get_column_names('products_extraction')
                save_to_csv(data, headers, f'sellers_{seller_id}_products_database.csv')
            elif choies == '5':
                row_info = self.db_handler.get_row_info(['seller_id', 'seller_name'], 'sellers')
            
                for index, row in enumerate(row_info):
                    self.log.info(f"ID {index} : {row[0]}, Name: {row[1]}")
                    seller_id = row[0]
                while True:
                    try:
                        user_pick = int(input('choice the seller ID you want to export products extraction from: '))
                        if 0 <= user_pick < len(row_info):
                            break
                        else:
                            self.log.info('Invalid choice, please try again.')
                    except ValueError:
                        self.log.info('Invalid input, please enter a number.')
                selected_seller = row_info[user_pick]
                remove_old_file(f'sellers_{seller_id}_products_extraction_database.csv')

                data = self.db_handler.get_row_info(['*'], 'products_extraction', )
                headers = self.db_handler.get_column_names('products_extraction')
                save_to_csv(data, headers, f'sellers_{seller_id}_products_database.csv')

            elif choies == '6':
                remove_old_file('all_seler_products_database.csv')
                data = self.db_handler.get_row_info(['*'],'products')
                headers = self.db_handler.get_column_names('products')
                save_to_csv(data, headers, 'all_seler_products_database.csv')

                remove_old_file('all_sellers_database.csv')
                data = self.db_handler.get_row_info(['*'],'sellers')
                headers = self.db_handler.get_column_names('sellers')
                save_to_csv(data, headers, 'all_sellers_database.csv')
                
                remove_old_file('all_products_database.csv')
                data = self.db_handler.get_row_info(['*'],'products_extraction')
                headers = self.db_handler.get_column_names('products_extraction')
                save_to_csv(data, headers, 'all_products_database.csv')
            elif choies == '7':
                pass
        else :
            print(f'database at {db_path} not found !. check database path .')    

        

    def start(self):
        while True:
            choice = self.display_menu()
            if choice == "1":
                self.run_scraper_category()
            elif choice == "2" :
                self.run_scraper_single()
            elif choice == "3":
               self.export_table_to_csv()
               print(' [!] CSV file create successfully')

            elif choice == "4" :
                self.run_seller_scraper_product()
            elif choice == "5" :
                self.run_single_scraper_product()
            elif choice == "6" :
                self.scraper_all_prdouct_on_db()
            elif choice == "7":
                self.driver.close_driver()
                print("Exit the program.")
                break
            else:
                print("Invalid option, please try again.")
    
if __name__ == "__main__":
    # TODO add testing unit -> (TODO)
    # TODO add flask GUI -> (TODO) 
    # TODO add API endpoint -> (TODO) 
    # TODO add data analysis -> (TODO)
    # TODO  add seller category field to sellers table (TODO) 

    geko_path = r'geckodriver.exe' # path to geckodriver.exe
    db_path = 'digikala_database.db'
    log = setup_logger()
    WebScraperPanel(driver_path=geko_path,db_path=db_path,log=log).start()

