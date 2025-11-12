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
    supplier_id: int
