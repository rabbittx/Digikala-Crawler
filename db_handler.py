import sqlite3
import json
class DataBaseHandler():
    def __init__(self, db_path,log):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.log = log
    def create_tables(self):
        # Create a table for seller information
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS sellers (
            seller_id TEXT PRIMARY KEY,
            crawl_date TEXT,                 
            seller_name TEXT,
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
            product_id TEXT PRIMARY KEY,
            crawl_date TEXT,
            seller_name TEXT,
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
            product_id TEXT PRIMARY KEY,                
            crawl_date TEXT,               
            product_link TEXT ,
            main_product_details TEXT ,
            buy_box TEXT ,
            product_image TEXT ,
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
        # جدول تاریخچه برای فروشندگان
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS sellers_history (
            history_id INTEGER PRIMARY KEY AUTOINCREMENT,
            seller_id TEXT,
            crawl_date TEXT,
            seller_name TEXT,
            membership_period TEXT,
            satisfaction_with_goods TEXT,
            seller_performance TEXT,
            people_have_given_points TEXT,
            timely_supply TEXT,
            obligation_to_send TEXT,
            no_return TEXT,
            introduction_of_the_seller TEXT    
            change_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (seller_id) REFERENCES sellers (seller_id)
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS products_history (
            history_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT,
            crawl_date TEXT,
            seller_name TEXT,
            product_link TEXT,
            product_image TEXT,
            product_rate TEXT,
            product_name TEXT,
            product_price TEXT,
            product_price_discount_percent TEXT,
            product_price_discount TEXT,
            product_special_sale TEXT,
            stock TEXT
            change_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products (product_id)
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS products_extraction_history (
            history_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT,
            crawl_date TEXT,
            product_link TEXT ,
            main_product_details TEXT ,
            buy_box TEXT ,
            product_image TEXT ,
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
            change_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products_extraction (product_id)
        )
        ''')


# ============================= CLEAN CODE =======================================================
    # new run -> (data , table_id , table_name)  
            # -> check data if exists in database(/,/,/) -> return true/false 
                # if true --> check if fields is same in table -> pass
                          # -> else not same -> send data of table to historical table + save new data to table 
                # if false --> insert data to table 
    def check_field_value(self,row_data, crawl_data):
        key_to_pass = ['crawl_date','product_image','reviews','question_box','seller_name','product_id','seller_id']
        for key in row_data:
            if key not in key_to_pass  :
                if row_data[key] != crawl_data[key]:
                    return True
        return False
    
    def check_existing_data(self, row_id, column_name, table_name):
        query = f'SELECT * FROM {table_name} WHERE {column_name} = "{row_id}"'
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result != [] and result != None:
            result = {col[0]: val for col, val in zip(self.cursor.description, result)}
        return False if not result else self.parse_json_fields(result)

    def parse_json_fields(self, record):
        parsed_record = {}
        for key in record.keys():
            try:
                parsed_record[key] = json.loads(record[key])
            except (TypeError, json.JSONDecodeError):
                parsed_record[key] = record[key]
        return parsed_record

    def replace_recode_to_history_table(self,data,column_name,table_name):
        # TODO need to check if this funcion work successfully or not 
        try:
            row_id = data[column_name]
            query = f'SELECT * FROM {table_name} WHERE {column_name} = "{row_id}"'
            self.cursor.execute(query)
            record = self.cursor.fetchone()
            record = {col[0]: val for col, val in zip(self.cursor.description, record)}
            if record:
                self.insert_recode_to_table(data=record,table_name=f'{table_name}_history')
                self.cursor.execute(f'DELETE FROM {table_name} WHERE {column_name} = "{row_id}" ') # شرط مشابه برای حذف
                self.conn.commit()
                self.log.info(f'[+] recode DELETED from {table_name} table and insert to {table_name}_history table')
            else:
                self.log.error("[-] recode not found.")
        except sqlite3.Error as e:
            self.log.error(f"[-] database ERROR : {e}")

    def insert_recode_to_table(self,data,table_name) :
        for key in data:
            if isinstance(data[key], dict) or isinstance(data[key], list):
                data[key] = json.dumps(data[key])
        columns = ', '.join(data.keys())
        placeholders = ', '.join([f":{k}" for k in data])
        query = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
        self.cursor.execute(query, data)
        self.conn.commit()
        self.log.info('[+] insert recode to table successfully ')

    def run(self,data,column_name,table_name):
        if self.check_existing_data(row_id=data[column_name],column_name=column_name,table_name=table_name) :
            existing_recode = self.check_existing_data(row_id=data[column_name],column_name=column_name,table_name=table_name) 
            existing_recode = self.parse_json_fields(existing_recode)
            self.log.info("[!] Data already exist")
            if self.check_field_value(data,existing_recode):
                self.log.info("[!] page data get updated start to replace recode ")
                self.replace_recode_to_history_table(data=data,column_name=column_name,table_name=table_name)
                self.insert_recode_to_table(data,table_name)
            else :
                self.log.info('[-] Fields are the same no update on this data - PASS')
        else :
            self.log.info("[+] New Data not exist in database start to insert it")
            self.insert_recode_to_table(data,table_name) 

    def close_connection(self):
        self.conn.commit()
        self.conn.close()

if __name__ == "__main__" :
    DataBaseHandler(db_path='digikala_database.db',log='log').create_tables()