import sqlite3
from tables import Roles, User
from faker import Faker
import bcrypt
import random

faker = Faker()

def init_db(connection):
    pass

ROLE_NAMES_AND_DESCIRPTIONS = {
    "admin": "Overall admin",
    "manager1": "Manager in charge of front shop" ,
    "manager2": "Manager in charge of back shop",
    "cashier1": "cashier in store 1",
    "cashier2": "cashier in store 2",
}

def create_data_for_users(connection):

    """
        create fake data
    """
    users = []

    for _ in range(50):
        password = f"{faker.password()}".encode()
        password_hash = bcrypt.hashpw(password, bcrypt.gensalt())
        user_id =  faker.numerify(text='############')
        users.append(
            User(
                user_id=user_id,
                username=faker.user_name(),
                password_hash=password_hash,
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                email=faker.email(),
                role_name=random.choice(list(ROLE_NAMES_AND_DESCIRPTIONS.keys())),
                is_active=random.choice([True, False]),
                last_login=faker.date_time(),
                created_at=faker.date_time(),
                updated_at=faker.date_time()
            )
        )

    for user in users:
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO users (
                       user_id, username, password_hash, 
                       first_name, last_name, email, 
                       role_id, is_active, last_login,
                       created_at, updated_at
                       ) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''',
            (
                user.user_id,
                user.username,
                user.password_hash,
                user.first_name,
                user.last_name,
                user.email,
                user.role_name,
                user.is_active,
                user.last_login,
                user.created_at,
                user.updated_at
            )        
        )

def read_users_data(connection):
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users")

    return cursor.fetchall()

def delete_users_data(connection):
    cursor = connection.cursor()

    cursor.execute("DELETE FROM users")