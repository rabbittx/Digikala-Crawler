from source.logger import setup_logger
from source.webScraper import DigiKalaScraper
import sys ,os
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
                        '8': ('rest setting and reconfig.','Reconfig'),
                        '9': ('Quit the scraper.','QuitMode'),
                        'help': ('Enter a number (1-9) to select an option or enter \'help\' to check help menu','helpMode')       
                        }
        
        example_menu = {
                        'SingleProductCrawlMode' : 'https://www.digikala.com/product/dkp-11194944',
                        'SingleSellerCrawlMode' : 'https://www.digikala.com/seller/6xwus/',
                        'CategoryCrawlMode_01' : 'https://www.digikala.com/search/?q=iphone',
                        'CategoryCrawlMode_02' : 'https://www.digikala.com/search/category-mobile-phone/xiaomi/',
                        'CategoryCrawlMode_03' : 'https://www.digikala.com/search/',
                       }
        
        export_menu = {
                        'export_welcome' : '----------- CSV export menu ---------\nChoose the data you wish to export .',
                        '1' : ('export sellers table data .','all_seller'),
                        '2' : ('export seller\'s products data with ID .','seller_products'),
                        '3' : ('export all seller products table .','all_products'),
                        '4' : ('export single seller\'s product information with all specifications .','seller_products_with_all_specifications'),
                        '5' : ('export all seller\'s products with all specifications .','all_products_with_specifications'),
                        '6' : ('export all table data .','all_data'),
                        '7' : ('back to crawler menu .','back_to_menu')
                      }
        return {
                'scraper_menu' : scraper_menu,
                'example_menu' : example_menu,
                'export_menu' : export_menu,
                }
    
    def crawl_options(self,mode,input_url=None,scroll_count=None,seller_info=None):
        crawler_option = {
                            'CategoryCrawlMode': lambda: self.scraper.execute_crawl(mode=mode, input_url=input_url, scroll_count=scroll_count, seller_info=seller_info),
                            'SingleSellerCrawlMode': lambda: self.scraper.execute_crawl(mode=mode, input_url=input_url, scroll_count=scroll_count, seller_info=seller_info),
                            'SingleSellerProductCrawlMode': lambda: self.scraper.execute_crawl(mode=mode, input_url=input_url, scroll_count=scroll_count, seller_info=seller_info),
                            'SingleProductCrawlMode': lambda: self.scraper.execute_crawl(mode=mode, input_url=input_url, scroll_count=scroll_count, seller_info=seller_info),
                            'AllProductsCrawlMode': lambda: self.scraper.execute_crawl(mode=mode, input_url=input_url, scroll_count=scroll_count, seller_info=seller_info),
                            'CSVExportMode': lambda : self.csv_export(self.menus()['export_menu']),
                            'ComprehensiveDatabaseReportMode': lambda : self.database_report_show(self.scraper.database_report()),
                            'Reconfig': lambda : self.reconfig(self.scraper.config_file_path),
                            'QuitMode':lambda: sys.exit("Exiting the program..."),
                            'helpMode':lambda: self.show_help(),

                        }

        if mode in crawler_option:
            crawler_option[mode]()
        else:
            raise ValueError("Invalid mode specified.")
    def show_help(self):
        self.logger.info("""
                        ----------------------- HELP ------------------------
                        To effectively use the Digikala-Crawler, please follow these steps:

                        1. Set the database path and the path to your geckodriver.
                        2. Choose your preferred web driver: Firefox or Chrome. Specify if you'd like to run it in headless mode for background operations without opening a browser window.
                        3. Decide on the crawling mode to start gathering data. After collecting some data, you can export the required information using the CSVExportMode option.
                        4. For detailed instructions, examples, and more, visit our documentation at 'https://github.com/rabbittx/Digikala-Crawler/tree/master/archive/documents'.
                        5. Need further assistance? Feel free to open an issue on our GitHub page at 'https://github.com/rabbittx/Digikala-Crawler/issues' or contact us directly at amirhabibi1993x@gmail.com.

                        Thank you for using Digikala-Crawler. Happy data gathering!
                        """)
    def reconfig(self,config_path):
        if os.path.exists(config_path):
            os.remove(config_path)
            self.scraper = DigiKalaScraper(log=logger,config_file_path=config_file_path,)


    def show_examples(self,mode,menu):
        self.logger.info('------------ URL examples --------------------')
        for k,v in  menu.items():
            if mode in k :
                self.logger.info(v)

    def csv_export(self,menu):
        mode = self.show_menu(menu=menu)
        self.scraper.export_data_to_csv(mode)

    def database_report_show(self,report):
        for k,v in  report.items():
            self.logger.info(f'[+] DATABASE REPROT : for {k.replace("_count"," ").replace("_"," ")} have [{v}] record found .')
        
    def get_crawl_input(self,mode):
        while True:
            self.logger.info(f"Please enter the {mode.replace('CrawlMode','')} URL you want to crawl, or type 'exit' to quit: ")
            input_url = input()

            if input_url.lower() == 'exit':
                self.logger.info("Exiting the crawl input process.")
                return None  
            
            crawl_data = self.scraper.check_crawl_url(mode=mode, input_url=input_url)
            
            if crawl_data['start_to_crawl']:
                return input_url.lower()

            else:
                self.logger.info("The URL is not valid for crawling. Please try again.")
   
    def show_menu(self,menu):
        for (k,v) in  menu.items():
            self.logger.info(f"[+] {k} => {v[0]}") if k == 'help' else self.logger.info(f"[+] {k}) {v[0]}")
        user_choose = input('choose the option you need : ')
        if user_choose not in menu.keys():
            self.logger.info('[-] choose again !')
        mode = menu[str(user_choose)][1]
        return mode

    def run(self):
        while True: 
            mode = self.show_menu(self.menus()['scraper_menu'] )
            if mode in ['CategoryCrawlMode','SingleSellerCrawlMode','SingleProductCrawlMode'] :
                self.show_examples(mode=mode,menu=self.menus()['example_menu'])
                input_url = self.get_crawl_input(mode)
                if input_url is None:
                    self.run()
            else : 
                input_url = None  
            if mode == 'CategoryCrawlMode' :
                scroll_count = int(input('enter scroll count on page : '))
            else :
                scroll_count = True
            if mode == 'SingleSellerProductCrawlMode' :
                seller_info = self.scraper.show_sllers()
            else :
                seller_info = None

            self.crawl_options(mode=mode,input_url=input_url,scroll_count=scroll_count,seller_info=seller_info)
        
    
        
    

if __name__ == '__main__' :
    logger = setup_logger() # logger to handle logs
    config_file_path = 'console-config.ini' # setting file path 
    panel = DigikalaScraperConsolePanel(logger=logger,config_file_path=config_file_path)
    panel.run()

