import sqlite3

class dataBaseHandler():
    def __init__(self,db_path) :
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        # Create a table for seller information
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS sellers (
            crawl_date TEXT,                 
            seller_name TEXT,
            seller_id TEXT PRIMARY KEY,
            membership_period TEXT,
            satisfaction_with_goods TEXT,
            seller_performance TEXT,
            people_have_given_points TEXT,
            timely_supply TEXT,
            obligation_to_send TEXT,
            no_return TEXT,
            introduction_of_the_seller TEXT
        )
        ''')

        # Create a table for product details
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            crawl_date TEXT,
            seller_name TEXT,
            product_id TEXT PRIMARY KEY,
            product_link TEXT,
            product_image TEXT,
            product_rate TEXT,
            product_name TEXT,
            product_price TEXT,
            product_price_discount_percent TEXT,
            product_price_discount TEXT,
            product_special_sale TEXT,
            stock TEXT
        )
        ''')
    def close_connction(self):
        self.conn.close()

dataBaseHandler('digikala.db').create_tables()