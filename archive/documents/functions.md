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


# ProductDetailsExtractor Class Documentation

The `ProductDetailsExtractor` class is designed to extract product details from a given HTML page.

## Introduction

```python
ProductDetailsExtractor(driver, db_handler, log)
```
  - `driver`: The web driver instance used to load web pages and perform browser operations.
  - `db_handler`: An instance of the `DataBaseHandler` class for database operations.
  - `log`: An instance of the `Logger` class for logging messages.

## Methods
`clean_text(text)`

This method is used to remove unwanted characters and return the cleaned text.

`check_with_multi_class_name(element, field_name, tag_name, attrs_name, attrs_list)`

This method is used to find an element with multiple class names.

`safe_find(soup, finds, tag, attrs)`

This method is used to safely find elements using BeautifulSoup, using try-catch blocks to avoid exceptions.

`safe_extraction(element_name, element, extraction_function)`

This method is used to safely call an extraction function by passing the required arguments and handling errors.

`product_elements_extraction(soup)`

This method extracts all necessary product elements from an HTML page using the BeautifulSoup library.

`main_product_details_extraction(element)`

This method extracts the main product details from a div element.

`product_buy_box_extraction(element)`

This method extracts product buy box details from a div element.

`product_image_extraction(element)`

This method extracts product image URLs from img tags in the HTML page.

`other_seller_box_extraction(element)`

This method extracts information about other sellers offering the product from an HTML element.

`similar_products_extraction(element)`

This method extracts information about similar products from the product description page.

`related_videos_extraction(element)`

This method extracts information about related video reviews.

`expert_check_box_extraction(element)`

This method extracts information about the experts' checkbox from the page.

`specifications_box_extraction(element)`

This method extracts product specification information from the page.

`reviews_box_extraction(element)`

This method extracts review data from the page.

`question_box_extraction(element)`

This method extracts question and answer data from the page.

`also_bought_items_extraction(element)`

This method extracts "also bought" items from the product description page.

`seller_offer_extraction(element)`

This method extracts seller offer items from the product description page.

`page_extraction(product_id, product_url)`

This method extracts all relevant data from a single webpage.

`check_not_empty(data)`

This method is used to check if any field is empty.

`run(url)`

This method starts the data extraction process from a specific product URL.

## `seller_product_data_extractor.py` : 

# SellerProductDataExtractor Class Documentation

The `SellerProductDataExtractor` class is designed to extract the necessary data from a seller's product listing.

## Constructor

```python
SellerProductDataExtractor(driver, db_handler, log)
```
  - `driver`: The web driver instance used for accessing web pages.
  - `db_handler`: An instance of the database handler for performing database-related operations.
  - `log`: An instance for logging events and process-related information.

## Methods

`has_desired_text(tags, find_text)`

Checks if any of the given tags contain the specified find_text.

`seller_details(soup)`

Extracts and returns details about the seller from the given BeautifulSoup object.

`extract_product_details(product)`

Extracts information about a single product (price, discount price, description) from a product element.

`check_category(url, scroll_count)`

Extracts data from a category page on Digikala based on the provided URL and the number of times to scroll down the page to load all products.

`check_seller(url)`

Extracts details of a specific seller using the provided URL.

## `driver_manager.py` : 

The DriverManager class is designed for initializing and managing a web browser driver and extracting data from web pages.
Method `__init__(self, driver_path, log, headless_mode, driver_type)`

This method initializes the web browser driver.

  - `driver_path`: Path to the web browser driver
  - `log`: A logger object for logging events
  - `headless_mode`: If set to True, the browser will run in headless mode (without a graphical interface)
  - `driver_type`: Type of browser (firefox or chrome)

Method `initialize_driver(self, headless_mode)`

This method initializes the web browser driver based on the selected browser type and headless mode.

Method `load_page(self, url)`

This method loads a web page using the provided URL and sets it as the active page for subsequent actions.

Method `get_page_source(self)`

This method returns the source code of the current page as a BeautifulSoup object.

Method `get_prdoucts_on_page(self, page_source, return_value)`

This method parses the provided HTML content to find products on a webpage.

Method `get_seller_id(self)`

This method extracts the seller ID from the product detail page.

Method `close_driver(self)`

This method is used to close the driver.

## `db_handler.py` : 

Method `__init__(self, db_path, log)`

This method initializes the database and connects to it.

  - `db_path`: The path to the database file
  - `log`: An object for logging events

Method `create_tables(self)`

This method creates the necessary tables in the database if they do not already exist.

Method `get_next_id(self, table_name, fields_id, id_name)`

This method is used to get the next ID for auto-increment in SQLite.

Method `get_row_info(self, fields, table_name, condition=None, return_as_list=False)`

This method is used to extract information from the database based on specific conditions and fields requested by the user.

Method `get_connection(self)`

This method is used to connect to the database.

Method `get_sellers(self)`

This method extracts sellers from the database.

Method `get_column_names(self, table_name)`

This method returns the names of columns of a specified table.

Method `check_field_value(self, row_data, crawl_data)`

This method checks whether a specific field has been filled or not.

Method `check_existing_data(self, row_id, column_name, table_name)`

This method is used to check fields in the database whether they have been updated or not.

Method `parse_json_fields(self, record)`

This method parses fields into JSON.

Method `replace_recode_to_history_table(self, data, column_name, table_name)`

