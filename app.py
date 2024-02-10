from flask import Flask, render_template, request, redirect, url_for ,jsonify
# فرض می‌شود که WebConfigManager، setup_logger، و DataBaseHandler به درستی پیاده‌سازی شده‌اند
from source.config import WebConfigManager
from source.logger import web_setup_logger
from source.db_handler import DataBaseHandler
from source.webScraper import DigiKalaScraper
import sys
class WebGUIApp:
    def __init__(self  ):
        self.app = Flask(__name__)
        self.log = web_setup_logger()
        self.config_manager = WebConfigManager(log=self.log,config_file="web_config.ini")
        self.log.info('hello from init')
        self.add_routes()
        self.scraper=DigiKalaScraper(config_file_path=self.config_manager.config_file,log=self.log)
        self.db_handler =self.scraper.db_handler

    def add_routes(self):

        @self.app.route("/", methods=["GET", "POST"])
        def index():
            if not self.config_manager.get_setting("Paths", "geckopath"):  
                return redirect(url_for('settings'))
            try:
                # sellers = self.db_handler.get_row_info(fields=['seller_id,seller_name'],table_name='seller_name',condition=None,return_as_list=False)
                sellers = self.db_handler.get_sellers() if self.db_handler else []
                return render_template("index.html", sellers=sellers)
            except Exception as e:
                self.log.error(f"Database error: {e}")
                return "Error accessing the database."

        @self.app.route("/settings", methods=["GET", "POST"])
        def settings():
            if request.method == "POST":
                geko_path = request.form.get('gekoPath')
                db_path = request.form.get('dbPath')
                driver_type = request.form.get('driverType')
                headless_mode = request.form.get('headlessMode', 'off') == 'on'  # Checkbox 'on' if checked, otherwise 'off'
                self.config_manager.set_setting('Paths', 'GeckoPath', geko_path)
                self.config_manager.set_setting('Paths', 'DBPath', db_path)
                self.config_manager.set_setting('Setting', 'DriverType', driver_type)
                self.config_manager.set_setting('Setting', 'HeadlessMode', str(headless_mode).lower())
                return redirect(url_for('index'))     
            geko_path = self.config_manager.get_setting('Paths', 'GeckoPath')
            db_path = self.config_manager.get_setting('Paths', 'DBPath')
            driver_type = self.config_manager.get_setting('Setting', 'DriverType')
            headless_mode = self.config_manager.get_setting('Setting', 'HeadlessMode') == 'true'
            return render_template('settings.html')
                
        @self.app.route('/get-logs')
        def get_logs():
            num_lines = 10  
            with open(r'archive\logs\web_crawler_logs.txt', 'r') as file:
                logs = file.readlines()[-num_lines:]  
            return ''.join(logs)
          
        @self.app.route('/start-category-crawl', methods=['POST'])
        def start_category_crawl():
            if request.method == "POST" :
                category_url = request.form.get('categorycrawl')
                category_scroll_count = request.form.get('scrollCount')
                crawl_setting = self.scraper.check_crawl_url(mode='CategoryCrawlMode',input_url=category_url)
                if crawl_setting['start_to_crawl'] :
                    self.log.info(crawl_setting['message'])
                    self.log.info(type(category_scroll_count))
                    self.crawl_options(mode='CategoryCrawlMode',input_url=crawl_setting['url'],scroll_count=int(category_scroll_count),seller_info=None)
                    return jsonify({"status": "succsue", "message": crawl_setting['message'], "url": crawl_setting['url']})
                else:
                    return jsonify({"status": "error", "message": crawl_setting['message'], "url": crawl_setting['url']})
   
        @self.app.route('/export',methods=['POST'])
        def export_data():
            if request.method == "POST":
                db_path = request.form.get('dbPath')
                driver_type = request.form.get('driverType')   

        @self.app.route('/single_seller',methods=['POST'])
        def single_product_page():
            pass
        @self.app.route('/single_product',methods=['POST'])
        def single_seller_page():
            pass
        @self.app.route('/single_seller_prdoucts',methods=['POST'])
        def single_seller_prdoucts():
            pass
        @self.app.route('/all_products',methods=['POST'])
        def crawl_all_products():
            pass
        
        # exports options 
        
        
        # report database option


    def crawl_options(self,mode,input_url=None,scroll_count=None,seller_info=None):
        crawler_option = {
                            'CategoryCrawlMode': lambda: self.scraper.execute_crawl(mode=mode, input_url=input_url, scroll_count=scroll_count, seller_info=seller_info),
                            'SingleSellerCrawlMode': lambda: self.scraper.execute_crawl(mode=mode, input_url=input_url, scroll_count=scroll_count, seller_info=seller_info),
                            'SingleSellerProductCrawlMode': lambda: self.scraper.execute_crawl(mode=mode, input_url=input_url, scroll_count=scroll_count, seller_info=seller_info),
                            'SingleProductCrawlMode': lambda: self.scraper.execute_crawl(mode=mode, input_url=input_url, scroll_count=scroll_count, seller_info=seller_info),
                            'AllProductsCrawlMode': lambda: self.scraper.execute_crawl(mode=mode, input_url=input_url, scroll_count=scroll_count, seller_info=seller_info),
                            'CSVExportMode': lambda : self.csv_export(),
                            'ComprehensiveDatabaseReportMode': lambda : self.database_report_show(self.scraper.database_report()),
                            'QuitMode':lambda: sys.exit("Exiting the program..."),

                        }

        if mode in crawler_option:
            crawler_option[mode]()
        else:
            raise ValueError("Invalid mode specified.")
    
    
    
    
    def run(self):
        self.app.run(debug=True)


if __name__ == "__main__":
    
    web_app = WebGUIApp().run()
