[Read this in Persian](README.fa.md)
Sure, here's the translation of your README.md file into English:
Introducing Digikala

=======================
Digikala is a prominent online store in Iran, known for its extensive range of products and services. Initially focused on selling electronic and digital devices, over the past 15 years, it has evolved into a comprehensive e-commerce platform with a diverse range of product categories. This expansion has made Digikala one of the leading e-commerce platforms in the Middle East.

Digikala has transformed into a complete ecosystem of online businesses, not just limited to e-commerce. This group has focused on completing the value chain of Iran's digital economy and has provided the necessary infrastructures for various types of businesses. Their activities include content production, logistics, financial technology, marketing technology, and cloud technology. With its wide access and comprehensive services, Digikala meets the diverse needs of its customers.
Key Statistics and Achievements of Digikala include:

    Over 41.5 million active monthly users.
    More than 9.7 million SKUs (Stock Keeping Units).
    Collaboration with over 308,000 sellers.
    Significant presence in logistics and distribution with more than 530 infrastructure centers.
    Strong fulfillment capacity, capable of handling over 904,000 orders daily.
    Expanding product variety, with a 29% growth last year.
    Diverse subsidiaries and services, including Fidibo (an e-book store), Digistyle (an online fashion and clothing store), Digipay (focusing on mobile and web payments), and Pindo (a consumer-to-consumer advertising platform).

The success of Digikala is largely due to its commitment to ensuring a positive online buying and selling experience. The company regularly monitors product quality and pricing and actively responds to user feedback and reports to maintain high standards.
Project Introduction

=======================
Project Title: Digikala Web Crawler
Project Introduction:

The Digikala Web Crawler project is a comprehensive and flexible system for collecting and analyzing data from the Digikala online store. Developed in Python, this system is capable of extracting information related to sellers and products from Digikala's web pages. The primary goal of this project is to provide a powerful tool for competitive analysis and precise business decision-making.
Key Features:

db_handler.py:
Manages the SQLite database for storing and manipulating collected data.

crawler.py:
The main crawler script that uses Selenium and BeautifulSoup to extract the required data.

panel.py:
A text-based user interface (CLI) that allows users to control the crawler process and export data to CSV format.

logger.py:
A logging system for tracking crawler operations and debugging.
Uses and Benefits:

This project is a powerful tool for traders and market analysts looking to better understand the market and competitors' behavior. Using this crawler, users can analyze prices, review product inventory, and gain a better understanding of seller performance. The system can also identify new market opportunities and improve sales strategies.
Project Setup

=======================
Step 1: Install Python

Ensure that Python version 3.x is installed on your system. Use the following command to check the Python version:

```bash

python --version
```
Step 2: Clone the Project Repository

Clone the project from the relevant repository (assuming the project is in a Git repository):

```bash

git clone 
cd DIGIKALA
```
Step 3: Create a Virtual Environment

To prevent conflicts between libraries, create a virtual environment:

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
Step 6: Set Up the Environment File (env)

Download the geckodriver.exe file required for the Firefox browser and place it alongside the project.
Step 7: Run the Project

Execute the panel script to start the project:

```bash
python panel.py
```

Step 8: Using the Project

In the displayed panel, first select option 1, then enter the URL of the category you want to extract data from, followed by the amount of page scroll. After completion, you can receive a CSV file output using option 2 and stop the project with option 3.
