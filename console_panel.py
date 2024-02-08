from source.seller_product_data_extractor import SellerProductDataExtractor
import csv  , os ,re
from source.logger import setup_logger
from source.driver_manager import DriverManager
from source.db_handler import DataBaseHandler
from source.product_details_extractor import ProductDetailsExtractor
import os
from source.config import ConsoleConfigManager


from webScraper import DigiKalaScraper
class DigikalaScraperConsolePanel:
    def __init__(self,logger,config_file_path):
        self.logger = logger
        self.scraper = DigiKalaScraper(log=logger,config_file_path=config_file_path,)

    def menus(self):
        scraper_menu = {
                        'spacper_welcome' : 'Welcome to DigiKala Scraper Console panle',
                        '1' : 'start to crawl for category .',
                        '2' : 'start to crawl for single seller .',
                        '3' : 'start to crawl single seller product with all specifications .',
                        '4' : 'start crawl single product with all specifications .',
                        '5' : 'start crawl all products on database with all specifications .',
                        '6' : 'CSV export menu .',
                        '7' : 'check data in database .',
                        '8' : 'quit .',                        
                        }
        example_menu = {
                        'example_single_product' : 'https://www.digikala.com/product/dkp-11194944',
                        'example_single_seller' : 'https://www.digikala.com/seller/6xwus/',
                        'example_category_01' : 'https://www.digikala.com/search/?q=iphone',
                        'example_category_02' : 'https://www.digikala.com/search/category-mobile-phone/xiaomi/',
                        'example_category_03' : 'https://www.digikala.com/search/',
                       }
        
        export_menu = {
                        'export_welcome' : '----------- CSV export menu ---------\nChoose the data you wish to export .',
                        '1' : 'export sellers table data .',
                        '2' : 'export seller\'s products data with ID .',
                        '3' : 'export all seller products table .',
                        '4' : 'export single seller\'s product information with all specifications .',
                        '5' : 'export all seller\'s products with all specifications .',
                        '6' : 'export all table data .',
                        '7' : 'back to crawler menu .',
                      }
        return {
                'scraper_menu' : scraper_menu,
                'example_menu' : example_menu,
                'export_menu' : export_menu,
                }


if __name__ == '__main__' :
    logger = setup_logger()
    config_file_path = 'console-config2.ini'
    panel = DigikalaScraperConsolePanel(logger=logger,config_file_path=config_file_path)
    for k,v in panel.menus()['scraper_menu'].items():
        print(k," : ",v)