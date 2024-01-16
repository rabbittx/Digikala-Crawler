import sqlite3

class DataBaseHandler():
    def __init__(self, db_path):
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

        # Create a table for extracted product details
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS products_extraction (
             crawl_date TEXT,               
            product_id TEXT PRIMARY KEY,
            product_link TEXT ,
            main_product_details TEXT ,
            buy_box TEXT ,
            product_images TEXT ,
            other_seller TEXT ,
            similar_products TEXT ,
            related_videos TEXT ,
            introduction_box TEXT ,
            expert_check TEXT ,
            specifications_box TEXT ,
            reviews TEXT ,
            question_box TEXT ,
            also_bought_items TEXT ,
            seller_offer TEXT
        )
        ''')

    # TODO fix all function to use them from here ! 
        # FROM CRAWLER.py
    def split_value(self,intput):
        return intput if ';' not in intput else intput.split(';')[-1]

    def check_field_value(self,row_data, crawl_data):
            for key in row_data:
                if key != 'crawl_date' and key != 'product_image'  :
                    row_value = row_data[key].split(';')[-1] if ';' in row_data[key] else row_data[key]
                    if row_value != crawl_data[key]:
                        return True
            return False

    def update_or_insert_seller(self, seller_data):
        row_id = self.split_value(seller_data['seller_id'])
        self.cursor.execute('SELECT * FROM sellers WHERE seller_id = ?', (row_id,))
        existing_row = self.cursor.fetchone()
        if existing_row:
            # Create a dictionary from the existing row
            existing_data = {col[0]: val for col, val in zip(self.cursor.description, existing_row)}
            # Check if the data needs to be updated
            if self.check_field_value(existing_data, seller_data):
                updated_data = {}
                for key, value in seller_data.items():
                    if key in existing_data and existing_data[key] is not None:
                        updated_data[key] = existing_data[key] + ";" + value
                    else:
                        updated_data[key] = value
                self.update_data('sellers', updated_data, 'seller_id', row_id)
        else:
            self.insert_data('sellers', seller_data)
    
    def update_or_insert_product(self, product_data):
        row_id = self.split_value(product_data['product_id'])
        self.cursor.execute('SELECT * FROM products WHERE product_id = ?', (row_id,))
        existing_row = self.cursor.fetchone()
        if existing_row:
            existing_data = {col[0]: val for col, val in zip(self.cursor.description, existing_row)} 
            if self.check_field_value(existing_data, product_data):
                    updated_data = {}
                    for key, value in product_data.items():
                        if key in existing_data and existing_data[key] is not None:
                            updated_data[key] = existing_data[key] + ";" + value
                        else:
                            updated_data[key] = value
                    self.update_data('products', updated_data, 'product_id', row_id)
        else:
            self.insert_data('products', product_data)

    def update_data(self, table_name, data, key_field, key_value_field):
        set_clause = ', '.join([f"{k} = :{k}" for k in data])
        data[key_field] = key_value_field  
        try:
            self.cursor.execute(f'UPDATE {table_name} SET {set_clause} WHERE {key_field} = :{key_field}', data)
            self.conn.commit()  
        except Exception as e:
            self.log.error(f'Error during updating data in {table_name}: {e}')
            raise

    def insert_data(self, table_name, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join([f":{k}" for k in data])
        try:
            self.cursor.execute(f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})', data)
            self.conn.commit()  
        except Exception as e:
            self.log.error(f'Error during inserting data into {table_name}: {e}')
            raise

    def save_to_database(self,  data):
                self.update_or_insert_seller(data[0])
                for product in data[1]:
                    product['seller_name'] = data[0]['seller_name']
                    self.update_or_insert_product(product)
#-----------------------------------------------------------------------
         # TODO fix all function to use them from here
             # FROM PRODUCTS_EXTRACTION.py 
    
    def update_or_insert_extraction(self, extraction_data):
        row_id = self.split_value(extraction_data['product_id'])
        self.cursor.execute('SELECT * FROM products_extraction WHERE product_id = ?', (row_id,))
        existing_row = self.cursor.fetchone()
        if existing_row:
            existing_data = {col[0]: val for col, val in zip(self.cursor.description, existing_row)}
            if self.check_field_value(existing_data, extraction_data):
                updated_data = {}
                for key, value in extraction_data.items():
                    if key in existing_data and existing_data[key] is not None:
                        updated_data[key] = existing_data[key] + ";" + value
                    else:
                        updated_data[key] = value
                self.update_or_insert_data('products_extraction', updated_data, 'product_id', row_id)
        else:
            self.insert_data('products_extraction', extraction_data)

    def update_or_insert_data(self, table_name, data, key_field, key_value_field):
        set_clause = ', '.join([f"{k} = :{k}" for k in data])
        data[key_field] = key_value_field  
        try:
            self.cursor.execute(f'UPDATE {table_name} SET {set_clause} WHERE {key_field} = :{key_field}', data)
            self.conn.commit()  
        except Exception as e:
            self.log.error(f'Error during updating data in {table_name}: {e}')
            raise

    def insert_data(self, table_name, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join([f":{k}" for k in data])
        try:
            self.cursor.execute(f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})', data)
            self.conn.commit()  
        except Exception as e:
            self.log.error(f'Error during inserting data into {table_name}: {e}')
            raise

    def save_to_database(self, product_info):
        self.update_or_insert_extraction(product_info)
#-----------------------------------------------------------------------


    def close_connection(self):
        self.conn.close()

if __name__ == '__main__':
    # TODO optimize all function about store data in tables here and use them from here !
    
    db_path = 'digikala.db'
    DataBaseHandler(db_path).create_tables()
    