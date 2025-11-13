from dataclasses import dataclass
import datetime

@dataclass
class Role:
    role_id: int
    role_name: str
    role_description: str | None
    permissions: str | None
    created_at: str
    updated_at: str

@dataclass
class User:
    user_id: int
    username: str
    password_hash: str
    first_name: str
    last_name: str 
    email: str | None
    role_name: str
    is_active: bool
    last_login: datetime
    created_at: datetime
    updated_at: datetime

@dataclass
class Client:
    client_id: int
    first_name: str
    last_name: str
    phone_number: str | None
    email: str
    tin: str 
    client_type: str
    business_name: str | None
    business_address: str
    business_type: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime

@dataclass
class Category:
    category_id: int
    company_name: str
    category_code: str | None
    description: str
    created_at: datetime
    updated_at: datetime

@dataclass
class Supplier:
    supplier_id: int
    company_name: str
    contact_name: str
    email: str
    phone_number: str
    tin: str
    address: str
    is_acitve: str
    created_at: datetime
    updated_at: datetime

@dataclass
class Product:
    product_id: int
    product_name: str 
    product_code: str | None
    barcode: str | None
    category_id: int | None
    supplier_id: int | None
    image_url: str | None
    description: str | None
    unit_purchase_price: float
    unit_selling_price: float
    current_stock: int
    reorder_level: int
    product_type: str
    tax_rate: float
    is_taxable: bool
    is_tax_inclusive: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime
