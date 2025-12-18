from tables import *
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
                    password_hash=str(password_hash),
                    first_name=faker.first_name(),
                    last_name=faker.last_name(),
                    email=f"{i}_{faker.email()}",
                    role_name=str(random.choice(list(ROLE_NAMES_AND_DESCIRPTIONS.keys()))),
                    is_active=str(random.choice([True, False])),
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
    
            client_id = str(faker.numerify(text='############'))
           
            clients.append(
                Client(
                    client_id=client_id,
                    first_name=faker.first_name(),
                    last_name=faker.last_name(),
                    phone_number=faker.phone_number(),
                    email=faker.email(),
                    tin=faker.itin(),
                    client_type=str(random.choice(["customer","business"])),
                    business_name=faker.building_number(),
                    business_address=faker.street_address(),
                    business_type=str(random.choice(["customer","supplier", "export"])),
                    is_active=str(random.choice([True, False])),
                    created_at=faker.date_time(),
                    updated_at=faker.date_time(),
                    deleted_at=faker.date_time()
                )
            )

        for client in clients:

            print(f"inserting {client.client_id}")
        
            self.db.execute('''
                INSERT INTO clients (
                        client_id, first_name, last_name,
                        phone_number, email, tin, client_type, 
                        business_name, business_address, business_type, 
                        is_active, created_at, updated_at, deleted_at
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
            category_code=row['category_code'],
            description=row['description'],
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

        for i in range(number_of_rows):
           
            records.append(
                Category(
                    category_id=None,
                    category_name=random.choice(categories),
                    category_code=f"CAT{i+1:03d}",
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
            company_name=row['company_name'],
            contact_name=row['contact_name'],
            email=row['email'],
            phone_number=row['phone_number='],
            tin=row['tin'],
            address=row['address'],
            is_active=row['is_active'],
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

    def save_or_upsert_single_supplier(self, supplier: Supplier):
        if supplier.supplier_id is None:
            self.db.execute('''
                INSERT INTO suppliers (
                    supplier_id, company_name, contact_code,
                    email, phone_number, tin, address, 
                    is_active, created_at, updated_at
                ) 
                VALUES (?, ?, ?, ?, ?, ?, ? , ?, ?, ?, ?)
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
                    company_name, contact_code,
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

    def populate_suppliers_table_with_fake_data(self, number_of_rows=50):

        """
            create fake data
        """
        suppliers = []

        for _ in range(number_of_rows):
    
            supplier_id = int(faker.numerify(text='############'))
            tin = faker.bothify("TIN-#########")
           
            suppliers.append(
                Supplier(
                    supplier_id=supplier_id,
                    company_name=faker.company(),
                    contact_name=faker.name(),
                    email=faker.email(),
                    phone_number=faker.phone_number(),
                    tin = tin,
                    address=faker.address(),
                    is_active=faker.boolean(),
                    created_at=faker.date_time(),
                    updated_at=faker.date_time(),
                )
            )

        for supplier in suppliers:

            print(f"inserting {supplier.supplier_id}")
        
            self.db.execute('''
                INSERT INTO suppliers (
                        supplier_id, company_name, contact_name,
                        email, phone_number, tin,
                        address, is_active, created_at,
                        updated_at
                    ) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
                (
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
                )        
            )

class ProductRepository:
    def __init__(self, db_context: DatabaseContext):
        self.db = db_context

    def _row_to_product(self, row) -> Product:
        return Product(
            product_id=row['product_id'],
            product_name=row['product_name'],
            product_code=row['product_code'],
            barcode=row['barcode'],
            category_id=row['category_id'],
            supplier_id=row['supplier_id'],
            image_url=row['image_url'],
            description=row['description'],
            unit_purchase_price=row['unit_purchase_price'],
            unit_selling_price=row['unit_selling_price'],
            current_stock=row['current_stock'],
            reorder_level=row['reorder_level'],
            product_type=row['product_type'],
            tax_rate=row['tax_rate'],
            is_taxable=row['is_taxable'],
            is_tax_inclusive=row['is_tax_inclusive'],
            is_active=row['is_active'],
            created_at=row['created_at'],
            updated_at=row['updated_at'],
            deleted_at=row['deleted_at']
        )
    
    def get_all_products(self) -> List[Product]:
       self.db.execute("SELECT * FROM products")
       return [self._row_to_product(product) for product in self.db.fetchall()]
    
    def get_single_product(self) -> Optional[Product]:
        self.db.execute("SELECT * FROM products LIMIT 1")
        product = self.db.fetchone()
        return self._row_to_product(product) if product else None
    
    def delete_all_products(self):
        self.db.execute("DELETE FROM products")

    def save_or_upsert_single_product(self, product: Product):
        if product.product_id is None:
            self.db.execute('''
                INSERT INTO products (
                    product_id, product_name, product_code,
                    barcode, category_id, supplier_id, image_url,
                    description, unit_purchase_price, unit_selling_price,
                    current_stock, reorder_level, product_type,
                    tax_rate, is_taxable, is_tax_inclusive,
                    is_active, created_at, updated_at, deleted_at
                ) 
                VALUES (?, ?, ?, ?, ?, ?, ? , ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                product.product_id,
                product.product_name,
                product.product_code,
                product.barcode,
                product.category_id,
                product.supplier_id,
                product.image_url,
                product.description,
                product.unit_purchase_price,
                product.unit_selling_price,
                product.current_stock, 
                product.reorder_level,
                product.product_type,
                product.tax_rate,
                product.is_taxable,
                product.is_tax_inclusive,
                product.is_active,
                product.created_at,
                product.updated_at,
                product.deleted_at
            ))
            product.product_id = self.db.cursor.lastrowid
            print(f"Successfully inserted product: {product['product_id']}")

        else:
            self.db.execute('''
                UPDATE products SET
                    product_name, product_code, barcode, 
                    category_id, supplier_id, image_url,
                    description, unit_purchase_price, unit_selling_price,
                    current_stock, reorder_level, product_type,
                    tax_rate, is_taxable, is_tax_inclusive,
                    is_active, created_at, updated_at, deleted_at
                WHERE product_id = ?
            ''', (
                product['product_id'],
                product['product_name'],
                product['product_code'],
                product['barcode'],
                product['category_id'],
                product['supplier_id'],
                product['image_url'],
                product['description'],
                product['unit_purchase_price'],
                product['unit_selling_price'],
                product['current_stock'],
                product['reorder_level'],
                product['created_at'],
                product['updated_at'],
                product['deleted_at']
            ))
            print(f"Updated existing products: {product['product_id']}")

    def populate_products_table_with_fake_data(self, number_of_rows=50):
        """
        Create fake product data with VALID foreign key references
        """
        # Clear existing products first
        self.delete_all_products()
        
        # Get valid category IDs that exist in the database
        self.db.execute("SELECT category_id FROM categories")
        valid_category_ids = [row['category_id'] for row in self.db.fetchall()]
        
        # Get valid supplier IDs that exist in the database
        self.db.execute("SELECT supplier_id FROM suppliers")
        valid_supplier_ids = [row['supplier_id'] for row in self.db.fetchall()]
        
        if not valid_category_ids:
            raise Exception("No categories found! Create categories first.")
        if not valid_supplier_ids:
            raise Exception("No suppliers found! Create suppliers first.")

        products = []
        for i in range(number_of_rows):
            purchase_price = round(random.uniform(5, 500), 2)
            selling_price = round(purchase_price * random.uniform(1.2, 2.5), 2)  # 20-150% markup
            
            products.append(
                Product(
                    product_id=None,  # Let database auto-generate
                    product_name=faker.company() + " " + faker.word(),
                    product_code=f"PROD{i+1:05d}",
                    barcode=faker.ean13(),
                    category_id=random.choice(valid_category_ids),
                    supplier_id=random.choice(valid_supplier_ids),
                    image_url=faker.image_url(),
                    description=faker.sentence(),
                    unit_purchase_price=purchase_price,
                    unit_selling_price=selling_price,
                    current_stock=random.randint(0, 1000),
                    reorder_level=random.randint(10, 50),
                    product_type=random.choice(['goods', 'service']),
                    tax_rate=round(random.uniform(0, 20), 2),
                    is_taxable=random.choice([True, False]),
                    is_tax_inclusive=random.choice([True, False]),
                    is_active=random.choice([True, False]),
                    created_at=faker.date_time(),
                    updated_at=faker.date_time(),
                    deleted_at=None
                )
            )

        for product in products:
            try:
                print(f"Inserting product: {product.product_name}")
                
                self.db.execute('''
                    INSERT INTO products (
                        product_name, product_code, barcode, category_id, supplier_id,
                        image_url, description, unit_purchase_price, unit_selling_price,
                        current_stock, reorder_level, product_type, tax_rate,
                        is_taxable, is_tax_inclusive, is_active, created_at,
                        updated_at, deleted_at
                    ) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    product.product_name,
                    product.product_code,
                    product.barcode,
                    product.category_id,  # This is now a VALID category_id
                    product.supplier_id,  # This is now a VALID supplier_id
                    product.image_url,
                    product.description,
                    product.unit_purchase_price,
                    product.unit_selling_price,
                    product.current_stock,
                    product.reorder_level,
                    product.product_type,
                    product.tax_rate,
                    product.is_taxable,
                    product.is_tax_inclusive,
                    product.is_active,
                    product.created_at,
                    product.updated_at,
                    product.deleted_at
                ))
            except Exception as e:
                print(f"Error inserting product {product.product_name}: {e}")
                raise
        
        print(f"✅ Successfully inserted {len(products)} products")

class SaleRepository:
    def __init__(self, db_context: DatabaseContext):
        self.db = db_context
    
    def _row_to_sale(self, row) -> Sale:
        return Sale(
            sale_id=row['sale_id'],
            invoice_number=row['invoice_number'],
            sale_date=row['sale_date'],
            client_id=row['client_id'],
            category_id=row['category_id'],
            biller_id=row['biller_id'],
            subtotal=row['subtotal'],
            discount_amount=row['discount_amount'],
            tax_amount=row['tax_amount'],
            grand_total=row['grand_total'],
            amount_paid=row['amount_paid'],
            change_given=row['change_given'],
            sale_status=row['sale_status'],
            payment_method=row['payment_method'],
            momo_reference=row['momo_reference'],
            notes=row['notes'],
            created_at=row['created_at'],
            updated_at=row['updated_at'],
        )
    
    def get_all_sales(self) -> List[Sale]:
       self.db.execute("SELECT * FROM sales")
       return [self._row_to_sale(sale) for sale in self.db.fetchall()]
    
    def get_single_sale(self) -> Optional[Sale]:
        self.db.execute("SELECT * FROM sales LIMIT 1")
        sale = self.db.fetchone()
        return self._row_to_sale(sale) if sale else None
    
    def delete_all_sales(self):
        self.db.execute("DELETE FROM sales")

    def save_or_upsert_single_sale(self, sale: Sale):
        if sale.sale_id is None:
            self.db.execute('''
                INSERT INTO sales (
                    sale_id, invoice_number, sale_date,
                    client_id, biller_id, subtotal, discount_amount,
                    tax_amount, grand_total, amount_paid,
                    change_given, sale_status, payment_method,
                    momo_reference, notes, created_at,
                    updated_at,
                ) 
                VALUES (?, ?, ?, ?, ?, ?, ? , ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                sale.sale_id,
                sale.invoice_number,
                sale.sale_date,
                sale.client_id,
                sale.biller_id,
                sale.supplier_id,
                sale.subtotal,
                sale.discount_amount,
                sale.tax_amount,
                sale.grand_total,
                sale.amount_paid, 
                sale.change_given,
                sale.sale_status,
                sale.payment_method,
                sale.momo_reference,
                sale.notes,
                sale.created_at,
                sale.updated_at
            ))
            sale.sale_id = self.db.cursor.lastrowid
            print(f"Successfully inserted sale: {sale['sale_id']}")

        else:
            self.db.execute('''
                UPDATE sales SET
                    sale_id, invoice_number, sale_date,
                    client_id, biller_id, subtotal, discount_amount,
                    tax_amount, grand_total, amount_paid,
                    change_given, sale_status, payment_method,
                    momo_reference, notes, created_at, updated_at
                WHERE sale_id = ?
            ''', (
                sale['sale_id'],
                sale['invoice_number'],
                sale['sale_date'],
                sale['client_id'],
                sale['biller_id'],
                sale['subtotal'],
                sale['discount_amount'],
                sale['tax_amount'],
                sale['grand_total'],
                sale['amount_paid'],
                sale['change_given'],
                sale['sale_status'],
                sale['payment_method'],
                sale['momo_reference'],
                sale['notes'],
                sale['created_at'],
                sale['updated_at']
            ))
            print(f"Updated existing sales: {sale['sale_id']}")

    def populate_sales_table_with_fake_data(self, number_of_rows=50):
        """
        Create fake sales data with VALID foreign key references
        """
        # Clear existing sales first
        self.delete_all_sales()
        
        # Get valid client IDs that exist in the database
        self.db.execute("SELECT client_id FROM clients")
        valid_client_ids = [row['client_id'] for row in self.db.fetchall()]
        
        # Get valid user IDs for billers that exist in the database
        self.db.execute("SELECT user_id FROM users")
        valid_user_ids = [row['user_id'] for row in self.db.fetchall()]
        
        if not valid_client_ids:
            raise Exception("No clients found! Create clients first.")
        if not valid_user_ids:
            raise Exception("No users found! Create users first.")

        sales = []
        for i in range(number_of_rows):
            subtotal = round(random.uniform(50, 5000), 2)
            discount_amount = round(subtotal * random.uniform(0, 0.2), 2)  # 0-20% discount
            tax_amount = round((subtotal - discount_amount) * 0.15, 2)  # 15% tax
            grand_total = round(subtotal - discount_amount + tax_amount, 2)
            amount_paid = round(grand_total * random.uniform(0.8, 1.2), 2)  # May overpay or underpay
            change_given = max(0, amount_paid - grand_total)
            
            sale_status = random.choice(['completed', 'cancelled', 'refunded', 'on_hold'])
            payment_method = random.choice(['cash', 'momo', 'card', 'bank_transfer', 'credit'])

            sales.append(
                Sale(
                    sale_id=None,  # Let database auto-generate - REMOVED manual ID
                    invoice_number=f"INV-{faker.random_number(digits=6)}",
                    sale_date=faker.date_time_this_year(),
                    client_id=random.choice(valid_client_ids),  # Use VALID client ID
                    biller_id=random.choice(valid_user_ids),    # Use VALID user ID
                    subtotal=subtotal,
                    discount_amount=discount_amount,
                    tax_amount=tax_amount,
                    grand_total=grand_total,
                    amount_paid=amount_paid,
                    change_given=change_given,
                    sale_status=sale_status,
                    payment_method=payment_method,
                    momo_reference=faker.bothify(text="REF????-#####") if payment_method == 'momo' else None,
                    notes=faker.text(max_nb_chars=100),
                    created_at=faker.date_time(),
                    updated_at=faker.date_time(),
                )
            )

        for sale in sales:
            try:
                print(f"Inserting sale: {sale.invoice_number}")
                
                self.db.execute('''
                    INSERT INTO sales (
                        invoice_number, sale_date, client_id, biller_id, 
                        subtotal, discount_amount, tax_amount, grand_total, 
                        amount_paid, change_given, sale_status, payment_method, 
                        momo_reference, notes, created_at, updated_at
                    ) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    sale.invoice_number,
                    sale.sale_date,
                    sale.client_id,
                    sale.biller_id,
                    sale.subtotal,
                    sale.discount_amount,
                    sale.tax_amount,
                    sale.grand_total,
                    sale.amount_paid,
                    sale.change_given,
                    sale.sale_status,
                    sale.payment_method,
                    sale.momo_reference,
                    sale.notes,
                    sale.created_at,
                    sale.updated_at
                ))
            except Exception as e:
                print(f"Error inserting sale {sale.invoice_number}: {e}")
                raise
        
        print(f"✅ Successfully inserted {len(sales)} sales")
    
class SaleItemRepository:
    def __init__(self, db_context: DatabaseContext):
        self.db = db_context

    def _row_to_sale_item(self, row) -> Sale_Item:
        return Sale_Item(
            sale_item_id=row['sale_item_id'],
            sale_id=row['sale_id'],
            product_id=row['product_id'],
            quantity=row['quantity'],
            unit_price=row['unit_price'],
            discount_amount=row['discount_amount'],
            tax_rate=row['tax_rate'],
            tax_amount=row['tax_amount'],
            subtotal=row['subtotal'],
            line_total=row['line_total'],
            created_at=row['created_at'],
            updated_at=row['updated_at'],
        )
    
    def get_all_sale_items(self) -> List[Sale_Item]:
       self.db.execute("SELECT * FROM sale_items")
       return [self._row_to_sale_item(sale_item) for sale_item in self.db.fetchall()]
    
    def get_single_sale_items(self) -> Optional[Sale_Item]:
        self.db.execute("SELECT * FROM sale_items LIMIT 1")
        sale_item = self.db.fetchone()
        return self._row_to_sale_item(sale_item) if sale_item else None
    
    def delete_all_sale_items(self):
        self.db.execute("DELETE FROM sale_items")

    def save_or_upsert_single_sale_item(self, sale_item: Sale_Item):
        if sale_item.sale_item_id is None:
            self.db.execute('''
                INSERT INTO sale_items (
                    sale_item_id, sale_id, product_id, 
                    quantity, unit_price, discount_amount, 
                    tax_rate, tax_amount, subtotal, 
                    line_total, created_at, updated_at
                ) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                sale_item.sale_item_id,
                sale_item.sale_id,
                sale_item.product_id,
                sale_item.quantity,
                sale_item.unit_price,
                sale_item.discount_amount,
                sale_item.tax_rate,
                sale_item.tax_amount,
                sale_item.subtotal,
                sale_item.line_total,
                sale_item.created_at,
                sale_item.updated_at
            ))
            sale_item.sale_id = self.db.cursor.lastrowid
            print(f"Successfully inserted sale: {sale_item['sale_id']}")

        else:
            self.db.execute('''
                UPDATE sale_items SET
                    sale_id, product_id, quantity, 
                    unit_price, discount_amount, 
                    tax_rate, tax_amount, subtotal, 
                    line_total, created_at, updated_at
                WHERE sale_item_id = ?
            ''', (
            
            ))
            print(f"Updated existing sales: {sale_item['sale_item_id']}")
    
    def populate_sale_items_table_with_fake_data(self, number_of_rows=50):
        """
        Create fake sale items data with VALID foreign key references
        """
        # Clear existing sale items first
        self.delete_all_sale_items()
        
        # Get valid sale IDs that exist in the database
        self.db.execute("SELECT sale_id FROM sales")
        valid_sale_ids = [row['sale_id'] for row in self.db.fetchall()]
        
        # Get valid product IDs that exist in the database
        self.db.execute("SELECT product_id, unit_selling_price FROM products")
        valid_products = [row for row in self.db.fetchall()]
        
        if not valid_sale_ids:
            raise Exception("No sales found! Create sales first.")
        if not valid_products:
            raise Exception("No products found! Create products first.")

        sale_items = []
        for i in range(number_of_rows):
            # Get random sale and product
            sale_id = random.choice(valid_sale_ids)
            product = random.choice(valid_products)
            product_id = product['product_id']
            unit_price = product['unit_selling_price']  # Use actual product price
            
            # Generate realistic values
            quantity = random.randint(1, 10)
            discount_percent = random.uniform(0, 0.15)  # 0-15% discount
            tax_rate = 0.15  # Standard 15% VAT
            
            # Calculate line item totals
            subtotal = round(quantity * unit_price, 2)
            discount_amount = round(subtotal * discount_percent, 2)
            taxable_amount = subtotal - discount_amount
            tax_amount = round(taxable_amount * tax_rate, 2)
            line_total = round(taxable_amount + tax_amount, 2)

            sale_items.append(
                Sale_Item(
                    sale_item_id=None,  # Let database auto-generate
                    sale_id=sale_id,  # Use VALID sale ID
                    product_id=product_id,  # Use VALID product ID
                    quantity=quantity,
                    unit_price=unit_price,
                    discount_amount=discount_amount,
                    tax_rate=tax_rate,
                    tax_amount=tax_amount,
                    subtotal=subtotal,
                    line_total=line_total,
                    created_at=faker.date_time(),
                    updated_at=faker.date_time(),
                )
            )

        for sale_item in sale_items:
            try:
                print(f"Inserting sale item for sale_id: {sale_item.sale_id}")
                
                self.db.execute('''
                    INSERT INTO sale_items (
                        sale_id, product_id, quantity, 
                        unit_price, discount_amount, 
                        tax_rate, tax_amount, subtotal, 
                        line_total, created_at, updated_at
                    ) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    sale_item.sale_id,
                    sale_item.product_id,
                    sale_item.quantity,
                    sale_item.unit_price,
                    sale_item.discount_amount,
                    sale_item.tax_rate,
                    sale_item.tax_amount,
                    sale_item.subtotal,
                    sale_item.line_total,
                    sale_item.created_at,
                    sale_item.updated_at
                ))
            except Exception as e:
                print(f"Error inserting sale item: {e}")
                raise
        
        print(f"✅ Successfully inserted {len(sale_items)} sale items")

# ==================== PURCHASE REPOSITORY ====================
class PurchaseRepository:
    def __init__(self, db_context: DatabaseContext):
        self.db = db_context

    def _row_to_purchase(self, row) -> Purchase:
        return Purchase(
            purchase_id=row['purchase_id'],
            purchase_date=row['purchase_date'],
            purchase_invoice=row['purchase_invoice'],
            created_by=row['created_by'],
            subtotal=row['subtotal'],
            tax_amount=row['tax_amount'],
            grand_total=row['grand_total'],
            amount_paid=row['amount_paid'],
            balance=row['balance'],
            payment_status=row['payment_status'],
            purchase_status=row['purchase_status'],
            expected_delivery_date=row['expected_delivery_date'],
            received_date=row['received_date'],
            notes=row['notes'],
            created_at=row['created_at'],
            updated_at=row['updated_at'],
        )
    
    def get_all_purchases(self) -> List[Purchase]:
        self.db.execute("SELECT * FROM purchases")
        return [self._row_to_purchase(purchase) for purchase in self.db.fetchall()]
    
    def get_single_purchase(self) -> Optional[Purchase]:
        self.db.execute("SELECT * FROM purchases LIMIT 1")
        purchase = self.db.fetchone()
        return self._row_to_purchase(purchase) if purchase else None
    
    def delete_all_purchases(self):
        self.db.execute("DELETE FROM purchases")

    def save_or_upsert_single_purchase(self, purchase: Purchase):
        if purchase.purchase_id is None:
            self.db.execute('''
                INSERT INTO purchases (
                    purchase_date, purchase_invoice, created_by, 
                    subtotal, tax_amount, grand_total, 
                    amount_paid, balance, payment_status, 
                    purchase_status, expected_delivery_date, 
                    received_date, notes, created_at, updated_at
                ) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                purchase.purchase_date,
                purchase.purchase_invoice,
                purchase.created_by,
                purchase.subtotal,
                purchase.tax_amount,
                purchase.grand_total,
                purchase.amount_paid,
                purchase.balance,
                purchase.payment_status,
                purchase.purchase_status,
                purchase.expected_delivery_date,
                purchase.received_date,
                purchase.notes,
                purchase.created_at,
                purchase.updated_at
            ))
            purchase.purchase_id = self.db.cursor.lastrowid
            print(f"Successfully inserted purchase: {purchase.purchase_id}")
        else:
            self.db.execute('''
                UPDATE purchases SET
                    purchase_date = ?, purchase_invoice = ?, created_by = ?, 
                    subtotal = ?, tax_amount = ?, grand_total = ?, 
                    amount_paid = ?, balance = ?, payment_status = ?, 
                    purchase_status = ?, expected_delivery_date = ?, 
                    received_date = ?, notes = ?, updated_at = ?
                WHERE purchase_id = ?
            ''', (
                purchase.purchase_date,
                purchase.purchase_invoice,
                purchase.created_by,
                purchase.subtotal,
                purchase.tax_amount,
                purchase.grand_total,
                purchase.amount_paid,
                purchase.balance,
                purchase.payment_status,
                purchase.purchase_status,
                purchase.expected_delivery_date,
                purchase.received_date,
                purchase.notes,
                purchase.updated_at,
                purchase.purchase_id
            ))
            print(f"Updated existing purchase: {purchase.purchase_id}")
        
    def populate_purchases_table_with_fake_data(self, number_of_rows=50):
        """Create fake purchase data with VALID foreign key references"""
        # Clear existing purchases first
        self.delete_all_purchases()
        
        # Get valid usernames that exist in the database for created_by
        self.db.execute("SELECT username FROM users")
        valid_usernames = [row['username'] for row in self.db.fetchall()]
        
        if not valid_usernames:
            raise Exception("No users found! Create users first.")

        purchases = []
        for i in range(number_of_rows):
            subtotal = round(random.uniform(100, 5000), 2)
            tax_amount = round(subtotal * 0.15, 2)  # 15% VAT
            grand_total = round(subtotal + tax_amount, 2)
            amount_paid = round(random.uniform(0, grand_total), 2)
            
            # Determine payment status based on amount paid
            if amount_paid == 0:
                payment_status = 'unpaid'
            elif amount_paid < grand_total:
                payment_status = 'partial'
            else:
                payment_status = 'paid'
            
            # Determine purchase status
            purchase_status = random.choice(['pending', 'ordered', 'partially_received', 'received', 'cancelled'])
            
            # Generate simple dates
            purchase_date = faker.date_this_year()
            expected_delivery_date = faker.date_between(start_date=purchase_date, end_date='+30d')
            
            # Only set date_received if status is received or partially_received
            if purchase_status in ['received', 'partially_received']:
                date_received = faker.date_between(start_date=purchase_date, end_date=expected_delivery_date)
            else:
                date_received = None

            purchases.append(
                Purchase(
                    purchase_id=None,  # Let database auto-generate
                    purchase_date=purchase_date.strftime('%Y-%m-%d'),
                    purchase_invoice=f"PINV-{faker.random_number(digits=6)}",
                    created_by=random.choice(valid_usernames),  # Use VALID username
                    subtotal=subtotal,
                    tax_amount=tax_amount,
                    grand_total=grand_total,
                    amount_paid=amount_paid,
                    payment_status=payment_status,
                    purchase_status=purchase_status,
                    expected_delivery_date=expected_delivery_date.strftime('%Y-%m-%d'),
                    date_received=date_received.strftime('%Y-%m-%d') if date_received else None,
                    notes=faker.text(max_nb_chars=100),
                    created_at=faker.date_time(),
                    updated_at=faker.date_time(),
                )
            )

        for purchase in purchases:
            try:
                print(f"Inserting purchase invoice: {purchase.purchase_invoice}")
                
                self.db.execute('''
                    INSERT INTO purchases (
                        purchase_date, purchase_invoice, created_by, 
                        subtotal, tax_amount, grand_total, 
                        amount_paid, payment_status, 
                        purchase_status, expected_delivery_date, 
                        date_received, notes, created_at, updated_at
                    ) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    purchase.purchase_date,
                    purchase.purchase_invoice,
                    purchase.created_by,
                    purchase.subtotal,
                    purchase.tax_amount,
                    purchase.grand_total,
                    purchase.amount_paid,
                    purchase.payment_status,
                    purchase.purchase_status,
                    purchase.expected_delivery_date,
                    purchase.date_received,
                    purchase.notes,
                    purchase.created_at,
                    purchase.updated_at
                ))
            except Exception as e:
                print(f"Error inserting purchase {purchase.purchase_invoice}: {e}")
                raise
        
        print(f"✅ Successfully inserted {len(purchases)} purchases")

# ==================== PURCHASE ITEMS REPOSITORY ====================
class PurchaseItemsRepository:
    def __init__(self, db_context: DatabaseContext):
        self.db = db_context

    def _row_to_purchase_item(self, row) -> Purchase_Items:
        return Purchase_Items(
            purchase_item_id=row['purchase_item_id'],
            purchase_id=row['purchase_id'],
            product_id=row['product_id'],
            quantity=row['quantity'],
            unit_cost=row['unit_cost'],
            subtotal=row['subtotal'],
            created_at=row['created_at'],
        )
    
    def get_all_purchase_items(self) -> List[Purchase_Items]:
        self.db.execute("SELECT * FROM purchase_items")
        return [self._row_to_purchase_item(item) for item in self.db.fetchall()]
    
    def get_single_purchase_item(self) -> Optional[Purchase_Items]:
        self.db.execute("SELECT * FROM purchase_items LIMIT 1")
        item = self.db.fetchone()
        return self._row_to_purchase_item(item) if item else None
    
    def delete_all_purchase_items(self):
        self.db.execute("DELETE FROM purchase_items")

    def save_or_upsert_single_purchase_item(self, item: Purchase_Items):
        if item.purchase_item_id is None:
            self.db.execute('''
                INSERT INTO purchase_items (
                    purchase_id, product_id, quantity, 
                    unit_cost, subtotal, created_at
                ) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                item.purchase_id,
                item.product_id,
                item.quantity,
                item.unit_cost,
                item.subtotal,
                item.created_at
            ))
            item.purchase_item_id = self.db.cursor.lastrowid
            print(f"Successfully inserted purchase item: {item.purchase_item_id}")
        else:
            self.db.execute('''
                UPDATE purchase_items SET
                    purchase_id = ?, product_id = ?, quantity = ?, 
                    unit_cost = ?, subtotal = ?
                WHERE purchase_item_id = ?
            ''', (
                item.purchase_id,
                item.product_id,
                item.quantity,
                item.unit_cost,
                item.subtotal,
                item.purchase_item_id
            ))
            print(f"Updated existing purchase item: {item.purchase_item_id}")
    
    def populate_purchase_items_table_with_fake_data(self, number_of_rows=50):
        """Create fake purchase items data with VALID foreign key references"""
        # Clear existing purchase items first
        self.delete_all_purchase_items()
        
        # Get valid purchase IDs that exist in the database
        self.db.execute("SELECT purchase_id FROM purchases")
        valid_purchase_ids = [row['purchase_id'] for row in self.db.fetchall()]
        
        # Get valid product IDs that exist in the database
        self.db.execute("SELECT product_id FROM products")
        valid_product_ids = [row['product_id'] for row in self.db.fetchall()]
        
        if not valid_purchase_ids:
            raise Exception("No purchases found! Create purchases first.")
        if not valid_product_ids:
            raise Exception("No products found! Create products first.")

        items = []
        for i in range(number_of_rows):
            # Use valid IDs from the database
            purchase_id = random.choice(valid_purchase_ids)
            product_id = random.choice(valid_product_ids)
            
            quantity = random.randint(1, 100)
            unit_cost = round(random.uniform(10, 500), 2)
            subtotal = round(quantity * unit_cost, 2)

            items.append(
                Purchase_Items(
                    purchase_item_id=None,  # Let database auto-generate
                    purchase_id=purchase_id,  # Use VALID purchase ID
                    product_id=product_id,    # Use VALID product ID
                    quantity=quantity,
                    unit_cost=unit_cost,
                    subtotal=subtotal,
                    created_at=faker.date_time_this_year(),
                )
            )

        for item in items:
            try:
                print(f"Inserting purchase item for purchase_id: {item.purchase_id}")
                
                self.db.execute('''
                    INSERT INTO purchase_items (
                        purchase_id, product_id, quantity, 
                        unit_cost, subtotal, created_at
                    ) 
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    item.purchase_id,
                    item.product_id,
                    item.quantity,
                    item.unit_cost,
                    item.subtotal,
                    item.created_at
                ))
            except Exception as e:
                print(f"Error inserting purchase item: {e}")
                raise
        
        print(f"✅ Successfully inserted {len(items)} purchase items")

# ==================== PAYMENT REPOSITORY ====================
class PaymentRepository:
    def __init__(self, db_context: DatabaseContext):
        self.db = db_context

    def _row_to_payment(self, row) -> Payment:
        return Payment(
            payment_id=row['payment_id'],
            payment_date=row['payment_date'],
            transaction_type=row['transaction_type'],
            reference_id=row['reference_id'],
            amount=row['amount'],
            payment_method=row['payment_method'],
            payment_reference=row['payment_reference'],
            momo_provider=row['momo_provider'],
            momo_number=row['momo_number'],
            notes=row['notes'],
            processed_by=row['processed_by'],
            created_at=row['created_at'],
        )
    
    def get_all_payments(self) -> List[Payment]:
        self.db.execute("SELECT * FROM payments")
        return [self._row_to_payment(payment) for payment in self.db.fetchall()]
    
    def get_single_payment(self) -> Optional[Payment]:
        self.db.execute("SELECT * FROM payments LIMIT 1")
        payment = self.db.fetchone()
        return self._row_to_payment(payment) if payment else None
    
    def delete_all_payments(self):
        self.db.execute("DELETE FROM payments")

    def save_or_upsert_single_payment(self, payment: Payment):
        if payment.payment_id is None:
            self.db.execute('''
                INSERT INTO payments (
                    payment_date, transaction_type, reference_id, 
                    amount, payment_method, payment_reference, 
                    momo_provider, momo_number, notes, 
                    processed_by, created_at
                ) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                payment.payment_date,
                payment.transaction_type,
                payment.reference_id,
                payment.amount,
                payment.payment_method,
                payment.payment_reference,
                payment.momo_provider,
                payment.momo_number,
                payment.notes,
                payment.processed_by,
                payment.created_at
            ))
            payment.payment_id = self.db.cursor.lastrowid
            print(f"Successfully inserted payment: {payment.payment_id}")
        else:
            self.db.execute('''
                UPDATE payments SET
                    payment_date = ?, transaction_type = ?, reference_id = ?, 
                    amount = ?, payment_method = ?, payment_reference = ?, 
                    momo_provider = ?, momo_number = ?, notes = ?, 
                    processed_by = ?
                WHERE payment_id = ?
            ''', (
                payment.payment_date,
                payment.transaction_type,
                payment.reference_id,
                payment.amount,
                payment.payment_method,
                payment.payment_reference,
                payment.momo_provider,
                payment.momo_number,
                payment.notes,
                payment.processed_by,
                payment.payment_id
            ))
            print(f"Updated existing payment: {payment.payment_id}")
    
    def populate_payments_table_with_fake_data(self, number_of_rows=50):
        """Create fake payment data with VALID foreign key references"""
        # Clear existing payments first
        self.delete_all_payments()
        
        # Get valid usernames that exist in the database for processed_by
        self.db.execute("SELECT username FROM users")
        valid_usernames = [row['username'] for row in self.db.fetchall()]
        
        # Get valid sale IDs for reference_id
        self.db.execute("SELECT sale_id FROM sales")
        valid_sale_ids = [row['sale_id'] for row in self.db.fetchall()]
        
        # Get valid purchase IDs for reference_id
        self.db.execute("SELECT purchase_id FROM purchases")
        valid_purchase_ids = [row['purchase_id'] for row in self.db.fetchall()]
        
        if not valid_usernames:
            raise Exception("No users found! Create users first.")
        if not valid_sale_ids and not valid_purchase_ids:
            raise Exception("No sales or purchases found! Create sales or purchases first.")

        payments = []
        for i in range(number_of_rows):
            # Choose transaction type and get appropriate reference ID
            transaction_type = random.choice(['sale', 'purchase', 'refund'])
            
            if transaction_type == 'sale' and valid_sale_ids:
                reference_id = random.choice(valid_sale_ids)
                amount = round(random.uniform(10, 1000), 2)  # Smaller amounts for sales
            elif transaction_type == 'purchase' and valid_purchase_ids:
                reference_id = random.choice(valid_purchase_ids)
                amount = round(random.uniform(100, 5000), 2)  # Larger amounts for purchases
            else:
                # If no valid IDs for chosen type, use what's available
                if valid_sale_ids:
                    reference_id = random.choice(valid_sale_ids)
                    transaction_type = 'sale'
                    amount = round(random.uniform(10, 1000), 2)
                else:
                    reference_id = random.choice(valid_purchase_ids)
                    transaction_type = 'purchase'
                    amount = round(random.uniform(100, 5000), 2)
            
            payment_method = random.choice(['cash', 'momo', 'card', 'bank_transfer', 'cheque'])
            
            # Only set momo fields if payment method is momo
            if payment_method == 'momo':
                momo_provider = random.choice(['mtn', 'vodafone', 'airteltigo'])
                momo_number = faker.phone_number()
            else:
                momo_provider = None
                momo_number = None

            payments.append(
                Payment(
                    payment_id=None,  # Let database auto-generate
                    payment_date=faker.date_time_this_year().strftime('%Y-%m-%d'),
                    transaction_type=transaction_type,
                    reference_id=reference_id,  # Use VALID reference ID
                    amount=amount,
                    payment_method=payment_method,
                    payment_reference=f"PAY-{faker.random_number(digits=8)}",
                    momo_provider=momo_provider,
                    momo_number=momo_number,
                    notes=faker.text(max_nb_chars=100),
                    processed_by=random.choice(valid_usernames),  # Use VALID username
                    created_at=faker.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S'),
                )
            )

        for payment in payments:
            try:
                print(f"Inserting payment: {payment.payment_reference}")
                
                self.db.execute('''
                    INSERT INTO payments (
                        payment_date, transaction_type, reference_id, 
                        amount, payment_method, payment_reference, 
                        momo_provider, momo_number, notes, 
                        processed_by, created_at
                    ) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    payment.payment_date,
                    payment.transaction_type,
                    payment.reference_id,
                    payment.amount,
                    payment.payment_method,
                    payment.payment_reference,
                    payment.momo_provider,
                    payment.momo_number,
                    payment.notes,
                    payment.processed_by,
                    payment.created_at
                ))
            except Exception as e:
                print(f"Error inserting payment {payment.payment_reference}: {e}")
                raise
        
        print(f"✅ Successfully inserted {len(payments)} payments")

# ==================== AUDIT LOG REPOSITORY ====================
class AuditLogRepository:
    def __init__(self, db_context: DatabaseContext):
        self.db = db_context

    def _row_to_audit_log(self, row) -> Audit_Log:
        return Audit_Log(
            audit_id=row['audit_id'],
            user_id=row['user_id'],
            action=row['action'],
            description=row['description'],
            table_name=row['table_name'],
            created_at=row['created_at'],
        )
    
    def get_all_audit_logs(self) -> List[Audit_Log]:
        self.db.execute("SELECT * FROM audit_logs")
        return [self._row_to_audit_log(log) for log in self.db.fetchall()]
    
    def get_single_audit_log(self) -> Optional[Audit_Log]:
        self.db.execute("SELECT * FROM audit_logs LIMIT 1")
        log = self.db.fetchone()
        return self._row_to_audit_log(log) if log else None
    
    def delete_all_audit_logs(self):
        self.db.execute("DELETE FROM audit_logs")

    def save_or_upsert_single_audit_log(self, log: Audit_Log):
        if log.audit_id is None:
            self.db.execute('''
                INSERT INTO audit_logs (
                    user_id, action, description, 
                    table_name, created_at
                ) 
                VALUES (?, ?, ?, ?, ?)
            ''', (
                log.user_id,
                log.action,
                log.description,
                log.table_name,
                log.created_at
            ))
            log.audit_id = self.db.cursor.lastrowid
            print(f"Successfully inserted audit log: {log.audit_id}")
        else:
            self.db.execute('''
                UPDATE audit_logs SET
                    user_id = ?, action = ?, description = ?, 
                    table_name = ?
                WHERE audit_id = ?
            ''', (
                log.user_id,
                log.action,
                log.description,
                log.table_name,
                log.audit_id
            ))
            print(f"Updated existing audit log: {log.audit_id}")
    
    def populate_audit_logs_table_with_fake_data(self, number_of_rows=50):
        """Create fake audit log data with VALID foreign key references"""
        # Clear existing audit logs first
        self.delete_all_audit_logs()
        
        # Get valid user IDs that exist in the database
        self.db.execute("SELECT user_id FROM users")
        valid_user_ids = [row['user_id'] for row in self.db.fetchall()]
        
        if not valid_user_ids:
            raise Exception("No users found! Create users first.")

        # Valid table names from your actual database schema
        valid_tables = ['sales', 'purchases', 'products', 'clients', 'payments', 'users', 'categories', 'suppliers']
        
        # Common actions with realistic descriptions
        actions = {
            'INSERT': 'Created new record in',
            'UPDATE': 'Modified existing record in', 
            'DELETE': 'Removed record from',
            'SELECT': 'Viewed records in',
            'LOGIN': 'User logged into system',
            'LOGOUT': 'User logged out of system'
        }

        logs = []
        for i in range(number_of_rows):
            user_id = random.choice(valid_user_ids)
            action = random.choice(list(actions.keys()))
            table_name = random.choice(valid_tables)
            
            # Create realistic description based on action and table
            if action in ['LOGIN', 'LOGOUT']:
                description = actions[action]
                table_name = 'system'  # Special case for login/logout
            else:
                description = f"{actions[action]} {table_name} table"

            logs.append(
                Audit_Log(
                    audit_id=None,  # Let database auto-generate
                    user_id=user_id,  # Use VALID user ID
                    action=action,
                    description=description,
                    table_name=table_name,
                    created_at=faker.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S'),
                )
            )

        for log in logs:
            try:
                print(f"Inserting audit log for user_id: {log.user_id} - {log.action} on {log.table_name}")
                
                self.db.execute('''
                    INSERT INTO audit_logs (
                        user_id, action, description, 
                        table_name, created_at
                    ) 
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    log.user_id,
                    log.action,
                    log.description,
                    log.table_name,
                    log.created_at
                ))
            except Exception as e:
                print(f"Error inserting audit log: {e}")
                raise
        
        print(f"✅ Successfully inserted {len(logs)} audit logs")

