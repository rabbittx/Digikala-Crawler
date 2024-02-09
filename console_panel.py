from source.logger import setup_logger
from webScraper import DigiKalaScraper

class DigikalaScraperConsolePanel:
    def __init__(self,logger,config_file_path):
        self.logger = logger
        self.scraper = DigiKalaScraper(log=logger,config_file_path=config_file_path,)

    def menus(self):
        scraper_menu = {
                        'spacper_welcome': ('Welcome to DigiKala Scraper Console Panel','welcomeMode'),
                        '1': ('Start crawling for a category.','CategoryCrawlMode'),
                        '2': ('Start crawling for a single seller.','SingleSellerCrawlMode'),
                        '3': ('Start crawling for a single seller\'s product including all specifications.','SingleSellerProductCrawlMode'),
                        '4': ('Start crawling for a single product including all specifications.','SingleProductCrawlMode'),
                        '5': ('Start crawling for all products in the database including all specifications.','AllProductsCrawlMode'),
                        '6': ('Open CSV export menu.','CSVExportMode'),
                        '7': ('Generate comprehensive database report with all tables.','ComprehensiveDatabaseReportMode'),
                        '8': ('Quit the scraper.','QuitMode'),
                        'help': ('Enter a number (1-8) to select an option','helpMode')       
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
    
    def crawl_options(self,mode,input_url,scroll_count=None,seller_info=None):
        print(f'page scrolling count is ===> [{scroll_count}]')
        crawler_option = {
                            'CategoryCrawlMode': lambda: self.scraper.execute_crawl(mode=mode, input_url=input_url, scroll_count=scroll_count, seller_info=None),
                            'SingleSellerCrawlMode': lambda: self.scraper.execute_crawl(mode=mode, input_url=input_url, scroll_count=scroll_count, seller_info=None),
                            'SingleSellerProductCrawlMode': '',
                            'SingleProductCrawlMode': '',
                            'AllProductsCrawlMode': '',
                            'CSVExportMode': '',
                            'ComprehensiveDatabaseReportMode': '',
                            'QuitMode': '',

                        }
        if mode in crawler_option:
            crawler_option[mode]()
        else:
            raise ValueError("Invalid mode specified.")
        
    def get_crawl_input(self,mode):
        while True:
            # فرض بر این است که input_url توسط کاربر وارد می‌شود
            input_url = input(f"Please enter the {mode.replace('CrawlMode','')} URL you want to crawl, or type 'exit' to quit: ")

            # ارائه گزینه برای خروج
            if input_url.lower() == 'exit':
                print("Exiting the crawl input process.")
                return None  # یا هر عملی که مایلید در صورت خروج انجام دهید

            crawl_data = self.scraper.check_crawl_url(mode=mode, input_url=input_url)
            
            if crawl_data['start_to_crawl']:
                
                return input_url.lower()
                # اگر start_to_crawl True باشد، حلقه شکسته و فرآیند ادامه پیدا می‌کند
                break
            else:
                # اگر start_to_crawl False باشد، پیامی نمایش داده و برای ورودی جدید از کاربر درخواست می‌شود
                print("The URL is not valid for crawling. Please try again.")
            # حلقه به طور خودکار ادامه می‌یابد
                
    def run(self):
        menus = self.menus()
        for (k,v) in  menus['scraper_menu'].items():
           
            self.logger.info(f"[+] {k} => {v[0]}") if k == 'help' else self.logger.info(f"[+] {k}) {v[0]}")
                

        user_choose = input('choose the option you need : ')
        if user_choose not in menus['scraper_menu'].keys():
            self.logger.info('[-] choose again !')
        # if menus['scraper_menu'][str(user_choose)][1] == 'SingleSellerProductCrawlMode' :
        #     seller_info = self.scraper.show_sllers()
        #     print(seller_info)
        if menus['scraper_menu'][str(user_choose)][1] == 'CategoryCrawlMode' \
            or menus['scraper_menu'][str(user_choose)][1] == 'SingleSellerCrawlMode'\
                or menus['scraper_menu'][str(user_choose)][1] == 'SingleProductCrawlMode':
            input_url = self.get_crawl_input(menus['scraper_menu'][str(user_choose)][1])
            if input_url is None:
                self.run()

        if menus['scraper_menu'][str(user_choose)][1] == 'CategoryCrawlMode' :
            scroll_count = int(input('enter scroll count on page : '))
        else :
            scroll_count = True
        
        
        self.crawl_options(mode=menus["scraper_menu"][str(user_choose)][1],input_url=input_url,scroll_count=scroll_count)
        
        
    

if __name__ == '__main__' :
    logger = setup_logger()
    config_file_path = 'console-config4.ini'
    panel = DigikalaScraperConsolePanel(logger=logger,config_file_path=config_file_path)
    panel.run()


# BUG -> get_next_id need to be same when data need to replace with historyical table . 
# TODO -> all mode name need to get update in all script files .
# TODO -> check for 404 pages and product not available page on open_page()
# TODO -> regex patterns need to get updated to check if link is valid => eq : link start with https(fixed),url split tokens length etc ...
# TODO -> befor get page_source in driver_manager need to check if products in loading... with to it get load 
      