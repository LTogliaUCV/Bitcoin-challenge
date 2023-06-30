import sqlite3
import pandas as pd

class BitcoinDatabase:
    def __init__(self, db_file,table_name):
        self.db_file = db_file
              
        # Create the 'btc' table if it doesn't exist
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            date TEXT NOT NULL,
            price REAL NOT NULL
        );
        """
        cursor.execute(create_table_sql)
        conn.commit()
        conn.close()
        
    def insert_data(self, df, table_name):
        # Insert data from the Pandas DataFrame into the 'btc' table
        conn = sqlite3.connect(self.db_file)
        df.to_sql(table_name, conn, if_exists='append', index=False)
        conn.commit()
        conn.close()
        
    def select_data(self, table_name):
        # Select all data from the 'btc' table and return it as a Pandas DataFrame
        conn = sqlite3.connect(self.db_file)
        select_query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(select_query, conn)
        conn.close()
        return df
    

class RollingMeanDatabase:
    def __init__(self, db_name, table_name):
        self.db_name = db_name
        self.table_name = table_name

    def insert_rolling_mean(self, df):
        # Convert the 'date' column to datetime type
     

        # Open a connection to the database
        conn = sqlite3.connect(self.db_name)

        # Create the table if it doesn't exist
        conn.execute(f'''CREATE TABLE IF NOT EXISTS {self.table_name}
                        (date TEXT ,
                        mean_value_price REAL);''')

        # Insert the results into the table
        df.to_sql(self.table_name, conn, if_exists='append', index=False)

        # Close the connection to the database
        conn.close()
