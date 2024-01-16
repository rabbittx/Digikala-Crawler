# TODO install driver here 
from selenium import webdriver

class DriverManager:
    def __init__(self, driver_path):
        self.driver_path = driver_path
        self.driver = None

    def start_driver(self):
        # ... تنظیمات مربوط به راه‌اندازی درایور (مثل headless و ...) ...
        pass

    def close_driver(self):
        if self.driver:
            self.driver.quit()

