from crawler import WebScraper
import csv ,sqlite3 , os
class WebScraperPanel:
    def __init__(self, scraper):
        self.scraper = scraper

    def display_menu(self):
        print("welcome to digikala web crawler")
        print("1. start to crawl")
        print("2. export all data in csv file ")
        print("3. quit")
        choice = input("enter your choice : ")
        return choice

    def run_scraper(self):
        category_url = input("enter catagory url to crawl: ")
        scroll_count = input("Please enter the number of page scroll rates (Example 5 ) : ")
        try:
            scroll_count = int(scroll_count)
        except ValueError:
            print("The number of scrolling times must be a number. By default, it is set to 3.")
            scroll_count = 3
        self.scraper.run(category_url,scroll_count)
        print("Data extraction was done successfully.")

    def export_table_to_csv(self,db_path, table_name, csv_file_path):
        if os.path.exists(csv_file_path):
            os.remove(csv_file_path)
        if os.path.exists(db_path):
                
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()   
            cursor.execute(f"SELECT * FROM {table_name}")
            columns = [description[0] for description in cursor.description]
            with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(columns)
                for row in cursor.fetchall():
                    processed_row = [self.scraper.split_value(val) if isinstance(val, str) else val for val in row]
                    csv_writer.writerow(processed_row)
        else : 
            print(f'Database "{db_path}" does not exist! - crawl some pages first ')
            
    def start(self):
        while True:
            choice = self.display_menu()
            if choice == "1":
                self.run_scraper()
            elif choice == "2":
                self.export_table_to_csv(self.scraper.db_path, 'sellers', 'sellers.csv')
                self.export_table_to_csv(self.scraper.db_path, 'products', 'product.csv')
                print(' [!] CSV file create successfully')
            elif choice == "3":
                self.scraper.close_resources()
                print("Exit the program.")
                break
            else:
                print("Invalid option, please try again.")
    
if __name__ == "__main__":
    geko_path = r'geckodriver.exe' # path to geckodriver.exe
    scraper = WebScraper(geko_path)
    panel = WebScraperPanel(scraper)
    panel.start()
