[به فارسی بخوانید](functions.fa.md)

### Class and functions

## `webScriper.py` : 
The `DigiKalaScraper` class is designed to facilitate web scraping operations on the Digikala website. It utilizes various components to extract information about sellers, products, and product details, and then stores this data in a database. This class also provides functionalities for exporting the data to CSV files and managing the web scraping process through different modes.

## Initialization
DigiKalaScraper(config_file_path, log)
  - config_file_path: Path to the configuration file. This file determines whether the scraper operates in console mode or web mode. 
  - log: Logger instance for logging messages throughout the scraping process.
  
### Methods
`_initialize_settings()`

Initializes scraper settings from the configuration file. Settings include database path, web driver path, headless mode option, and driver type.

`initialize_driver(geko_path, driver_type, headless_mode, db_handler, logger)`

Initializes the web driver for the scraping process.
  - `geko_path`: Path to the GeckoDriver.
  - `driver_type`: Type of the web driver (firefox or chrome).
  - `headless_mode`: Boolean indicating whether to run the browser in headless mode.
  - `db_handler`: Instance of the DataBaseHandler class.
  - `logger`: Logger instance.  

`get_sellers()` 

Retrieves a list of sellers from the database.

`show_sellers()`

Displays all sellers available in the database and allows user to pick a seller for crawling their products.

`check_crawl_url(mode, input_url)`

Validates the input URL based on the specified crawling mode.
  - `mode`: Crawling mode (SingleProductCrawlMode, SingleSellerCrawlMode, CategoryCrawlMode).
  - `input_url`: URL to be validated.

`initialize_crawl_for_products(available_products)`

Initializes the crawling process for a list of product URLs.
  - `available_products`: List of product URLs to crawl.

`execute_crawl(mode, input_url, scroll_count, seller_info=None)`

Executes the web scraping process based on the specified mode and settings.
  - `mode`: Crawling mode.
  - `input_url`: URL for the starting point of the crawl.
  - `scroll_count`: Number of times to scroll the page (if applicable).
  - `seller_info`: Optional seller information for targeted scraping.

`remove_old_file(filename)`

Removes an old file if it exists.
  - `filename`: Name of the file to be removed.

`save_to_csv(data, headers, filename)`

Exports data to a CSV file.
  - `data`: Data to be exported.
  - `headers`: Column headers for the CSV file.
  - `filename`: Name of the CSV file.

`export_table(table_name, seller_id=None, condition=None)`

Exports data from a specific table to a CSV file.
  - `table_name`: Name of the database table.
  - `seller_id`: Optional seller ID for filtering data.
  - `condition`: Additional conditions for data filtering.

`export_data_to_csv(export_mode, seller_id=None, seller_name=None)`

Manages the export of data to CSV files based on the specified mode.
  - `export_mode`: Mode of data export (all_seller, seller_products, etc.).
  - `seller_id`: Optional seller ID for targeted export.
  - `seller_name`: Optional seller name for targeted export.

`database_report()`

Generates a report of the database contents, including counts of sellers, products, and extracted information.

### Example Usage
```python
    logger = setup_logger()
    scraper = DigiKalaScraper(config_file_path="config/console_config.ini", log=logger)
    scraper.execute_crawl(mode="SingleProductCrawlMode", input_url="https://www.digikala.com/product/dkp-12345", scroll_count=3)
```
This documentation provides a comprehensive overview of the DigiKalaScraper class, its methods, and how to use them for web scraping operations on the Digikala website.


## `product_details_extractor.py` : 


## `seller_product_data_extractor.py` : 


## `driver_manager.py` : 


## `db_handler.py` : 


## `logger.py` : 


## `console_panel.py` : 


## `app.py` : 


## `TODOS.py` : 

