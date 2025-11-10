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
('General', 'GEN', 'General products'),
('Electronics', 'ELEC', 'Electronic items'),
('Food & Beverages', 'FOOD', 'Food and beverage products'),
('Clothing', 'CLOTH', 'Clothing and apparel');

-- ============================================
-- USEFUL VIEWS
-- ============================================

-- Sales Summary View
CREATE VIEW v_sales_summary AS
SELECT 
    s.sale_id,
    s.invoice_number,
    s.sale_date,
    COALESCE(c.first_name || ' ' || c.last_name, c.business_name, 'Walk-in') AS customer_name,
    u.first_name || ' ' || u.last_name AS biller_name,
    s.grand_total,
    s.payment_status,
    s.payment_method,
    s.sale_status
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
    c.category_name,
    s.company_name AS supplier_name
FROM products p
JOIN categories c ON p.category_id = c.category_id
LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
WHERE p.current_stock <= p.reorder_level 
AND p.is_active = 1
AND p.deleted_at IS NULL;

-- Customer Purchase History View
CREATE VIEW v_customer_purchases AS
SELECT 
    c.customer_id,
    COALESCE(c.first_name || ' ' || c.last_name, c.business_name) AS customer_name,
    c.phone_number,
    c.email,
    COUNT(s.sale_id) AS total_transactions,
    COALESCE(SUM(s.grand_total), 0) AS total_spent,
    MAX(s.sale_date) AS last_purchase_date
FROM customers c
LEFT JOIN sales s ON c.customer_id = s.customer_id
WHERE c.is_active = 1
GROUP BY c.customer_id;

-- Product Sales Performance View
CREATE VIEW v_product_sales_performance AS
SELECT 
    p.product_id,
    p.product_name,
    p.product_code,
    c.category_name,
    COUNT(DISTINCT si.sale_id) AS times_sold,
    SUM(si.quantity) AS total_quantity_sold,
    SUM(si.line_total) AS total_revenue,
    AVG(si.unit_price) AS avg_selling_price,
    p.current_stock,
    p.unit_purchase_price,
    p.unit_selling_price
FROM products p
JOIN categories c ON p.category_id = c.category_id
LEFT JOIN sale_items si ON p.product_id = si.product_id
WHERE p.is_active = 1 AND p.deleted_at IS NULL
GROUP BY p.product_id;

-- Daily Sales Summary View
CREATE VIEW v_daily_sales_summary AS
SELECT 
    DATE(sale_date) AS sale_date,
    COUNT(DISTINCT sale_id) AS total_transactions,
    SUM(subtotal) AS total_subtotal,
    SUM(discount_amount) AS total_discounts,
    SUM(tax_amount) AS total_tax,
    SUM(grand_total) AS total_sales,
    SUM(CASE WHEN payment_status = 'paid' THEN grand_total ELSE 0 END) AS paid_amount,
    SUM(CASE WHEN payment_status = 'pending' THEN grand_total ELSE 0 END) AS pending_amount
FROM sales
WHERE sale_status != 'cancelled'
GROUP BY DATE(sale_date);

-- ============================================
-- TRIGGERS FOR STOCK MANAGEMENT
-- ============================================

-- Update stock after sale
CREATE TRIGGER after_sale_item_insert
AFTER INSERT ON sale_items
FOR EACH ROW
BEGIN
    -- Update product stock
    UPDATE products 
    SET current_stock = current_stock - NEW.quantity
    WHERE product_id = NEW.product_id;
    
    -- Log stock movement
    INSERT INTO stock_movements (
        product_id, 
        movement_type, 
        quantity, 
        reference_type, 
        reference_id,
        old_stock,
        new_stock,
        created_by
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
END;

-- Update stock after purchase
CREATE TRIGGER after_purchase_item_insert
AFTER INSERT ON purchase_items
FOR EACH ROW
BEGIN
    -- Update product stock
    UPDATE products 
    SET current_stock = current_stock + NEW.quantity
    WHERE product_id = NEW.product_id;
    
    -- Log stock movement
    INSERT INTO stock_movements (
        product_id,
        movement_type,
        quantity,
        reference_type,
        reference_id,
        old_stock,
        new_stock,
        created_by
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
END;

-- Restore stock on refund
CREATE TRIGGER after_refund_item_insert
AFTER INSERT ON refund_items
FOR EACH ROW
BEGIN
    -- Get product_id from sale_item
    UPDATE products 
    SET current_stock = current_stock + NEW.quantity_returned
    WHERE product_id = (SELECT product_id FROM sale_items WHERE sale_item_id = NEW.sale_item_id);
    
    -- Log stock movement
    INSERT INTO stock_movements (
        product_id,
        movement_type,
        quantity,
        reference_type,
        reference_id,
        old_stock,
        new_stock,
        created_by
    )
    SELECT 
        si.product_id,
        'refund',
        NEW.quantity_returned,
        'refund',
        NEW.refund_id,
        p.current_stock - NEW.quantity_returned,
        p.current_stock,
        (SELECT processed_by FROM refunds WHERE refund_id = NEW.refund_id)
    FROM sale_items si
    JOIN products p ON si.product_id = p.product_id
    WHERE si.sale_item_id = NEW.sale_item_id;
END;