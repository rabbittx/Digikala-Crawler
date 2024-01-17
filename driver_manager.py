# TODO install driver here 
from selenium import webdriver

class DriverManager:
    def __init__(self, driver_path):
        self.log.info('Initializing Web Scraper...')
        self.driver = self.initialize_driver(driver_path)

    def initialize_driver(self, driver_path):
        try:
            service = Service(driver_path)
            driver = webdriver.Firefox(service=service)
            self.log.info('Web driver initialized successfully')
            return driver
        except Exception as e:
            self.log.error(f'Error initializing web driver: {e}')
            raise

    def close_driver(self):
        if self.driver:
            self.driver.quit()

