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
    category_name: str
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
    is_active: bool
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

@dataclass
class Sale:
    sale_id: int
    invoice_number: str 
    sale_date: str
    client_id: int
    biller_id: int
    subtotal: float
    discount_amount: float
    tax_amount: float
    grand_total: float
    amount_paid: float
    change_given: float
    sale_status: str
    payment_method: str
    momo_reference: str
    notes: str
    created_at: datetime
    updated_at: datetime

@dataclass
class Sale_Item:
    sale_item_id: int
    sale_id: int
    product_id: int
    quantity: float
    unit_price: float
    discount_amount: float
    tax_rate: float
    tax_amount: float
    subtotal: float
    line_total: float
    created_at: datetime
    updated_at: datetime

@dataclass
class Purchase:
    purchase_id: int
    purchase_date: str
    purchase_invoice: int
    created_by: str
    subtotal: float
    tax_amount: float
    grand_total: float
    amount_paid: float
    balance: float
    payment_status: str
    purchase_status: str
    expected_delivery_date: str
    received_date: str
    notes: str
    created_at: datetime
    updated_at: datetime

@dataclass
class Purchase_Items:
    purchase_item_id: int
    purchase_id: int
    product_id: int
    quantity: float
    unit_cost: float
    subtotal: float
    created_at: datetime

@dataclass
class Payment:
    payment_id: int
    payment_date: str
    transaction_type: str
    reference_id: int
    amount: float
    payment_method: str
    payment_reference: str
    momo_provider: str
    momo_number: str
    notes: str
    processed_by: str
    created_at: str

@dataclass
class Audit_Log:
    audit_id: int
    user_id: int
    action: str
    description: str
    table_name: str
    created_at: str

@dataclass
class Report:
    report_id: int
    report_type: str
    report_title: str
    generated_by: int
    start_date: str
    end_date: str
    filters: str
    file_format: str
    status: str
    created_at: str