# ==================== REPORT REPOSITORY ====================
class ReportRepository:
    def __init__(self, db_context: DatabaseContext):
        self.db = db_context

    def _row_to_report(self, row) -> Report:
        return Report(
            report_id=row['report_id'],
            report_type=row['report_type'],
            report_title=row['report_title'],
            generated_by=row['generated_by'],
            start_date=row['start_date'],
            end_date=row['end_date'],
            filters=row['filters'],
            file_format=row['file_format'],
            status=row['status'],
            created_at=row['created_at'],
        )
    
    def get_all_reports(self) -> List[Report]:
        self.db.execute("SELECT * FROM reports")
        return [self._row_to_report(report) for report in self.db.fetchall()]
    
    def get_single_report(self) -> Optional[Report]:
        self.db.execute("SELECT * FROM reports LIMIT 1")
        report = self.db.fetchone()
        return self._row_to_report(report) if report else None
    
    def delete_all_reports(self):
        self.db.execute("DELETE FROM reports")

    def save_or_upsert_single_report(self, report: Report):
        if report.report_id is None:
            self.db.execute('''
                INSERT INTO reports (
                    report_type, report_title, generated_by, 
                    start_date, end_date, filters, 
                    file_format, status, created_at
                ) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                report.report_type,
                report.report_title,
                report.generated_by,
                report.start_date,
                report.end_date,
                report.filters,
                report.file_format,
                report.status,
                report.created_at
            ))
            report.report_id = self.db.cursor.lastrowid
            print(f"Successfully inserted report: {report.report_id}")
        else:
            self.db.execute('''
                UPDATE reports SET
                    report_type = ?, report_title = ?, generated_by = ?, 
                    start_date = ?, end_date = ?, filters = ?, 
                    file_format = ?, status = ?
                WHERE report_id = ?
            ''', (
                report.report_type,
                report.report_title,
                report.generated_by,
                report.start_date,
                report.end_date,
                report.filters,
                report.file_format,
                report.status,
                report.report_id
            ))
            print(f"Updated existing report: {report.report_id}")
    
    def populate_reports_table_with_fake_data(self, number_of_rows=50):
        """Create fake report data with VALID foreign key references"""
        # Clear existing reports first
        self.delete_all_reports()
        
        # Get valid user IDs that exist in the database for generated_by
        self.db.execute("SELECT user_id FROM users")
        valid_user_ids = [row['user_id'] for row in self.db.fetchall()]
        
        if not valid_user_ids:
            raise Exception("No users found! Create users first.")

        reports = []
        for i in range(number_of_rows):
            # Ensure end_date is after start_date
            start_date = faker.date_this_year()
            end_date = faker.date_between(start_date=start_date, end_date='+30d')
            
            report_type = random.choice(['sales', 'purchases', 'clients', 'products', 'custom'])
            
            # Create realistic report titles based on type
            report_titles = {
                'sales': ['Daily Sales Summary', 'Monthly Revenue Report', 'Product Performance Analysis', 'Sales by Category'],
                'purchases': ['Vendor Purchase History', 'Monthly Procurement Report', 'Supplier Performance Analysis'],
                'clients': ['Customer Database Export', 'Client Purchase History', 'Customer Segmentation Report'],
                'products': ['Inventory Stock Report', 'Product Profitability Analysis', 'Low Stock Alert Report'],
                'custom': ['Custom Business Analysis', 'Financial Summary Report', 'Operational Efficiency Report']
            }
            
            report_title = random.choice(report_titles[report_type])

            # Create simple filter examples
            filter_examples = {
                'sales': '{"date_range": "last_30_days", "category": "all"}',
                'purchases': '{"supplier": "all", "status": "completed"}',
                'clients': '{"client_type": "business", "active_only": true}',
                'products': '{"category": "electronics", "low_stock": true}',
                'custom': '{"custom_filters": "business_analysis"}'
            }

            reports.append(
                Report(
                    report_id=None,  # Let database auto-generate
                    report_type=report_type,
                    report_title=report_title,
                    generated_by=random.choice(valid_user_ids),  # Use VALID user ID
                    start_date=start_date.strftime('%Y-%m-%d'),
                    end_date=end_date.strftime('%Y-%m-%d'),
                    filters=filter_examples[report_type],
                    file_format=random.choice(['pdf', 'excel', 'csv']),
                    status=random.choice(['pending', 'completed', 'failed']),
                    created_at=faker.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S'),
                )
            )

        for report in reports:
            try:
                print(f"Inserting report: {report.report_title}")
                
                self.db.execute('''
                    INSERT INTO reports (
                        report_type, report_title, generated_by, 
                        start_date, end_date, filters, 
                        file_format, status, created_at
                    ) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    report.report_type,
                    report.report_title,
                    report.generated_by,
                    report.start_date,
                    report.end_date,
                    report.filters,
                    report.file_format,
                    report.status,
                    report.created_at
                ))
            except Exception as e:
                print(f"Error inserting report {report.report_title}: {e}")
                raise
        
        print(f"✅ Successfully inserted {len(reports)} reports")
    