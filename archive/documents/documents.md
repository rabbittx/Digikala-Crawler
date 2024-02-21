[read in english](documents.md)
<div dir='rtl'>
## Project Introduction
The Digikala Crawler project is a tool for extracting information from the Digikala online store website. This project allows you to extract information related to sellers, products of each seller, and complete details of each product and save it in a database. In addition, this project provides the capability to export the information in Excel file format.

Considering the importance of having access to a comprehensive database of seller information and products, I decided to develop this project. This database can serve as a resource for machine learning, data analysis, and the development of various projects. The first step in this direction was to develop the crawler section and the information storage capabilities in the database, thereby laying the groundwork for use in APIs, machine learning models, and more complex analyses.

### Features and Capabilities
In its first phase, this project provides the capability to extract and store information through two user panels; one under the console and the other under the web. It enables the extraction of information individually or in groups through the product address or seller page, as well as the collective extraction of information based on categories or specific searches.

At this stage, the extracted information can be stored in the database and exported in CSV format, allowing for the analysis and review of data under different conditions. This can be done through the output menu in both console and web modes.

### Installation Guide
To set up and use this project after cloning it from GitHub, you need to create a virtual environment for installing and setting up the necessary libraries for this project. After installing and setting up the virtual environment and libraries, by launching one of the panels, you can perform the necessary configurations, which include web driver addressing, database addressing, browser type selection, and browser operation mode as either normal or in the background. Then, you can access the executed panel and start extracting information from Digikala. Once the extraction is completed, you can use the output menu to receive the required csv file output.
```bash
git clone https://github.com/rabbittx/Digikala-Crawler.git
cd Digikala-Crawler
python -m venv env
source env/bin/activate # For Linux
env/Scripts/activate # For Windows
pip install -r requirements.txt
# Execute one of the panels. Console panel or web panel
python console_panel.py # To use the console panel
python app.py # To use the web panel
```

After running the panel, you need to configure the crawler:

    archive\gekcodrive\firefox\geckodriver.exe (suggested path): web driver address
    archive\dataBase\digikala_database.db (suggested path): database address
    firefox, chrome: browser type
    Browser usage type: headless mode, normal mode

After configuring the crawler with the executed panel, you can start extracting and use the output menu to produce the desired output file in csv format.
Usage Guide

## Console Panel

