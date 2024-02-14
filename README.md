[Read in persian](README.fa.md)

# Introduction to Digikala
Digikala is a leading online store in Iran, recognized for its wide variety of products and services. Initially focused on selling electronic and digital items, over the past 15 years, it has transformed into a comprehensive e-commerce platform offering a diverse range of product categories. This expansion has made Digikala one of the leading e-commerce platforms in the Middle East.

Digikala has evolved into a complete ecosystem of online businesses that extends beyond just e-commerce. The group's focus has been on completing the value chain of Iran's digital economy, providing the necessary infrastructure for various types of businesses. Their activities include content production, logistics, financial technology, marketing technology, and cloud technology. With its wide access and comprehensive services, Digikala meets the diverse needs and populations of its customers.

## Key Statistics and Achievements of Digikala include:

* Over 41.5 million active monthly users.

* More than 9.7 million SKUs (Stock Keeping Units).

* Collaborations with over 308,000 sellers.

* A significant presence in logistics and distribution with over 530 infrastructure centers.

* Strong fulfillment capacity, capable of handling more than 904,000 orders daily.

* An expanding product range that saw a 29% growth last year.

* A variety of subsidiaries and services, including Fidibo (an e-book store), Digistyle (an online fashion and clothing store), Digipay (focused on mobile and web payments), and Pindo (a consumer-to-consumer advertising platform).

Digikala's success is largely due to its commitment to ensuring a positive online buying and selling experience. The company regularly monitors product quality and pricing and actively responds to feedback and reports from users to maintain high standards.

## Project Introduction
### Project Title: Digikala Web Crawler

### Project Overview:
The Digikala Web Crawler project is a comprehensive and flexible system for collecting and analyzing data from the Digikala online store. Developed in Python, this system can extract information about sellers and products from Digikala web pages. The main goal of this project is to provide a powerful tool for competitive analysis and accurate business decision-making. With this project, you will be able to extract information about sellers and products and create a history for them. Should any changes occur in product or seller information, the previous data will be stored in history tables for review.

### Main Features:

* `db_handler.py`: Manages the SQLite database for storing and manipulating collected data.

* `driver_manager.py`: Creates and manages driver operations.

* `product_details_extractor.py`: Extracts product page information from Digikala and sends the data to db_handler.

* `seller_product_data_extractor.py`: Extracts category page information and seller information, and sends the data to db_handler.

* `webScriper.py`: A file to create a crawler object and use the extraction functions.

* `console_panel.py`: A Command Line Interface (CLI) that allows the user to control the crawler process and export data in CSV format.

* `app.py`: A web-based user interface using Flask (under development).

* `logger.py`: A logging system to track crawler operations and debug.

* `TODOS.py`: A file for organizing to-do lists and bugs.

### Applications and Benefits:

This project is a powerful tool for merchants and market analysts looking to gain a better understanding of the market and competitor behavior. With this crawler, users can analyze prices, check product inventory, and gain a better understanding of seller performance. The system can also help identify new market opportunities and improve sales strategies.

* Extracting seller and product information and storing data in inventory and history tables.
* Outputting data in CSV format.

### Project Setup
#### Step 1: Install Python

Ensure Python version 3.x is installed on your system. Use the following command to check your Python version:

```bash
python --version
```
Step 2: Clone the Project Repository

Clone the project from its repository (assuming the project is in a Git repository):

```bash

git clone https://github.com/rabbittx/Digikala-Explorer.git
cd Digikala-Explorer
```
Step 3: Create a Virtual Environment

To avoid library conflicts, create a virtual environment:

```bash

python -m venv env
```
Step 4: Activate the Virtual Environment

Activate the virtual environment:

On Windows:

```bash

venv\Scripts\activate
```
On macOS and Linux:

```bash

source venv/bin/activate
```
Step 5: Install Dependencies

Install the project dependencies using the requirements.txt file:

```bash

pip install -r requirements.txt
```
Step 6: Set up the Environment File

Install Geckodriver:
First, download geckodriver for your browser:
[fireFox]('https://github.com/mozilla/geckodriver/releases')
[chrome]('https://chromedriver.chromium.org/downloads')
and place it in your desired location or alongside the project.
Suggested path alongside the project:
- archive\gekcodrive\firefox\geckodriver.exe
- archive\gekcodrive\chrome\chromedriver.exe

Step 7: Run the Project

Run the script panel to start the project:

```bash

python console_panel.py
```
Step 8: Use the Project

After the first run, you need to add the required settings. Specify the path of your web driver and the database location (the database is created automatically, you just need to enter an address for storage):

   - Suggested path for the database:
    archive\dataBase\digikala_database.db
    Also, specify which browser you are using, Firefox or Chrome, and then the project is ready to use.
    From the displayed menu, select your desired option. You can also choose whether you want the browser to run in the background or normally. After extracting the needed information, you can use the output menu to receive your data in a CSV file.

Note

===========

    * The version of the web driver must match your browser version; otherwise, you will encounter errors.
    * To avoid placing an excessive load on Digikala's servers, timing considerations have been made. Please do not remove or reduce them.
    * Please refrain from running multiple scripts simultaneously to speed up extraction.

## Future of the Project
### Planned Features

 - [ ] Adding integration with other browsers.
 - [ ] Adding the feature to display output in different formats.
 - [ ] Creating unit tests for different parts.
 - [ ] Adding an API to use main components in other applications.
 - [ ] Web user interface using Flask.

## Performance Improvements

- [ ] Optimizing memory usage.
- [ ] Improving project performance on different systems.
- [ ] Enhancing the speed and efficiency of algorithms.

## User Experience Development

 - [ ] Expanding setting options and features in the panel.
 - [ ] Creating a graphical user interface for easier interaction.
 - [ ] Adding navigation and guidance to the user manual.

## Security and Stability

 - [ ] Examining and improving security regarding user inputs.
 - [ ] Adding better error management and reporting.
 - [ ] Testing and fixing existing bugs.