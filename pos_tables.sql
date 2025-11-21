-- ============================================
-- COMPLETE POS SYSTEM DATABASE SCHEMA
-- For SMEs in Ghana
-- ============================================

-- ============================================
-- USERS & AUTHENTICATION
-- ============================================

CREATE TABLE roles (
  role_id INTEGER PRIMARY KEY AUTOINCREMENT,
  role_name TEXT NOT NULL UNIQUE, -- Staff and Admin
  role_description TEXT,
  permissions TEXT, -- Store JSON as text: e.g. '["view_sales", "create_products", "manage_users"]'
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
);

CREATE TRIGGER update_roles_timestamp
AFTER UPDATE ON roles
FOR EACH ROW
BEGIN
  UPDATE roles SET updated_at = CURRENT_TIMESTAMP WHERE role_id = OLD.role_id;
END;

CREATE TABLE users (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  email TEXT UNIQUE,
  role_name TEXT NOT NULL,
  is_active BOOLEAN DEFAULT TRUE,
  last_login DATETIME,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (role_name) REFERENCES roles(role_name)
);

CREATE INDEX idx_username   ON users (username);
CREATE INDEX idx_user_email ON users (email);
CREATE INDEX idx_user_role_name ON users (role_name);

CREATE TRIGGER update_users_timestamp
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
  UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE user_id = OLD.user_id;
END;

-- ============================================
-- CUSTOMERS
-- ============================================

CREATE TABLE clients (
  client_id INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name TEXT,
  last_name TEXT,
  phone_number TEXT NOT NULL,
  email TEXT NOT NULL,
  tin TEXT NOT NULL , -- Tax Identification Number (Ghana format: 11 digits) - Use TEXT for leading zeros
  client_type TEXT NOT NULL CHECK(client_type IN ('customer', 'business')) DEFAULT 'customer',
  business_name TEXT NOT NULL,
  business_address TEXT,
  business_type TEXT NOT NULL CHECK(business_type IN ('customer', 'supplier', 'export')) DEFAULT 'customer',
  is_active BOOLEAN DEFAULT TRUE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  deleted_at DATETIME -- Soft delete
);

CREATE INDEX idx_client_phone  ON clients (phone_number);
CREATE INDEX idx_client_email  ON clients (email);
CREATE INDEX idx_client_tin    ON clients (tin);
CREATE INDEX idx_client_active ON clients (is_active);
CREATE INDEX idx_client_type   ON clients (client_type);
CREATE INDEX idx_client_business_type ON clients (business_type);

CREATE TRIGGER update_clients_timestamp
AFTER UPDATE ON clients
FOR EACH ROW
BEGIN
  UPDATE clients SET updated_at = CURRENT_TIMESTAMP WHERE client_id = OLD.client_id;
END;

-- ============================================
-- PRODUCTS & INVENTORY
-- ============================================

CREATE TABLE categories (
  category_id INTEGER PRIMARY KEY AUTOINCREMENT,
  category_name TEXT NOT NULL,
  category_code TEXT UNIQUE,
  description TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
);

CREATE TRIGGER update_categories_timestamp
AFTER UPDATE ON categories
FOR EACH ROW
BEGIN
  UPDATE categories SET updated_at = CURRENT_TIMESTAMP WHERE category_id = OLD.category_id;
END;

CREATE TABLE suppliers (
  supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
  company_name TEXT NOT NULL,
  contact_name TEXT,
  email TEXT,
  phone_number TEXT NOT NULL,
  tin TEXT NOT NULL, 
  address TEXT,
  is_active BOOLEAN DEFAULT TRUE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
);

CREATE INDEX idx_supplier_company ON suppliers (company_name);
CREATE INDEX idx_supplier_phone   ON suppliers (phone_number);
CREATE INDEX idx_supplier_tin     ON suppliers (tin);
CREATE INDEX idx_supplier_active  ON suppliers (is_active);

CREATE TRIGGER update_suppliers_timestamp
AFTER UPDATE ON suppliers
FOR EACH ROW
BEGIN
  UPDATE suppliers SET updated_at = CURRENT_TIMESTAMP WHERE supplier_id = OLD.supplier_id;
END;

CREATE TABLE products (
  product_id INTEGER PRIMARY KEY AUTOINCREMENT,
  product_name TEXT NOT NULL,
  product_code TEXT UNIQUE,
  barcode TEXT UNIQUE,
  category_id INTEGER,
  supplier_id INTEGER,
  image_url TEXT,
  description TEXT,
  unit_purchase_price REAL NOT NULL DEFAULT 0.00,
  unit_selling_price REAL NOT NULL,
  current_stock INTEGER DEFAULT 0,
  reorder_level INTEGER DEFAULT 10,
  product_type TEXT NOT NULL CHECK(product_type IN ('goods', 'service')) DEFAULT 'goods',
  tax_rate REAL DEFAULT 15.00, -- Ghana VAT: 15%
  is_taxable BOOLEAN DEFAULT TRUE,
  is_active BOOLEAN DEFAULT TRUE,
  is_tax_inclusive BOOLEAN DEFAULT FALSE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  deleted_at DATETIME,
  FOREIGN KEY (category_id) REFERENCES categories(category_id),
  FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
);

