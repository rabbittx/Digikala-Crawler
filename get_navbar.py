from driver_manager import DriverManager
from logger import setup_logger
import time
log = setup_logger()
driver = DriverManager(driver_path=r'geckodriver.exe',log=log)

url = 'https://www.digikala.com/'


def get_navbar(driver,url):
    driver.open_page(url)
    time.sleep(20)
    source = driver.get_page_source()

    with open('navbar.html','w',encoding='utf-8-sig') as file :
        file.write(str(source))


get_navbar(driver,url)
