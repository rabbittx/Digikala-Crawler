from flask import Flask, render_template, request, redirect, url_for ,jsonify 
from source.logger import web_setup_logger
from source.webScraper import DigiKalaScraper




class WebGUIApp:
    def __init__(self, config_file_path):
        self.app = Flask(__name__)
        self.log = web_setup_logger()
        self.log.info('hello from init')
        self.scraper = DigiKalaScraper(log=self.log, config_file_path=config_file_path)
        self.add_routes()

    def add_routes(self):
        @self.app.route("/", methods=["GET", "POST"])
        def index():
            if not self.scraper.config_manager.get_setting('Paths', 'GeckoPath'):  
                return redirect(url_for('settings'))
            try:
                sellers = self.scraper.get_sellers() if self.scraper else []
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
                headless_mode = request.form.get('headlessMode', 'off') == 'on'  # Checkbox
                self.scraper.config_manager.set_setting('Paths', 'GeckoPath', geko_path)
                self.scraper.config_manager.set_setting('Paths', 'DBPath', db_path)
                self.scraper.config_manager.set_setting('Setting', 'DriverType', driver_type)
                self.scraper.config_manager.set_setting('Setting', 'HeadlessMode', str(headless_mode).lower())
                return redirect(url_for('index'))
            
            geko_path = self.scraper.config_manager.get_setting('Paths', 'GeckoPath')
            db_path = self.scraper.config_manager.get_setting('Paths', 'DBPath')
            driver_type = self.scraper.config_manager.get_setting('Setting', 'DriverType')
            headless_mode = self.scraper.config_manager.get_setting('Setting', 'HeadlessMode') == 'true'
            
            return render_template('settings.html', geko_path=geko_path, db_path=db_path, driver_type=driver_type, headless_mode=headless_mode)
                
        @self.app.route('/get-logs')
        def get_logs():
            num_lines = 10  
            with open(r'archive\logs\web_crawler_logs.txt', 'r') as file:
                logs = file.readlines()[-num_lines:]  
            return ''.join(logs)
          
        @self.app.route('/start-category-crawl', methods=['GET','POST'])
        def start_category_crawl():
            if request.method == "POST" :
                category_url = request.form.get('categorycrawl')
                category_scroll_count = request.form.get('scrollCount')
                crawl_setting = self.scraper.check_crawl_url(mode='CategoryCrawlMode',input_url=category_url)
                if crawl_setting['start_to_crawl'] :
                    self.log.info(crawl_setting['message'])
                    self.crawl_options(mode='CategoryCrawlMode',input_url=crawl_setting['url'],scroll_count=int(category_scroll_count))
                    return jsonify({"status": "succsue", "message": crawl_setting['message'], "url": crawl_setting['url']})
                else:
                    return jsonify({"status": "error", "message": crawl_setting['message'], "url": crawl_setting['url']})
   
        
        @self.app.route('/start_single_seller',methods=['GET','POST'])
        def single_product_page():
            if request.method == "POST" :
                single_url = request.form.get('single_seller_url_crawl')
                self.log.info(single_url)

                crawl_setting = self.scraper.check_crawl_url(mode='SingleSellerCrawlMode',input_url=single_url)
                if crawl_setting['start_to_crawl'] :
                    self.log.info(crawl_setting['message'])
                    self.crawl_options(mode='SingleSellerCrawlMode',input_url=crawl_setting['url'],)
                    return jsonify({"status": "succsue", "message": crawl_setting['message'], "url": crawl_setting['url']})
                else:
                    return jsonify({"status": "error", "message": crawl_setting['message'], "url": crawl_setting['url']})


        @self.app.route('/start_single_product',methods=['POST'])
        def single_seller_page():
            if request.method == "POST" :
                seller_id,seller_name  = request.form.get('single_seller_products_id').split('/')
                message = f'{seller_name,seller_id} is being processed...'
                self.log.info(message)
                self.crawl_options(mode='SingleSellerProductCrawlMode', input_url=None, scroll_count=None, seller_info=(seller_name,seller_id))
                return jsonify({"status": "succsue", "message": message, "url": None, 'seller_info' : (seller_name,seller_id)})


        @self.app.route('/single_prdoucts',methods=['POST'])
        def single_seller_prdoucts():
            if request.method == "POST" :
                single_url = request.form.get('single_product_url').strip()
                self.log.info(single_url)

                crawl_setting = self.scraper.check_crawl_url(mode='SingleProductCrawlMode',input_url=single_url)
                if crawl_setting['start_to_crawl'] :
                    self.log.info(crawl_setting['message'])
                    self.crawl_options(mode='SingleProductCrawlMode',input_url=crawl_setting['url'],)
                    crawl_setting['message'] = 'crawl  completed for this product.'
                    return jsonify({"status": "succsue", "message": crawl_setting['message'], "url": crawl_setting['url']})
                else:
                    return jsonify({"status": "error", "message": crawl_setting['message'], "url": crawl_setting['url']})

        @self.app.route('/all_products',methods=['GET','POST'])
        def crawl_all_products():
            if request.method == "POST" :
                self.crawl_options(mode='AllProductsCrawlMode',)
                return jsonify({"status": "succsue", "message": 'Strat to crawl all products in database', "url": None})
       
        # exports options 
        @self.app.route('/export_all_seller_data',methods=['POST'])
        def export_all_data():
            if request.method == "POST" :
                self.scraper.export_data_to_csv( 'all_seller')
                return jsonify({"status" : "succsue","message" : "seller data exprot to csv file complated . "})
            else : 
                return jsonify({"status" : "error","message" : "erorr to exprot sellers data check logs"})
            
        @self.app.route('/export_seller_products_id',methods=['POST'])
        def export_seller_products_with_id():
            if request.method == "POST" :
                seller_id,seller_name  = request.form.get('single_seller_products_id').split('/')
                self.log.info(f'{seller_id}/{seller_name}')
                self.scraper.export_data_to_csv('seller_products_id' ,seller_id=seller_id,seller_name=seller_name)
                return jsonify({"status": "succsue", "message": "export seller products with id completed"})
            else :
                return jsonify({"status": "error", "message": "error to export seller products with id"})

        @self.app.route('/export_all_products',methods=['GET','POST'])
        def export_all_products_csv():
            if request.method == "POST" :
                self.scraper.export_data_to_csv( 'all_products')
                return jsonify({"status" : "succsue","message" : "seller data exprot to csv file complated . "})
            else : 
                return jsonify({"status" : "error","message" : "erorr to exprot sellers data check logs"})

        @self.app.route('/export_single_sellers_product_information_with_all_specification',methods=['GET','POST'])
        def export_single_sellers_product_information_with_all_specifications():
            if request.method == "POST" :
                seller_id,seller_name  = request.form.get('seller_products_specification_id').split('/')
                self.log.info(f'{seller_id}/{seller_name}')
                self.scraper.export_data_to_csv('seller_products_with_all_specifications' ,seller_id=seller_id,seller_name=seller_name)
                return jsonify({"status": "succsue", "message": "export seller products with id completed"})
            else :
                return jsonify({"status": "error", "message": "error to export seller products with id"})

        @self.app.route('/export_all_sellers_products_with_all_specifications:',methods=['GET','POST'])
        def export_all_sellers_products_with_all_specifications():
            if request.method == "POST" :
                self.scraper.export_data_to_csv('all_products_with_specifications' )
                return jsonify({"status": "succsue", "message": "export seller products with id completed"})
            else :
                return jsonify({"status": "error", "message": "error to export seller products with id"})

        @self.app.route('/export_all_table_data',methods=['GET','POST'])
        def export_all_tables_data():
            if request.method == "POST" :
                self.scraper.export_data_to_csv('all_products_with_specifications' )
                return jsonify({"status": "succsue", "message": "export seller products with id completed"})
            else :
                return jsonify({"status": "error", "message": "error to export seller products with id"})

        # report database option
        @self.app.route("/report", methods = ['GET','POST'])
        def show_reports():
            if request.method == 'POST' :
                reports = self.scraper.database_report()
                message = f"""
                            seller  => {reports['seller_count']} records found ,
                            product  => {reports['product_count']} records found ,
                            products_extrection  => {reports['products_extrection_count']} records found ,
                            seller_historical  => {reports['seller_historical_count']} records found ,
                            products_historical  => {reports['products_historical_count']} records found ,
                            products_extrection_historical  => {reports['products_extrection_historical_count']} records found ,

                         """
                return jsonify({"status": "succsue", "message": message})

    def crawl_options(self,mode,input_url=None,scroll_count=None,seller_info=None):
        crawler_option = {
                            'CategoryCrawlMode': lambda: self.scraper.execute_crawl(mode=mode, input_url=input_url, scroll_count=scroll_count, seller_info=seller_info),
                            'SingleSellerCrawlMode': lambda: self.scraper.execute_crawl(mode=mode, input_url=input_url, scroll_count=scroll_count, seller_info=seller_info),
                            'SingleSellerProductCrawlMode': lambda: self.scraper.execute_crawl(mode=mode, input_url=input_url, scroll_count=scroll_count, seller_info=seller_info),
                            'SingleProductCrawlMode': lambda: self.scraper.execute_crawl(mode=mode, input_url=input_url, scroll_count=scroll_count, seller_info=seller_info),
                            'AllProductsCrawlMode': lambda: self.scraper.execute_crawl(mode=mode, input_url=input_url, scroll_count=scroll_count, seller_info=seller_info),
                            'CSVExportMode': lambda : self.csv_export(),
                            'ComprehensiveDatabaseReportMode': lambda : self.database_report_show(self.scraper.database_report()),
                        }
        if mode in crawler_option:
            crawler_option[mode]()
        else:
            raise ValueError("Invalid mode specified.")
    

    
    
    
    def run(self):
        self.app.run(debug=True)


if __name__ == "__main__":
    
    web_app = WebGUIApp(config_file_path='web_config0.ini')
    web_app.run()