CREATE INDEX idx_product_code     ON products (product_code);
CREATE INDEX idx_product_barcode  ON products (barcode);
CREATE INDEX idx_product_category ON products (category_id);
CREATE INDEX idx_product_supplier ON products (supplier_id);  -- Added: Useful for supplier reports
CREATE INDEX idx_product_active   ON products (is_active);

CREATE TRIGGER update_products_timestamp
AFTER UPDATE ON products
FOR EACH ROW
BEGIN
  UPDATE products SET updated_at = CURRENT_TIMESTAMP WHERE product_id = OLD.product_id;
END;

-- ============================================
-- SALES
-- ============================================

CREATE TABLE sales (
  sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
  invoice_number TEXT NOT NULL UNIQUE,
  sale_date DATETIME DEFAULT CURRENT_TIMESTAMP,
  client_id INTEGER, -- Nullable for walk-in clients
  biller_id INTEGER NOT NULL, -- User who processed the sale
  subtotal REAL NOT NULL,
  discount_amount REAL DEFAULT 0.00,
  tax_amount REAL DEFAULT 0.00, -- Total VAT/NHIL/GETFund
  grand_total REAL NOT NULL,
  amount_paid REAL NOT NULL,
  change_given REAL DEFAULT 0.00,
  sale_status TEXT NOT NULL CHECK(sale_status IN ('completed', 'cancelled', 'refunded', 'on_hold')) DEFAULT 'on_hold',
  payment_method TEXT NOT NULL CHECK(payment_method IN ('cash', 'momo', 'card', 'bank_transfer', 'credit')) DEFAULT 'cash',
  momo_reference TEXT, -- For mobile money transactions
  notes TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (client_id) REFERENCES clients(client_id),
  FOREIGN KEY (biller_id) REFERENCES users(user_id)
);

CREATE INDEX idx_sales_invoice ON sales (invoice_number);
CREATE INDEX idx_sales_date    ON sales (sale_date);
CREATE INDEX idx_sales_client  ON sales (client_id);
CREATE INDEX idx_sales_biller  ON sales (biller_id);

CREATE TRIGGER update_sales_timestamp
AFTER UPDATE ON sales
FOR EACH ROW
BEGIN
  UPDATE sales SET updated_at = CURRENT_TIMESTAMP WHERE sale_id = OLD.sale_id;
END;

