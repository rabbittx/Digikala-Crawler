import sqlite3 
import json
db_path = 'digikala.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
table_name = 'products_extraction'
row_id = 'dkp-6903697'
column_name = 'product_id'


def get_data_from_database(table_name,row_id,column_name):
    query = f'SELECT * FROM {table_name} WHERE {column_name} = "{row_id}"'
    cursor.execute(query)
    row = cursor.fetchall()
    existing_data = {col[0]: val for col, val in zip(cursor.description, row)}
    existing_data = json.loads(existing_data)
    return existing_data


def check_existing_data( row_id, column_name, table_name):
    query = f'SELECT * FROM {table_name} WHERE {column_name} = "{row_id}"'
    cursor.execute(query)
    result = cursor.fetchone()
    existing_data = {col[0]: val for col, val in zip(cursor.description, result)}
    print(existing_data)
        # اینجا result را مستقیماً به parse_json_fields ارسال می‌کنیم
    return False if not result else parse_json_fields(existing_data)

def parse_json_fields( record):
    parsed_record = {}
    for key in record.keys():
        try:
            parsed_record[key] = json.loads(record[key])
        except (TypeError, json.JSONDecodeError):
            parsed_record[key] = record[key]
    return parsed_record

test = check_existing_data(table_name=table_name,row_id=row_id,column_name=column_name)
print(test)