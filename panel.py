from crawler import WebScraper
class WebScraperPanel:
    def __init__(self, scraper):
        self.scraper = scraper

    def display_menu(self):
        print("welcome to digikala web crawler")
        print("1. start to crawl")
        print("2. quit")
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

    def start(self):
        while True:
            choice = self.display_menu()
            if choice == "1":
                self.run_scraper()
            elif choice == "2":
                print("Exit the program.")
                break
            else:
                print("Invalid option, please try again.")

if __name__ == "__main__":
    geko_path = r'geckodriver.exe' # path to geckodriver.exe
    scraper = WebScraper(geko_path)
    panel = WebScraperPanel(scraper)
    panel.start()
