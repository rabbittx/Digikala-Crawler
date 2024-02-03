[به فارسی بخوانید](README.fa.md)

# DIGIKALA Web Scraper
Introduction

DIGIKALA is a prominent online store in Iran, known for its extensive range of products and services. Initially focusing on the sale of electronic and digital items, DIGIKALA has evolved over the past 15 years into a comprehensive e-commerce platform with diverse product categories. This expansion has turned DIGIKALA into one of the leading e-commerce platforms in the Middle East.

DIGIKALA has transformed into a complete ecosystem of online businesses, extending beyond just e-commerce. The group's focus has been on completing the digital economic value chain, providing necessary infrastructure for various business types. Their activities include content production, logistics, financial technology, marketing technology, and cloud technology. With broad access and comprehensive services, DIGIKALA caters to the diverse needs of its customer base.
Key Statistics and Achievements of DIGIKALA:

  * Over 41.5 million active monthly users.

  * More than 9.7 million SKUs (Stock Keeping Units).

  * Collaboration with over 308,000 sellers.

  * Significant presence in logistics and distribution with over 530 infrastructure centers.

  * Strong fulfillment capacity, handling over 904,000 daily orders.

  * Expanding product diversity, with a 29% growth last year.

  * Subsidiaries and diverse services, including Fidibo (e-book store), DIGISTYLE (online fashion and clothing store), DIGIPEY (focused on mobile and webpayments), and Pindo (consumer-to-consumer advertising platform).

DIGIKALA's success is largely attributed to its commitment to ensuring a positive online buying and selling experience. The company consistently monitors product quality and pricing, actively responding to user feedback and reports to maintain high standards.
Project Overview

Project Title: DIGIKALA Web Scraper

Project Description:
The DIGIKALA Web Scraper project is a comprehensive and flexible system for collecting and analyzing data from the DIGIKALA online store. Developed in Python, this system can extract information related to sellers and products from DIGIKALA web pages. The main goal of this project is to provide a powerful tool for competitive analysis and informed business decisions. With this project, you can extract information about sellers and their products, create a history for them, and check them for any changes in product or seller information.

Key Features:
    
 + db_handler.py: Manages the SQLite database for storing and manipulating collected data.
    
 + driver_manager.py: Creates a driver and manages driver-related operations.
    
 + product_details_extractor.py: Extracts information from DIGIKALA product pages and sends the data to db_handler.
    
 + seller_product_data_extractor.py: Extracts information from category pages and seller pages, sending the data to db_handler.
    
 + panel.py: A text-based user interface (CLI) allowing the user to control the scraper process and export data to CSV format.
    
 + logger.py: Event logging system for tracking scraper operations and debugging.

Applications and Benefits:
This project serves as a powerful tool for merchants and market analysts seeking a better understanding of the market and competitors. Users can analyze prices, check product inventory, and gain a better understanding of seller performance. The system can also identify new market opportunities and improve effective sales strategies.

Usage:
After executing the panel script for the first time, you need to configure the necessary settings. Specify the paths for your web driver and database (the database is automatically created, and you only need to enter the address for storage). You should also indicate which browser you are using, either Firefox or Chrome. The project is ready for use after these configurations. Choose your desired option from the displayed menu, and you can choose whether the browser should run in the background or normally. After extracting the required information, you can obtain your desired data in a CSV file from the export menu.

Note:

 - The web driver version must match your browser version; otherwise, you will encounter errors.
 - To prevent overload on DIGIKALA servers, time intervals have been set; please do not delete or reduce them.
 - Avoid running multiple scripts simultaneously to speed up your extraction.

## Future of the Project

### Program Features

 - [ ] Adding integration with other browsers.
 - [ ] Adding the feature to display output in different formats.
 - [ ] Creating a test unit for different sections.
 - [ ] Adding an API for using main components in other applications.

### Performance Improvements

 - [ ] Optimizing memory usage.
 - [ ] Improving project execution performance on different systems.
 - [ ] Increasing the speed and efficiency of algorithms.

### User Interface Development
 
 - [ ] Increasing features and settings options in the panel.
 
 - [ ] Creating a graphical user interface for easier interaction.
 
 - [ ] Adding navigation and user guidance to the user guide.

### Security and Stability

 - [ ] Checking and improving security for user inputs.

 - [ ] Adding better error management and reporting.

 - [ ] Testing and fixing existing bugs.