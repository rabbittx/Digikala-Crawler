from flask import Flask, render_template, request, redirect, url_for
from source.config import WebConfigManager  # اطمینان حاصل کنید که این مسیر درست است
from source.logger import setup_logger
from source.db_handler import DataBaseHandler



from flask import Flask, render_template, request, redirect, url_for

class WebGUIApp:
    def __init__(self, config_manager, log, db_handler):
        self.app = Flask(__name__)
        self.config_manager = config_manager
        self.log = log
        self.db_handler = db_handler

        # تعریف روت‌ها
        self.add_routes()

    def add_routes(self):
        app = self.app

        @app.route("/", methods=["GET", "POST"])
        def index():
            if request.method == "POST":
                # اجرای کدهای مرتبط با POST request
                pass

            # بازیابی اطلاعات فروشندگان
            sellers = self.db_handler.get_sellers()
            self.log.info(sellers)

            # ارسال اطلاعات به قالب
            return render_template("index.html", sellers=sellers)

        @app.route("/", methods=["GET", "POST"])
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
            headless_mode = self.config_manager.get_setting('Setting', 'HeadlessModeMode') == 'true'
                            
            return render_template('index.html')  # اطمینان حاصل کنید که فایل قالب موجود است           


    def run(self):
        self.app.run(debug=True)

if __name__ == "__main__":
    config_manager = WebConfigManager("web_config.ini")
    log = setup_logger()
    db_handler = DataBaseHandler(config_manager.get_setting("Paths", "dbpath"), log)
    
    web_app = WebGUIApp(config_manager, log, db_handler)
    web_app.run()