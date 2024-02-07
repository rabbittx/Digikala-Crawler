from source.seller_product_data_extractor import SellerProductDataExtractor
import csv  , os ,re
from source.logger import setup_logger
from source.driver_manager import DriverManager
from source.db_handler import DataBaseHandler
from source.product_details_extractor import ProductDetailsExtractor
import os
from source.config import ConsoleConfigManager

class DigiKalaScraper:
    def __init__(self, config, log, db_handler):
        self.config_manager = config
        self.logger = log
        self.db_path = self.config_manager.get_db_path()
        self.gecko_path = self.config_manager.get_gecko_path()
        self.headless_mode = self.config_manager.get_headless_mode()
        self.driver_type = self.config_manager.get_driver_type()
        self.db_handler = db_handler
        self.db_handler.create_tables()
        self.scroll_count = 3
        self.page_load_timeout = 10

    def initialize_driver(self, geko_path, driver_type, headless_mode, db_handler, logger):
        if self.headless_mode:
            self.logger.info('[+] browser will work in background, headless mode is True')
        else:
            self.logger.info("[+] browser will open normally")

        if not hasattr(self, '_driver'):
            self._driver = DriverManager(
                                        driver_type = driver_type,
                                        geko_path = geko_path,
                                        logger = logger, 
                                        headless_mode = headless_mode
                                        )
            self.webscraper = SellerProductDataExtractor(
                                                        driver = self._driver ,
                                                        db_handler = db_handler ,
                                                        logger = logger
                                                        )
            self.product_extraction_scraper = ProductDetailsExtractor(
                                                                     db_handler = db_handler,
                                                                     driver = self._driver,
                                                                     logger = logger
                                                                     )
        return self._driver
    

    def check_crawl_url(self, mode, input_url):
        check_data = {
            "crawl_mode": mode,
            "url": input_url,
            "message": '',
            "start_to_crawl" : False,
        }

        if check_data['crawl_mode'] == 'single_product':
            if not re.search(r'https://www\.digikala\.com/product/dkp-\d+/$', check_data['url']):
                check_data['message'] = 'The URL does not belong to any product. Please check it and try again.'
                self.logger.warning('[!] ' + check_data['message'])

        elif check_data['crawl_mode'] == 'single_seller':
            if not re.match(r'https://www\.digikala\.com/seller/[A-Za-z0-9]+/$', check_data['url']):
                check_data['message'] = 'The URL does not belong to any seller. Please check it and try again.'
                self.logger.warning("[!] " + check_data['message'])

        elif check_data['crawl_mode'] == 'category':
            if not re.search(r'search/\?q=|/category-|/search/', check_data['url']):
                check_data['message'] = 'The category URL is incorrect. Please try again'
                self.logger.warning('[!] ' + check_data['message'])
        else:
            check_data['message'] = 'Current input URL is ready to start to crawl.'
            check_data['start_to_crawl'] = True
            self.logger.info('[+] ' + check_data['message'])

        return check_data
    
    def initialize_crawl_for_products(self, available_products):
        """Logs and executes crawling for a list of available product URLs."""
        self.logger.info(f'Found {len(available_products)} available products.')
        for index, link in enumerate(available_products):
            self.logger.info(f'Starting crawl {index + 1} of {len(available_products)}: {link}')
            self.product_extraction_scraper.run(link)

    def execute_crawl(self, mode, input_url, scroll_count, seller_info=None):
        # Pre-processing for seller_info
        seller_id, seller_name = ('-', '-') if seller_info is None else seller_info
        
        # Initializing crawl settings
        crawl_settings = {
            "mode": mode,
            "url": input_url,
            "scrolling_count": scroll_count,
            "seller_id": seller_id,
            "seller_name": seller_name
        }
        
        if not hasattr(self, '_driver'):
            self.initialize_driver(self.driver_type)
            
        if crawl_settings['mode'] == 'all_products':
            seller_products = self.db_handler.get_row_info(['product_link', 'product_price'], 'products')
            available_products = [product[0] for product in seller_products if product[1] != 'product unavailable']
            self.initialize_crawl_for_products(available_products)
                
        elif crawl_settings['mode'] == 'single_product':
            self.logger.info(f'Starting to crawl the product at URL: {crawl_settings["url"]}')
            self.product_extraction_scraper.run(crawl_settings['url'])

        elif crawl_settings['mode'] == 'seller_products':
            self.logger.info(f'Crawling products for seller "{crawl_settings["seller_name"]}" with ID {crawl_settings["seller_id"]}.')    
            seller_products = self.db_handler.get_row_info(['product_link', 'product_price'], 'products', ['seller_name', crawl_settings['seller_name']])
            available_products = [product[0] for product in seller_products if product[1] != 'product unavailable']
            self.initialize_crawl_for_products(available_products)

        elif crawl_settings['mode'] == 'single_seller':
            self.webscraper.check_seller(crawl_settings['url'])
            self.logger.info("Data extraction for the specified seller has been completed successfully.")
            
        elif crawl_settings['mode'] == 'category':
            self.webscraper.check_category(crawl_settings['url'], crawl_settings['scrolling_count'])
            self.logger.info("Data extraction for the specified category has been completed successfully.")
            
        else:
            raise ValueError("Invalid crawl mode selected.")

    def remove_old_file(self, filename):
        if os.path.exists(filename):
            os.remove(filename)
            self.logger.info(f'Removed old file: {filename} successfully.')

    def save_to_csv(self, data, headers, filename):
        with open(filename, mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(data)
        self.logger.info(f'Exported data to {filename} successfully.')

    def export_table(self, table_name, seller_id=None, condition=None):
        csv_file_name = f'{seller_id}-{table_name}' if seller_id != '-' else f'{table_name}'
        csv_filename = f'{csv_file_name}-database.csv'
        self.remove_old_file(csv_filename)
        data = self.db_handler.get_row_info(['*'], table_name, condition)
        headers = self.db_handler.get_column_names(table_name)
        self.save_to_csv(data, headers, csv_filename)


    def export_data_to_csv(self, export_mode, seller_info):

        seller_id, seller_name = ('-', '-') if seller_info is None else seller_info

        if not os.path.exists(self.db_path):
            self.logger.error(f'ERROR: Database at {self.db_path} not found. Check database path.')
            return

        mode_actions = {
            'all_seller': lambda: self.export_table('sellers'),
            'seller_products': lambda: self.export_table('products', seller_id, ['seller_name', seller_name]),
            'all_products': lambda: self.export_table('products'),
            'seller_products_with_all_specifications': lambda: self.export_table('products_extraction', seller_id, ['seller_name', seller_name]),
            'all_products_with_specifications': lambda: self.export_table('products_extraction'),
            'all_data': lambda: [self.export_table('sellers'), self.export_table('products'), self.export_table('products_extraction')],
            'future': lambda: None,  
        }

        action = mode_actions.get(export_mode)
        if action:
            action()
            self.logger.info('Done processing the request. Exporting data...')
        else:
            self.logger.error(f'Invalid export mode: {export_mode}')