This method moves old data from the main table to the history table.

Method `insert_recode_to_table(self, data, table_name)`

This method adds a new line or updates an existing one in a specified table. If there is already a record with the same ID, it updates the record; otherwise, it creates a new one.

Method `update_database(self, data, column_name, table_name)`

This method updates records in a table based on a column.

Method `close_connection(self)`

This method closes the connection to the database.

## `logger.py` : 

Function `setup_logger`

This function is used to set up the general logger for the application.
Returns:

  - Logger object

How it works:

  - Creates a logger object named "DigikalaCrawler".
  - Sets the logger level to DEBUG.
  - Adds a handler to output log messages to the console.
  - Creates a formatter to specify the format of the log messages and adds it to the handler.

Function `web_setup_logger`

This function is used for setting up a specific logger for the web part of the application.

Returns:

  - Logger object

How it works:

  - Creates a logger object named "DigikalaCrawler".
  - Sets the logger level to DEBUG and disables propagation to prevent duplicate logs.
  - Creates a file handler to save logs in a log file.
  - Specifies a format for log messages and adds it to the file handler.

These functions are used to record and maintain information related to activities and errors of the application during execution, facilitating event analysis and troubleshooting.

## `console_panel.py` : 

This section pertains to the console panel for the Digikala Scraper, enabling you to execute scraping operations on Digikala through a console interface.

`__init__` Function

This function initializes the console panel, creating an instance of DigiKalaScraper using the specified logger and configuration file path.

`menus` Function

This function defines different menus for selecting various operations for the scraper, including crawling for a category, a specific seller, and exporting data in CSV format.

`crawl_options` Function

Based on the user's selection, this function executes the corresponding scraping operation. Each option relates to a specific mode of scraping and invokes the relevant functions.

`show_help` Function

This function provides guidance on how to use the Digikala-Crawler effectively, offering information on configuration, execution of different operations, and accessing documentation for further assistance.

`reconfig` Function

This function allows for the reconfiguration of the scraper if there's a need to change initial settings.

`show_examples` Function

It displays examples of URLs that can be used for scraping, making it easier for users to input valid URLs.

`csv_export` Function

Enables exporting collected data into CSV format.

`database_report_show` Function

Presents a comprehensive report of the data stored in the database, including the count of records in different tables.

`get_crawl_input` Function

Collects necessary inputs from the user to start the scraping operation.

`show_menu` Function

Displays a menu of different options to the user, allowing for the selection of various operations.

`run` Function

The main function for running the console panel, controlling the core logic of the program, including receiving inputs and executing different operations.

This class provides users with the ability to run various operations on the Digikala Scraper through a simple console interface, collecting desired data effectively.

## `app.py` : 

### Initialization

The `WebGUIApp` class initializes with a configuration file path and a logger. It creates a Flask application and defines routes for various scraper functionalities.

### Route Definitions

  - The `/` route displays the main page where users can start different types of crawls or go to settings.
  - The `/settings` route allows users to configure the scraper settings through a web form.
  - The `/get-logs` route shows the latest logs from the scraper.
  - Routes like `/start-category-crawl`, `/start_single_seller`, `/start_single_product`, and `/all_products` are endpoints for starting specific types of crawls 
   based on user input from the web interface.
  - Export routes (`/export_all_seller_data`, `/export_seller_products_id`, `/export_all_products`, etc.) allow users to export collected data to CSV files.
  - The `/report` route provides a comprehensive report of the database, showing the number of records in various tables.

### Methods

  - `add_routes` method defines all the endpoints and their functionalities.
  - `crawl_options` executes specific crawling tasks based on the mode selected by the user through the web interface.
  - The `run` method starts the Flask application, making the web interface accessible through a browser.

This setup provides an easy-to-use web interface for interacting with the DigiKala Scraper, making it more accessible to users without requiring direct interaction with the console or code.


## `TODOS.py` : 

This file outlines the planning and tracking of tasks to be done on the Digikala Scraper project, including updates, fixes, and planned additions.
DOCUMENTS / README

  - Update the README for the new version (GUI).
  - Update the documents to demonstrate how this project works and what can be achieved with it.

CONFIG

  - Add Docker to the project (planned).
  - Add test units (planned).

PANELS

  - Check for internet connection before starting the panel.
  - In the web panel, there's a bug where the report prints twice at the start but only once for the rest of the program.
  - In the console panel, an option to reset settings and reconfigure everything has been added (fixed).

db_handler.py

  - Fixed a bug where `get_next_id` needed to be the same when data needed to be replaced with the historical table.

driver_manager.py

  - Check for 404, 503 pages and product not available page on `open_page()`.
  - Before getting `page_source` in driver_manager, need to check if products are in loading... wait for it to load.
  - With full scrolling on the seller page, get products of 10 pages at once, need to add more pages to get all products from the seller.

logger
products_details_extractor.py

  - Currently, 20 items are received in reviews and questions. To get more items, if available, click on the next page button, get source and add it to temp in a loop.

seller_product_data_extractor.py
webScraper.py

  - Regex patterns need to be updated to check if the link is valid (e.g., link starts with https, URL split tokens length, etc.).
  - All mode names need to be updated in all script files (fixed).

This file provides an overview of upcoming tasks, completed fixes, and future plans for enhancing and developing the Digikala Scraper.