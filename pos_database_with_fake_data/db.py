from tables import Roles, User, Customer
from typing import List, Optional
from faker import Faker
import bcrypt
import random
from db_context import DatabaseContext

faker = Faker()

ROLE_NAMES_AND_DESCIRPTIONS = {
    "admin": "Overall admin",
    "manager1": "Manager in charge of front shop" ,
    "manager2": "Manager in charge of back shop",
    "cashier1": "cashier in store 1",
    "cashier2": "cashier in store 2",
}


class UserRepository:
    def __init__(self, db_context: DatabaseContext):
        self.db = db_context

    def _row_to_user(self, row) -> User:
        """Convert database row to Product dataclass"""
        return User(
            user_id=row['user_id'],
            username=row['username'],
            password_hash=row['password_hash'],
            first_name=row['first_name'],
            last_name=row['last_name'],
            email=row['email'],
            role_name=row['role_name'],
            is_active=row['is_active'],
            last_login=row['last_login'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )
    
    def read_users_data(self) -> List[User]:
       self.db.execute("SELECT * FROM users")
       return [self._row_to_user(user) for user in self.db.fetchall()]
    
    def read_single_user_data(self) -> Optional[User]:
        self.db.execute("SELECT * FROM users LIMIT 1")
        user = self.db.fetchone()
        return self._row_to_user(user) if user else None
    
    def delete_users_data(self):
        self.db.execute("DELETE FROM users")

    def single_save_or_upsert(self, user: User):
        if user.user_id is None:
            self.db.execute('''
                INSERT INTO users (
                    user_id, username, password_hash, 
                    first_name, last_name, email, 
                    role_name, is_active, last_login,
                    created_at, updated_at
                ) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
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
            ))
            user.user_id = self.db.cursor.lastrowid
            print(f"Successfully inserted user: {user['user_id']}")
        else:
            self.db.execute('''
            UPDATE users SET
                username = ?, password_hash = ?, first_name = ?, last_name = ?,
                email = ?, role_id = ?, is_active = ?, last_login = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
        ''', (
            user['username'], user['password_hash'],
            user['first_name'], user['last_name'], user['email'],
            user['role_id'], user['is_active'], user['last_login'],
            user['user_id']
        ))
        print(f"Updated existing user: {user['user_id']}")

    def populate_user_table_with_fake_data(self, number_of_rows=50):

        """
            create fake data
        """
        users = []

        for _ in range(number_of_rows):
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

            print(f"inserting {user.user_id}")
        
            self.db.execute('''
                INSERT INTO users (
                        user_id, username, password_hash, 
                        first_name, last_name, email, 
                        role_name, is_active, last_login,
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

class CustomerRepository:
    def __init__(self, db_context: DatabaseContext):
        self.db = db_context

    def _row_to_category(self, row) -> Customer:
        """Convert database row to Category dataclass"""
        return Customer(
            catgory_id=row['category_id']
        )
