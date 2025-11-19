from tables import Role, User, Client, Category, Supplier
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

ROLE_PERMISSIONS = {
    "admin" : "all perms",
    "manager1": "perms1",
    "manager2": "perms2",
    "cashier1": "perms3",
    "cashier2": "perms4"
}

class RoleRepository:
    def __init__(self, db_context: DatabaseContext):
        self.db = db_context

    def _row_to_role(self, row) -> Role:
        """Convert database row to Role dataclass"""
        return Role(
            role_id=row['role_id'],
            role_name=row['role_name'],
            role_description=row['role_description'],
            permissions=row['permissions'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )
    
    def read_all_roles(self) -> List[Role]:
       self.db.execute("SELECT * FROM roles")
       return [self._row_to_role(role) for role in self.db.fetchall()]
    
    def get_single_role(self) -> Optional[Role]:
        self.db.execute("SELECT * FROM roles LIMIT 1")
        role = self.db.fetchone()
        return self._row_to_role(role) if role else None
    
    def delete_all_roles(self):
        self.db.execute("DELETE FROM roles")

    def insert_roles(self):
        for name, description in ROLE_NAMES_AND_DESCIRPTIONS.items():
            role_id = faker.numerify(text='############')
          

            for role_perms_key in ROLE_NAMES_AND_DESCIRPTIONS.keys():
                if role_perms_key == name: 
                    permissions = ROLE_PERMISSIONS[role_perms_key]
            
            self.db.execute('''
                INSERT INTO roles (
                    role_id, role_name, 
                    role_description, permissions,
                    created_at, updated_at
                ) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''',
                (
                    role_id,
                    name,
                    description,
                    permissions,
                    faker.date_time(),
                    faker.date_time()
                )        
            )
            
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
    
    def get_all_users(self) -> List[User]:
       self.db.execute("SELECT * FROM users")
       return [self._row_to_user(user) for user in self.db.fetchall()]
    
    def get_single_user(self) -> Optional[User]:
        self.db.execute("SELECT * FROM users LIMIT 1")
        user = self.db.fetchone()
        return self._row_to_user(user) if user else None
    
    def delete_all_users(self):
        self.db.execute("DELETE FROM users")

    def save_or_upsert_single_user(self, user: User):
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

        for i in range(number_of_rows):
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
                    email=f"{i}_{faker.email()}",
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

class ClientRepository:
    def __init__(self, db_context: DatabaseContext):
        self.db = db_context

    def _row_to_client(self, row) -> Client:
        """Convert database row to Client dataclass"""
        return Client(
            client_id=row['client_id'],
            first_name=row['first_name'],
            last_name=row['last_name'],
            phone_number=row['phone_number'],
            email=row['email'],
            tin=row['tin'],
            client_type=row['client_type'],
            business_name=row['business_name'],
            business_address=row['business_address'],
            business_type=row['business_type'],
            is_active=row['is_active'],
            created_at=row['created_at'],
            updated_at=row['updated_at'],
            deleted_at=row['deleted_at']
        )
    
    def get_all_clients(self) -> List[Client]:
       self.db.execute("SELECT * FROM clients")
       return [self._row_to_client(client) for client in self.db.fetchall()]
    
    def get_single_client(self) -> Optional[Client]:
        self.db.execute("SELECT * FROM clients LIMIT 1")
        client = self.db.fetchone()
        return self._row_to_client(client) if client else None
    
    def delete_all_clients(self):
        self.db.execute("DELETE FROM clients")

    def save_or_upsert_single_client(self, client: Client):
        if client.client_id is None:
            self.db.execute('''
                INSERT INTO clients (
                    client_id, first_name, last_name, 
                    phone_number, email, tin, 
                    client_type, business_name, business_address,
                    business_type, is_active, created_at,
                    updated_at, deleted_at
                ) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                client.client_id,
                client.first_name,
                client.last_name,
                client.phone_number,
                client.email,
                client.tin,
                client.client_type,
                client.business_name,
                client.business_address,
                client.business_type,
                client.is_active,
                client.created_at,
                client.updated_at,
                client.deleted_at
            ))
            client.client_id = self.db.cursor.lastrowid
            print(f"Successfully inserted client: {client['client_id']}")
        else:
            self.db.execute('''
                UPDATE clients SET
                    first_name = ?, last_name = ?, phone_number = ?, email = ?,
                    tin = ?, client_type = ?, is_active = ?, business_name = ?,
                    business_address = ?, business_type = ?
                    updated_at = CURRENT_TIMESTAMP
                WHERE client_id = ?
            ''', (
                client['first_name'], client['last_name'],
                client['phone_number'], client['email'], client['tin'],
                client['client_type'], client['is_active'], client['business_name'],
                client['business_address'], client['business_type'], client['client_id']
            ))
            print(f"Updated existing user: {client['client_id']}")

    def populate_client_table_with_fake_data(self, number_of_rows=50):

        """
            create fake data
        """
        clients = []

        for _ in range(number_of_rows):
    
            client_id =  faker.numerify(text='############')
           
            clients.append(
                Client(
                    client_id=client_id,
                    first_name=faker.first_name(),
                    last_name=faker.last_name(),
                    phone_number=faker.phone_number(),
                    email=faker.email(),
                    tin=faker.itin(),
                    client_type=random.choice(["customer","business"]),
                    business_name=faker.building_number(),
                    business_address=faker.street_address(),
                    business_type=random.choice(["customer","supplier", "export"]),
                    is_active=random.choice([True, False]),
                    created_at=faker.date_time(),
                    updated_at=faker.date_time(),
                    deleted_at=faker.time()
                )
            )

        for client in clients:

            print(f"inserting {client.client_id}")
        
            self.db.execute('''
                INSERT INTO clients (
                        client_id,  first_name, last_name,
                        phone_number, email, tin,
                        client_type, business_name, business_address, 
                        business_type, is_active, created_at, 
                        updated_at, deleted_at
                    ) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
                (
                    client.client_id,
                    client.first_name,
                    client.last_name,
                    client.phone_number,
                    client.email,
                    client.tin,
                    client.client_type,
                    client.business_name,
                    client.business_address,
                    client.business_type,
                    client.is_active,
                    client.created_at,
                    client.updated_at,
                    client.deleted_at
                )        
            )

class CategoryRepository:
    def __init__(self, db_context: DatabaseContext):
        self.db = db_context

    def _row_to_category(self, row) -> Category:
        """Convert database row to Category dataclass"""
        return Category(
            category_id=row['category_id'],
            category_name=row['category_name'],
            category_code=['category_code'],
            description=['description'],
            created_at=row['created_at'],
            updated_at=row['updated_at'],
        )
    
    def get_all_categories(self) -> List[Category]:
       self.db.execute("SELECT * FROM categories")
       return [self._row_to_category(category) for category in self.db.fetchall()]
    
    def get_single_category(self) -> Optional[Category]:
        self.db.execute("SELECT * FROM categories LIMIT 1")
        category = self.db.fetchone()
        return self._row_to_category(category) if category else None
    
    def delete_all_categories(self):
        self.db.execute("DELETE FROM categories")

    def save_or_upsert_single_category(self, category: Category):
        if category.category_id is None:
            self.db.execute('''
                INSERT INTO categories (
                    category_id, category_name, category_code,
                    description, created_at, updated_at
                ) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                category.category_id,
                category.category_name,
                category.category_code,
                category.description,
                category.created_at,
                category.updated_at
            ))
            category.category_id = self.db.cursor.lastrowid
            print(f"Successfully inserted category: {category['category_id']}")

        else:
            self.db.execute('''
                UPDATE categories SET
                    category_name = ?, category_code = ?,
                    description = ?, created_at = ?,                            
                    updated_at = CURRENT_TIMESTAMP
                WHERE category_id = ?
            ''', (
                category['category_id'],
                category['category_name'],
                category['category_code'],
                category['description'],
                category['created_at'],
                category['updated_at']
            ))
            print(f"Updated existing category: {category['category_id']}")

    def populate_category_table_with_fake_data(self, number_of_rows=50):

        """
            create fake data
        """
        records = []

        # Option 1: Use common retail categories
        categories = [
            "Electronics", "Clothing", "Groceries", "Home & Garden", 
            "Health & Beauty", "Sports", "Books", "Toys"
        ]

        for _ in range(number_of_rows):
    
            category_id = faker.numerify(text='############')
           
            records.append(
                Category(
                    category_id=category_id,
                    category_name=random.choice(categories) +  " " + category_id,
                    category_code=f"CAT {category_id}",
                    description=faker.sentence(),
                    created_at=faker.date_time(),
                    updated_at=faker.date_time(),
                )
            )

        for category in records:

            print(f"inserting {category.category_id}")
        
            self.db.execute('''
                INSERT INTO categories (
                        category_id, category_name, category_code,
                        description, created_at, updated_at
                    ) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''',
                (
                    category.category_id,
                    category.category_name,
                    category.category_code,
                    category.description,
                    category.created_at,
                    category.updated_at
                )        
            )

class SupplierRepository:
    def __init__(self, db_context: DatabaseContext):
        self.db = db_context

    def _row_to_supplier(self, row) -> Supplier:
        """Convert database row to Supplier dataclass"""
        return Supplier(
            supplier_id=row['supplier_id'],
            company_name=['company_name'],
            contact_name=['contact_name'],
            email=['email'],
            phone_number=['phone_number='],
            tin=['tin'],
            address=['address'],
            is_active=['is_active']
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )
    
    def get_all_suppliers(self) -> List[Supplier]:
       self.db.execute("SELECT * FROM suppliers")
       return [self._row_to_supplier(supplier) for supplier in self.db.fetchall()]
    
    def get_single_supplier(self) -> Optional[Supplier]:
        self.db.execute("SELECT * FROM suppliers LIMIT 1")
        supplier = self.db.fetchone()
        return self._row_to_supplier(supplier) if supplier else None
    
    def delete_all_suppliers(self):
        self.db.execute("DELETE FROM suppliers")

    def save_or_upsert_single_category(self, supplier: Supplier):
        if supplier.supplier_id is None:
            self.db.execute('''
                INSERT INTO suppliers (
                    supplier_id, company_name, contact_code,
                    email, phone_number, tin, address, 
                    is_active, created_at, updated_at
                ) 
                VALUES (?, ?, ?, ?, ?, ?, ? , ?, ?. ?, ?)
            ''', (
                supplier.supplier_id,
                supplier.company_name,
                supplier.contact_name,
                supplier.email,
                supplier.phone_number,
                supplier.tin,
                supplier.address,
                supplier.is_active,
                supplier.created_at,
                supplier.updated_at
            ))
            supplier.supplier_id = self.db.cursor.lastrowid
            print(f"Successfully inserted supplier: {supplier['supplier_id']}")

        else:
            self.db.execute('''
                UPDATE suppliers SET
                    supplier_id, company_name, contact_code,
                    email, phone_number, tin, address, 
                    is_active, created_at, updated_at
                WHERE supplier_id = ?
            ''', (
                supplier['supplier_id'],
                supplier['company_name'],
                supplier['contact_name'],
                supplier['phone_number'],
                supplier['tin'],
                supplier['address'],
                supplier['is_address'],
                supplier['created_at'],
                supplier['updated_at']
            ))
            print(f"Updated existing supplier: {supplier['supplier_id']}")
