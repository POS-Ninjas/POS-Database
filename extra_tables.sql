 -- ============================================
-- HOLDS (On-Hold Transactions)
-- ============================================

CREATE TABLE held_transactions (
    hold_id INT PRIMARY KEY AUTO_INCREMENT,
    hold_reference TEXT(50) NOT NULL UNIQUE,
    user_id INT NOT NULL, -- User who put transaction on hold
    customer_id INT NULL,
    hold_data JSON NOT NULL, -- Store cart items as JSON
    subtotal DECIMAL(15, 2) NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    INDEX idx_user (user_id),
    INDEX idx_reference (hold_reference)
);

-- ============================================
-- REFUNDS & RETURNS
-- ============================================

CREATE TABLE refunds (
    refund_id INT PRIMARY KEY AUTO_INCREMENT,
    refund_number TEXT(50) NOT NULL UNIQUE,
    sale_id INT NOT NULL,
    refund_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    refund_type ENUM('full', 'partial') NOT NULL,
    refund_amount DECIMAL(15, 2) NOT NULL,
    refund_method ENUM('cash', 'momo', 'card', 'credit_note') NOT NULL,
    reason TEXT,
    processed_by INT NOT NULL,
    approved_by INT NULL,
    status ENUM('pending', 'approved', 'rejected', 'completed') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sale_id) REFERENCES sales(sale_id),
    FOREIGN KEY (processed_by) REFERENCES users(user_id),
    FOREIGN KEY (approved_by) REFERENCES users(user_id),
    INDEX idx_sale (sale_id),
    INDEX idx_refund_date (refund_date)
);

