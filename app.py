from flask import Flask, render_template, request, redirect, url_for
from source.config import WebConfigManager  # اطمینان حاصل کنید که این مسیر درست است

app = Flask(__name__)
config_manager = WebConfigManager('web_config.ini')  # اطمینان حاصل کنید که مسیر config.ini درست است

@app.route('/', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        # دریافت مقادیر از فرم و به‌روزرسانی پیکربندی
        geko_path = request.form.get('gekoPath')
        db_path = request.form.get('dbPath')
        driver_type = request.form.get('driverType')
        headless_mode = request.form.get('headlessMode', 'off') == 'on'  # Checkbox 'on' if checked, otherwise 'off'
        config_manager.set_setting('Paths', 'GeckoPath', geko_path)
        config_manager.set_setting('Paths', 'DBPath', db_path)
        config_manager.set_setting('Setting', 'DriverType', driver_type)
        config_manager.set_setting('Setting', 'HeadlessMode', str(headless_mode).lower())
        
        return redirect(url_for('settings'))
    
    # ارسال مقادیر فعلی پیکربندی به قالب
    geko_path = config_manager.get_setting('Paths', 'GeckoPath')
    db_path = config_manager.get_setting('Paths', 'DBPath')
    driver_type = config_manager.get_setting('Setting', 'DriverType')
    headless_mode = config_manager.get_setting('Setting', 'HeadlessMode') == 'true'
    
    return render_template('index.html', geko_path=geko_path, db_path=db_path, driver_type=driver_type, headless_mode=headless_mode)

if __name__ == '__main__':
    app.run(debug=True)