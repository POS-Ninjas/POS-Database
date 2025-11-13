from db import *
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
        user_repo  = UserRepository(db)
        roles_repo = RoleRepository(db)
        client_repo = ClientRepository(db)

        # roles_repo.insert_roles()
        # print(roles_repo.get_single_role())
        # roles_repo.delete_all_roles()

        # user_repo.populate_user_table_with_fake_data(100)
   
        # all_users = user_repo.get_all_users()
    
        # for user in all_users:
            # print(user)

        # print(user_repo.get_single_user())
        # print(user_repo.delete_all_users())

        client_repo.populate_client_table_with_fake_data()

        all_clients = client_repo.get_all_clients()

        for client in all_clients:
            print(client)

        # print(client_repo.get_single_client())
        # print(client_repo.delete_all_clients())


def main():
    print("Hello from pos-database-with-fake-data!")

    read_data()

if __name__ == "__main__":
    main()