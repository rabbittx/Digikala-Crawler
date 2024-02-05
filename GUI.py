from flask import Flask, render_template, request, jsonify
from panel import WebScraperPanel, ConfigManager  # نام ماژول شما را وارد کنید
from logger import setup_logger
app = Flask(__name__)
log = None
web_scraper_panel = None
config_manager = None


from flask import Flask, render_template, jsonify
import time

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

log_messages = []

def log_activity(message):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f'[{timestamp}] {message}'
    log_messages.append(log_entry)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/get_logs')
def get_logs():
    return jsonify(log_messages)

if __name__ == '__main__':
    app.run(debug=True)