CREATE TABLE refund_items (
    refund_item_id INT PRIMARY KEY AUTO_INCREMENT,
    refund_id INT NOT NULL,
    sale_item_id INT NOT NULL,
    quantity_returned DECIMAL(10, 2) NOT NULL,
    refund_amount DECIMAL(15, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (refund_id) REFERENCES refunds(refund_id) ON DELETE CASCADE,
    FOREIGN KEY (sale_item_id) REFERENCES sale_items(sale_item_id),
    INDEX idx_refund (refund_id)
);


-- ============================================
-- GHANA-SPECIFIC: TAX CONFIGURATION
-- ============================================

CREATE TABLE tax_rates (
    tax_id INT PRIMARY KEY AUTO_INCREMENT,
    tax_name TEXT(50) NOT NULL, -- VAT, NHIL, GETFund
    tax_code TEXT(20) UNIQUE,
    rate DECIMAL(5, 2) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    effective_from DATE NOT NULL,
    effective_to DATE NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ============================================
-- STOCK MOVEMENTS (Inventory Tracking)
-- ============================================

CREATE TABLE stock_movements (
    movement_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    product_id INT NOT NULL,
    movement_type ENUM('purchase', 'sale', 'adjustment', 'refund', 'damaged', 'expired') NOT NULL,
    quantity DECIMAL(10, 2) NOT NULL, -- Positive for in, negative for out
    reference_type TEXT(50), -- 'sale', 'purchase', 'adjustment'
    reference_id INT,
    old_stock DECIMAL(10, 2) NOT NULL,
    new_stock DECIMAL(10, 2) NOT NULL,
    notes TEXT,
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (created_by) REFERENCES users(user_id),
    INDEX idx_product (product_id),
    INDEX idx_movement_type (movement_type),
    INDEX idx_created_at (created_at)
);

-- ============================================
-- INITIAL DATA
-- ============================================

-- Default Roles
INSERT INTO roles (role_name, role_description, permissions) VALUES
('Super Admin', 'Full system access', '["all"]'),
('Manager', 'Store management access', '["view_sales", "create_sales", "view_reports", "manage_inventory", "manage_users"]'),
('Cashier', 'Basic sales operations', '["create_sales", "view_sales", "view_products"]'),
('Stock Keeper', 'Inventory management', '["view_inventory", "manage_inventory", "create_purchases"]');

-- Default Ghana Tax Rates
INSERT INTO tax_rates (tax_name, tax_code, rate, effective_from) VALUES
('VAT', 'VAT', 15.00, '2023-01-01'),
('NHIL', 'NHIL', 2.50, '2023-01-01'),
('GETFund', 'GETF', 2.50, '2023-01-01');

-- Default Category
INSERT INTO categories (category_name, category_code, description) VALUES
('General', 'GEN', 'General products');

-- ============================================
-- USEFUL VIEWS
-- ============================================

-- Sales Summary View
CREATE VIEW v_sales_summary AS
SELECT 
    s.sale_id,
    s.invoice_number,
    s.sale_date,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    CONCAT(u.first_name, ' ', u.last_name) AS biller_name,
    s.grand_total,
    s.payment_status,
    s.payment_method
FROM sales s
LEFT JOIN customers c ON s.customer_id = c.customer_id
JOIN users u ON s.biller_id = u.user_id;

-- Low Stock Alert View
CREATE VIEW v_low_stock_products AS
SELECT 
    p.product_id,
    p.product_name,
    p.product_code,
    p.current_stock,
    p.reorder_level,
    c.category_name
FROM products p
JOIN categories c ON p.category_id = c.category_id
WHERE p.current_stock <= p.reorder_level 
AND p.is_active = TRUE;

-- Customer Purchase History View
CREATE VIEW v_customer_purchases AS
SELECT 
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    COUNT(s.sale_id) AS total_transactions,
    COALESCE(SUM(s.grand_total), 0) AS total_spent,
    MAX(s.sale_date) AS last_purchase_date
FROM customers c
LEFT JOIN sales s ON c.customer_id = s.customer_id
GROUP BY c.customer_id;

-- ============================================
-- TRIGGERS
-- ============================================

-- Update stock after sale
DELIMITER //
CREATE TRIGGER after_sale_item_insert
AFTER INSERT ON sale_items
FOR EACH ROW
BEGIN
    UPDATE products 
    SET current_stock = current_stock - NEW.quantity
    WHERE product_id = NEW.product_id;
    
    INSERT INTO stock_movements (
        product_id, movement_type, quantity, reference_type, 
        reference_id, old_stock, new_stock, created_by
    )
    SELECT 
        NEW.product_id, 
        'sale', 
        -NEW.quantity, 
        'sale', 
        NEW.sale_id,
        current_stock + NEW.quantity,
        current_stock,
        (SELECT biller_id FROM sales WHERE sale_id = NEW.sale_id)
    FROM products 
    WHERE product_id = NEW.product_id;
END//

-- Update stock after purchase
CREATE TRIGGER after_purchase_item_insert
AFTER INSERT ON purchase_items
FOR EACH ROW
BEGIN
    UPDATE products 
    SET current_stock = current_stock + NEW.quantity
    WHERE product_id = NEW.product_id;
    
    INSERT INTO stock_movements (
        product_id, movement_type, quantity, reference_type, 
        reference_id, old_stock, new_stock, created_by
    )
    SELECT 
        NEW.product_id, 
        'purchase', 
        NEW.quantity, 
        'purchase', 
        NEW.purchase_id,
        current_stock - NEW.quantity,
        current_stock,
        (SELECT created_by FROM purchases WHERE purchase_id = NEW.purchase_id)
    FROM products 
    WHERE product_id = NEW.product_id;
END//

DELIMITER ;

-- ============================================
-- INDEXES FOR PERFORMANCE
-- ============================================

-- Additional composite indexes for common queries
CREATE INDEX idx_sales_date_customer ON sales(sale_date, customer_id);
CREATE INDEX idx_sales_date_status ON sales(sale_date, sale_status);
CREATE INDEX idx_products_category_active ON products(category_id, is_active);
CREATE INDEX idx_stock_movements_product_date ON stock_movements(product_id, created_at);