After configuring the crawler and accessing the menus, you can start extracting information. By selecting the desired option:

    Main crawler menu
        1: Start extracting a category or specific search using the page address
        2: Start extracting information of a seller using the seller's page address
        3: Start extracting complete product information of a seller with all details using the ID saved in the database (this option requires that the seller's page has been previously extracted)
        4: Complete extraction of product information with full details using the product page address
        5: Start extracting complete information of all products saved in the database (in this method, the information of products saved in the database is extracted one by one with all details)
        6: Access the output menu with CSV format
        7: View a full report of the information saved in the database tables
        8: Reconfigure the crawler
        9: Stop and exit the crawler
        help: Display the help menu

    Output menu with CSV format
        1 : Receive complete information of all sellers
        2 : Receive complete product information of a seller using the ID saved in the database (this method requires that IDs are available in the database)
        3 : Receive complete information of products saved in the database
        4 : Receive complete information of a seller's products with all details using the ID (this method requires that IDs are available in the database)
        5 : Receive complete information of all products with full details
        6 : Receive all information saved in the database
        7 : Return to the main menu

## Web Panel

In the web panel, sections and features similar to the console panel are available, and all sections are clearly marked in separate boxes, accessible and usable by clicking on the submit buttons of each section.

## Examples of Usage

In the console panel, examples needed for obtaining page addresses in each section are displayed, and in the web panel, by clicking on the help option in the navbar, you can view sample addresses. Also, sample addresses required for each section are placed in the placeholder of each input field.

## Project Structure
```bash
.
├── README.fa.md # Initial documentation and setup guide for the project in Persian
├── README.md # Initial documentation and setup guide for the project in English
├── TODOS.py #
├── app.py # Web user interface file (web panel)
├── archive # Archive folder
│   ├── dataBase # Database archive folder
│   │   └── digikala_database.db # Main database file (default address for the database in this path but can be changed in configuration)
│   ├── documents # Project documentation folder
│   │   ├── documents.fa.md # Documentation file in Persian
│   │   ├── documents.md # Documentation file in English
│   │   ├── functions.fa.md # Complete function documentation file in Persian
│   │   ├── functions.md # Complete function documentation file in English
│   │   └── www.digikala.com.png # An image of the product page and different sections for extraction
│   ├── gekcodrive # Web driver storage folder
│   │   ├── chorme # Chrome web driver storage folder
│   │   │   └── chromedriver.exe # Chrome web driver file with default address, you can change this address in the configuration
│   │   └── firefox # Firefox web driver folder
│   │       ├── geckodriver.exe # Firefox web driver file, you can change this default address in the configuration
│   │       └── geckodriver.log # Web driver log file
│   └── logs # Project log storage folder
│       └── web_crawler_logs.log # Log storage file used for displaying logs in the web panel (storing web panel logs)
├── console-config.ini # Configuration file for the console panel
├── console_panel.py # Console panel execution file
├── requirements.txt # Required libraries file for the project
├── source # Project source code storage folder
│   ├── config.py # Classes and functions for configurations file
│   ├── db_handler.py # Classes and functions related to database control file
│   ├── driver_manager.py # Classes and functions for web driver control
│   ├── logger.py # Classes and functions for log system control
│   ├── product_details_extractor.py # Classes and functions related to extracting information from seller page and seller products
│   ├── seller_product_data_extractor.py # File related to extracting complete information from the product page with full details
│   └── webScraper.py # Classes and functions for crawler control
├── static # Static files storage folder related to the web user interface
│   ├── css # Styles storage folder
│   │   └── style.css # Web user interface styles storage file
│   └── js # JavaScript scripts storage folder
│       └── scripts.js # JavaScript scripts storage file
├── templates # Web user interface page structure storage folder
│   ├── base.html # Page structure file
│   ├── footer.html # Page footer file
│   ├── header.html # Page header file
│   ├── index.html # Main page of the web user interface
│   └── settings.html # Crawler settings and configuration file
└── web_config.ini # Web user interface configuration file
```

## How to Contribute

We welcome everyone interested in contributing to this project. If you wish to propose changes or improvements, please follow these steps:

    First, Fork the project.
    Then, create a new Branch for your changes (git checkout -b feature/AmazingFeature).
    Commit your changes (git commit -m 'Add some AmazingFeature').
    Push your Branch to GitHub (git push origin feature/AmazingFeature).
    Submit a Pull Request.

## Contribution Rules

    Adhere to coding standards: Please follow PEP 8, the official coding style guide for Python code, to keep the code readable and consistent.
    Testing: Before submitting a Pull Request, please run the tests and ensure all tests pass successfully.
    Documentation: If your changes require an update to the documentation, please update the documentation accordingly.

# License

This project is released under the GNU General Public License v3.0. This means you are free to copy, modify, distribute, and/or publish the code, provided that any changes and extensions also remain under this license. For more information on the terms and conditions of use, please refer to the full text of the license.

## Support and Community
# Communication Channels

We are committed to creating a supportive and active community for this project. If you have questions, need assistance, or want to discuss project development, you can connect with us and other users through the following means:

    Telegram Channel: We have a Telegram group where project news and updates are shared: [[Telegram Link]](https://t.me/+WQuE2hAke0FjZjI0).

## License

This project is released under the GNU General Public License v3.0. GPL v3 is a public license that allows anyone to copy, distribute, and/or modify the project's source code under specific conditions that ensure the fundamental freedoms for all users are preserved.
Summary of GPL v3 Main Conditions:

    Freedom to run the program for any purpose.
    Freedom to study how the program works, and change it so it does your computing as you wish. Access to the source code makes this freedom possible.
    Freedom to redistribute copies to help others.
    Freedom to distribute your modified versions of the program, ensuring the community benefits from your improvements. Access to the source code is necessary for this freedom.

By using GPL v3, you are not only allowed to use and modify the code, but also obliged to distribute any distribution or modified version of the code under the same license, preserving the fundamental freedoms for all users.

For more information about GPL v3 and its specific terms, refer to the full text of the license.

    This project is strictly for educational purposes, data gathering for use in machine learning models, data analysis, and creating a database for learning. Please refrain from using this project to increase traffic on Digikala servers or any activity that could potentially harm them.
    The timers set for extracting information in the source code should not be reduced to prevent excessive load on Digikala servers.
    The developers are not responsible for any malicious behavior or misuse of this project.

