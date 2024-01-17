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

# -----------------------------------------------------------
# -------------------------- CLEAN CODE ---------------------------------

    def split_value(self,intput):
        return intput if ';' not in intput else intput.split(';')[-1]
    def check_field_value(self,row_data, crawl_data):
        for key in row_data:
            if key != 'crawl_date' and key != 'product_image'  :
                row_value = row_data[key].split(';')[-1] if ';' in row_data[key] else row_data[key]
                if row_value != crawl_data[key]:
                    return True
        return False

    def update_or_insert_data(self, data , data_key,table_name ):
        row_id = self.split_value(data[data_key])
        self.cursor.execute(f'SELECT * FROM {table_name} WHERE {data_key} = ?', (row_id,))
        existing_row = self.cursor.fetchone()
        if existing_row:
            # Create a dictionary from the existing row
            existing_data = {col[0]: val for col, val in zip(self.cursor.description, existing_row)}
            # Check if the data needs to be updated
            if self.check_field_value(existing_data, data):
                updated_data = {}
                for key, value in data.items():
                    if key in existing_data and existing_data[key] is not None:
                        updated_data[key] = existing_data[key] + ";" + value
                    else:
                        updated_data[key] = value
                self.update_data(table_name, updated_data, data_key, row_id)
        else:
            self.update_data(table_name, data)

    def update_data(self, table_name, data, key_field, key_value_field , query_name):

        try:
            if query_name == 'updating' :
                set_clause = ', '.join([f"{k} = :{k}" for k in data])
                data[key_field] = key_value_field  
                query = f'UPDATE {table_name} SET {set_clause} WHERE {key_field} = :{key_field}'
            elif query_name == 'inserting':
                columns = ', '.join(data.keys())
                placeholders = ', '.join([f":{k}" for k in data])
                query = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
            else :
                self.log.error('query name ERROR check the function input') 
                raise Exception
            self.cursor.execute(query, data)
            self.conn.commit()  
        except Exception as e:
            self.log.error(f'Error during {query_name} data in {table_name}: {e}')
            raise

    def save_to_database(self,  data, data_key_name,table_name):
        if table_name == 'sellers' or table_name == 'prdoucts' :
            self.update_or_insert_seller(data[0])
            for product in data[1]:
                product[data_key_name] = data[0][data_key_name]
                self.update_or_insert_product(product)
        elif table_name == 'products_extraction' :
            self.update_or_insert_extraction(data)


    def close_connection(self):
        self.conn.commit()
        self.conn.close()

if __name__ == '__main__':
    # TODO optimize all function about store data in tables here and use them from here !
    
    db_path = 'digikala.db'
    DataBaseHandler(db_path).create_tables()
    