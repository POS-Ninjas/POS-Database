from dataclasses import dataclass
import datetime

"""
    Table Roles has role_id, role_name, role_description
    permissions, created_at, updated_at
"""

@dataclass
class Roles:
    role_id: int
    role_name: str
    role_description: str | None
    permissions: str | None
    created_at: str
    updated_at: str

"""
    Table User has user_id, username, password_hash, first_name, last_name
    email, role_id, is_active, last_login, created_at, updated_at,
"""

@dataclass
class User:
    user_id: int
    username: str
    password_hash: str
    first_name: str
    last_name: str 
    email: str
    role_name: str
    is_active: bool
    last_login: datetime
    created_at: str
    updated_at: str
