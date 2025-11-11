from db import create_data_for_users, read_users_data, delete_users_data, UserRepository
from db_context import DatabaseContext
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
        # delete_users_data(connection)
        # print(read_users_data(connection))
        pass

    with DatabaseContext() as db:
        product_repo = UserRepository(db)


        product_repo.populate_user_table_with_fake_data(100)

        # all_users = product_repo.read_users_data()
    
        # for user in all_users:
        #     print(user)

        print(product_repo.read_single_user_data())

        print(product_repo.delete_users_data())


def main():
    print("Hello from pos-database-with-fake-data!")

    read_data()

if __name__ == "__main__":
    main()