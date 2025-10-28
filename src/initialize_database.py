import sqlite3
import os
from dotenv import dotenv_values

# Environment Variables
STORAGE_FILE = f"{dotenv_values(".env")["STORAGE_FILE"]}" 
RESET = False

## TABLE INITIALIZATION ##
table_queries = [
    '''CREATE TABLE User
             (user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
              name TEXT UNIQUE NOT NULL,
              password BLOB NOT NULL,
              salt TEXT NOT NULL)''',
    '''CREATE TABLE Account
            (account_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            name TEXT UNIQUE NOT NULL,
            email TEXT,
            description TEXT,
            password TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE)'''
]
def initialize_tables(table_queries : list = table_queries, reset = RESET):
    ## Dropping Existing Database if already existing
    if (reset == True and os.path.exists(STORAGE_FILE)):
        reset_tables()

        ## SQL connection variables
        connection = sqlite3.connect(STORAGE_FILE)
        cursor = connection.cursor()

        ## Create Tables
        for query in table_queries:
            cursor.execute(query)
        connection.commit()

        ## Close connections
        cursor.close()
        connection.close()

def reset_tables():
    connection = sqlite3.connect(STORAGE_FILE)
    connection.execute("DROP TABLE User")
    connection.execute("DROP TABLE Account")
    connection.close()

if __name__ == '__main__':
    pass