CREATE TABLE sale_items (
  sale_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
  sale_id INTEGER NOT NULL,
  product_id INTEGER NOT NULL,
  quantity REAL NOT NULL,
  unit_price REAL NOT NULL,
  discount_amount REAL DEFAULT 0.00,
  tax_rate REAL DEFAULT 15.00,
  tax_amount REAL DEFAULT 0.00,
  total_levies REAL GENERATED ALWAYS AS ((unit_price * quantity) * 0.05) VIRTUAL,
  subtotal REAL NOT NULL,
  line_total REAL NOT NULL, -- subtotal - discount + tax
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (sale_id) REFERENCES sales(sale_id) ON DELETE CASCADE,
  FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE INDEX idx_sales_items ON sale_items (sale_id);
CREATE INDEX idx_sales_items_product ON sale_items (product_id);
CREATE INDEX idx_sales_items_created ON sale_items (created_at);

CREATE TRIGGER update_sale_items_timestamp
AFTER UPDATE ON sale_items
FOR EACH ROW
BEGIN
  UPDATE sale_items SET updated_at = CURRENT_TIMESTAMP WHERE sale_item_id = OLD.sale_item_id;
END;

-- ============================================
-- PURCHASES
-- ============================================

CREATE TABLE purchases (
  purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
  purchase_date DATE DEFAULT CURRENT_TIMESTAMP,
  purchase_invoice TEXT,
  created_by TEXT NOT NULL,
  subtotal REAL NOT NULL DEFAULT 0.00,
  tax_amount REAL DEFAULT 0.00,
  grand_total REAL NOT NULL DEFAULT 0.00,
  amount_paid REAL DEFAULT 0.00,
  balance REAL GENERATED ALWAYS AS (grand_total - amount_paid) VIRTUAL,
  payment_status TEXT NOT NULL CHECK(payment_status IN ('paid', 'partial', 'unpaid')) DEFAULT 'unpaid',
  purchase_status TEXT NOT NULL CHECK(purchase_status IN ('pending', 'ordered', 'partially_received', 'received', 'cancelled')) DEFAULT 'pending',
  expected_delivery_date DATE,
  date_received DATE,
  notes TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (created_by) REFERENCES users(username)
);

-- Comprehensive indexes
CREATE INDEX idx_purchase_date           ON purchases (purchase_date);
CREATE INDEX idx_purchase_payment_status ON purchases (payment_status);
CREATE INDEX idx_purchase_status         ON purchases (purchase_status);
CREATE INDEX idx_purchase_invoice        ON purchases (purchase_invoice);
CREATE INDEX idx_purchase_expected_date  ON purchases (expected_delivery_date);
CREATE INDEX idx_purchase_received_date  ON purchases (date_received);

-- Update DATETIME trigger
CREATE TRIGGER update_purchases_timestamp
AFTER UPDATE ON purchases
FOR EACH ROW
BEGIN
  UPDATE purchases SET updated_at = CURRENT_TIMESTAMP WHERE purchase_id = OLD.purchase_id;
END;

CREATE TABLE purchase_items (
  purchase_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
  purchase_id INTEGER NOT NULL,
  product_id INTEGER NOT NULL,
  quantity REAL NOT NULL CHECK(quantity > 0),
  unit_cost REAL NOT NULL CHECK(unit_cost >= 0),
  subtotal REAL NOT NULL CHECK(subtotal >= 0),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (purchase_id) REFERENCES purchases(purchase_id) ON DELETE CASCADE,
  FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Comprehensive indexes
CREATE INDEX idx_purchase_items_purchase ON purchase_items (purchase_id);
CREATE INDEX idx_purchase_items_product  ON purchase_items (product_id);
CREATE INDEX idx_purchase_items_created  ON purchase_items (created_at);

-- Update DATETIME trigger
CREATE TRIGGER update_purchase_items_timestamp
AFTER UPDATE ON purchase_items
FOR EACH ROW
BEGIN
  UPDATE purchase_items SET updated_at = CURRENT_TIMESTAMP WHERE purchase_item_id = OLD.purchase_item_id;
END;

-- ============================================
-- PAYMENTS
-- ============================================

CREATE TABLE payments (
  payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
  payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
  transaction_type TEXT NOT NULL CHECK(transaction_type IN ('sale', 'purchase', 'refund', 'expense')) DEFAULT 'sale',
  reference_id INTEGER NOT NULL, -- sale_id or purchase_id
  amount REAL NOT NULL,
  payment_method TEXT NOT NULL CHECK(payment_method IN ('cash', 'momo', 'card', 'bank_transfer', 'cheque')) DEFAULT 'cash',
  payment_reference TEXT, -- Bank/Momo reference number
  momo_provider TEXT CHECK(momo_provider IS NULL OR momo_provider IN ('mtn', 'vodafone', 'airteltigo')), -- For Ghana Mobile Money
  momo_number TEXT,
  notes TEXT,
  processed_by TEXT NOT NULL, -- User who processed payment
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (processed_by) REFERENCES users (username)
);

CREATE INDEX idx_transaction_type ON payments (transaction_type);
CREATE INDEX idx_reference        ON payments (reference_id);
CREATE INDEX idx_payment_date     ON payments (payment_date);
CREATE INDEX idx_payments_method  ON payments (payment_method);

-- ============================================
-- AUDIT & REPORTS
-- ============================================

CREATE TABLE audit_logs (
    audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    action TEXT NOT NULL,
    description TEXT,  -- Added: Store what actually changed
    table_name TEXT,  -- Added: Which table was affected
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE INDEX idx_audit_logs_user       ON audit_logs (user_id);
CREATE INDEX idx_audit_logs_action     ON audit_logs (action);
CREATE INDEX idx_audit_logs_created_at ON audit_logs (created_at);
CREATE INDEX idx_audit_logs_table      ON audit_logs (table_name);  -- Added

CREATE TABLE reports (
  report_id INTEGER PRIMARY KEY AUTOINCREMENT,
  report_type TEXT NOT NULL CHECK(report_type IN ('sales', 'purchases', 'clients', 'products', 'custom')) DEFAULT 'custom',
  report_title TEXT NOT NULL,
  generated_by INTEGER NOT NULL,
  start_date DATE,
  end_date DATE,
  filters TEXT, -- Store report parameters
  file_path TEXT,
  file_format TEXT NOT NULL CHECK(file_format IN ('pdf', 'excel', 'csv')) DEFAULT 'pdf',
  status TEXT NOT NULL CHECK(status IN ('pending', 'completed', 'failed')) DEFAULT 'pending',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (generated_by) REFERENCES users(user_id)
);

CREATE INDEX idx_reports_type   ON reports (report_type);
CREATE INDEX idx_generated_by   ON reports (generated_by);
CREATE INDEX idx_reports_status ON reports (status);  