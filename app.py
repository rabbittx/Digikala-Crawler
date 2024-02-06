from flask import Flask, render_template, request, redirect, url_for
# فرض می‌شود که WebConfigManager، setup_logger، و DataBaseHandler به درستی پیاده‌سازی شده‌اند
from source.config import WebConfigManager
from source.logger import setup_logger
from source.db_handler import DataBaseHandler

from source.config import WebConfigManager
from source.logger import setup_logger
from source.db_handler import DataBaseHandler

from source.config import WebConfigManager
from source.logger import setup_logger
from source.db_handler import DataBaseHandler

class WebGUIApp:
    def __init__(self, config_manager, log):
        self.app = Flask(__name__)
        self.config_manager = config_manager
        self.log = log
        self.db_handler = None

        
        self.check_config()
        self.add_routes()

    def check_config(self):
        db_path = self.config_manager.get_setting("Paths", "dbpath")
        if db_path:
            self.db_handler = DataBaseHandler(db_path, self.log)

    def add_routes(self):
        @self.app.route("/", methods=["GET", "POST"])
        def index():
            if not self.db_handler:  
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
                self.check_config()
                return redirect(url_for('index'))     
            
            geko_path = self.config_manager.get_setting('Paths', 'GeckoPath')
            db_path = self.config_manager.get_setting('Paths', 'DBPath')
            driver_type = self.config_manager.get_setting('Setting', 'DriverType')
            headless_mode = self.config_manager.get_setting('Setting', 'HeadlessMode') == 'true'

            return render_template('settings.html')

    def run(self):
        self.app.run(debug=True)


if __name__ == "__main__":
    config_manager = WebConfigManager("web_config.ini")
    log = setup_logger()
    
    web_app = WebGUIApp(config_manager, log,)
    web_app.run()