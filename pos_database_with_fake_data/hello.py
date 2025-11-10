from db import create_data_for_users, read_users_data, delete_users_data
import sqlite3
from pathlib import Path

"""
TODO 

- have functions that populate the database for each table in the DB
- make it performant..add async io 
- have corresponding crud functions for each of the table 
- test the functions
- test the indexes of the database tables

"""

DB_PATH = Path('/home/test/Desktop/pos/POS-Database') / 'test.db'

def read_data():
    
    with sqlite3.connect(DB_PATH) as connection:
        # create_data_for_users(connection)
        delete_users_data(connection)
        print(read_users_data(connection))

def main():
    print("Hello from pos-database-with-fake-data!")

    read_data()

if __name__ == "__main__":
    main()