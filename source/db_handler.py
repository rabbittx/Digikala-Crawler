import sqlite3 ,json

class DataBaseHandler():
    def __init__(self, db_path,log):
        self.conn = sqlite3.connect(db_path,timeout=30)
        self.cursor = self.conn.cursor()
        self.log = log

    def create_tables(self):
        """
         Create table if they don't exist already.
        :return: None
        
        """
        # Create a table to store seller information
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

        # Create a table to store product details
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            product_id TEXT PRIMARY KEY,
            seller_id TEXT,
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

        # Create a table to store extracted product details
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS products_extraction (
            product_id TEXT PRIMARY KEY,  
            seller_id TEXT,              
            crawl_date TEXT,    
            seller_name TEXT, 
            categories TEXT,          
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

        # Create a table to store historical sellers details
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

        # Create a table to store historical products details
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS products_history (
            history_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT,
            seller_id TEXT,
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

        # Create a table to store historical extracted product details
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS products_extraction_history (
            history_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT,
            seller_id TEXT, 
            seller_name TEXT,
            crawl_date TEXT,
            categories TEXT,
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

    def get_row_info(self,fields,table_name,condition=None,return_as_list=False):
        """ 
        this function help to  extract information from the database based on certain conditions and fields requested by the user
        This function is used to select rows from the database based on certain conditions.
        
        Args:
            fields : A list of strings or single string  representing the columns you want to retrieve. If * then all.
            table_name : name of table want to select data from it 
            condition :  dictionary contains field and value for filtering data in the table
                        if None all records will be returned
            return_as_list : set it to True to  return selected rows as list
        """
        
        field = ','.join(fields)
        query = f"SELECT {field} FROM {table_name} "
        if condition != None :
            query += f'WHERE {condition[0]}= "{condition[1]}" '
        self.cursor.execute(query)
        row_info = self.cursor.fetchall()
        return row_info if return_as_list is True else [product for product in row_info]
     
    
    def get_column_names(self, table_name):
        """
         Get column names of a given table
         
         Args :
           table_name : Name of the table whose columns are needed.
        
        """

        query = f"PRAGMA table_info({table_name})"
        self.cursor.execute(query)
        columns_info = self.cursor.fetchall()
        column_names = [column_info[1] for column_info in columns_info]
        return column_names

    def check_field_value(self,row_data, crawl_data):
        """
         Checks whether a specific field has been filled or not.
         
         Args :
             row_data : A single record fetched from the database.
             crawl_data : The data which we need to compare with the database.
             
         Returns :
             True if the field has been filled , False otherwise.
        
        """

        key_to_pass = ['crawl_date','product_image','reviews','question_box','seller_name','product_id','seller_id']
        for key in row_data:
            if key not in key_to_pass  :
                if row_data[key] != crawl_data[key]:
                    return True
        return False
    
    def check_existing_data(self, row_id, column_name, table_name):
        """
         This function is used to check the fields in the database whether they have been updated or not .

         Args : 
           row_id : Unique id of each entry in the database.
           column_name : name of feild to check for update.
           table_name : Name of the table where the data needs to be checked.

         Returns :
           Data as json if existing else False.
         
        
        """

        query = f'SELECT * FROM {table_name} WHERE {column_name} = "{row_id}"'
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result != [] and result != None:
            result = {col[0]: val for col, val in zip(self.cursor.description, result)}
        return False if not result else self.parse_json_fields(result)

    def parse_json_fields(self, record):
        """
         parse fields to json

         Args : 
            record : Record which contains multiple fields.

         Returns :
             Json object of the record.
        
        """
        parsed_record = {}
        for key in record.keys():
            try:
                parsed_record[key] = json.loads(record[key])
            except (TypeError, json.JSONDecodeError):
                parsed_record[key] = record[key]
        return parsed_record

    def replace_recode_to_history_table(self,data,column_name,table_name):
        """
         Move old data from main table to history table.

         Args :  
            data : A dictionary that will be inserted into History Table.
                   It should contain at least 'ID' column.
            column_name : Name of the column which is used to identify each row uniquely.
            table_name : Name of the table where we want to move the data.

         Returns :
              True if success otherwise False.
        
        """

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
        """
         Insert a new line or update an existing one in a given table.
         
         If there is already a record with same ID then it updates the record  
         otherwise creates a new one.

         Args :   
             data : A dictionary containing field name and value pairs. 
                    The keys should match the columns names in the table.
             table_name : Name of the table.
         
         Returns :
               None
        
        """
        for key in data:
            if isinstance(data[key], dict) or isinstance(data[key], list):
                data[key] = json.dumps(data[key],ensure_ascii=False)
        columns = ', '.join(data.keys())
        placeholders = ', '.join([f":{k}" for k in data])
        query = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
        self.cursor.execute(query, data)
        self.conn.commit()
        self.log.info('[+] insert recode to table successfully ')

    def update_database(self,data,column_name,table_name):
        """
         Update records in a table based on a column.
         
         This function will find all the lines that have the specified 'column_value' 
         in the 'column_name' column and update them with the provided 'data'.

         Args :      
             data : A dictionary containing field name and value pairs.  
                     The keys should match the columns names in the table.
             column_name : Column name used to filter rows.
             table_name : Table where the changes are made.
        
        """
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
        """
         Close the connection to the database.
        
        """
        self.conn.commit()
        self.conn.close()
