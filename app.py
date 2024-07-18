import numpy as np
import pandas as pd
import singlestoredb as s2
from secret import *
import json

def pull_data():
    try:
        conn = s2.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            database=DATABASE,
            autocommit=True
        )
        query = f"SELECT * from customer LIMIT 10;"
        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        conn.close()
        if result:
            return json.dumps(result)
        else:
            return None
    except Exception as e:
        print(f"Error fetching vector: {e}")
        return None
    
def write_data_to_customer_copy(data):
    try:
        # Connect to the SingleStore database
        conn = s2.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            database=DATABASE,
            autocommit=True
        )
        
        # Convert JSON string to Python object (list of lists)
        data = json.loads(data)
        
        if not data:
            print("No data to write.")
            return
        
        # Prepare the insert query and values
        insert_query = """
        INSERT INTO customer_copy (
            c_custkey, c_name, c_address, c_nationkey, c_phone,
            c_acctbal, c_mktsegment, c_comment
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = [tuple(row) for row in data]

        with conn.cursor() as cursor:
            cursor.executemany(insert_query, values)
        
        conn.close()
        print("Data successfully written to customer_copy.")
    except Exception as e:
        print(f"Error writing data to customer_copy: {e}")

if __name__ == "__main__":
    data = pull_data()
    if data:
        write_data_to_customer_copy(data)
    else:
        print("No data found in source table.")

