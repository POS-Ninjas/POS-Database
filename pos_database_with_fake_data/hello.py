from db import *
from db_context import DatabaseContext
import sqlite3
from pathlib import Path

"""
TODO 

- have functions that populate the database for each table in the DB
- make it performant..add async io 
- have corresponding crud functions for each of the table 
- test the functions
- test the indexes of the database tables
"""

DB_PATH = Path('/home/test/Desktop/pos/POS-Database') / 'test.db'

def read_data():
    
    with sqlite3.connect(DB_PATH) as connection:
        # create_data_for_users(connection)
        # delete_users_data(connection)
        # print(read_users_data(connection))
        pass

    with DatabaseContext() as db:
        user_repo           = UserRepository(db)
        roles_repo          = RoleRepository(db)
        client_repo         = ClientRepository(db)
        category_repo       = CategoryRepository(db)
        supplier_repo       = SupplierRepository(db)
        product_repo        = ProductRepository(db)
        sale_repo           = SaleRepository(db)
        sale_item_repo      = SaleItemRepository(db)
        purchase_repo       = PurchaseRepository(db)
        purchase_items_repo = PurchaseItemsRepository(db)
        payment_repo        = PaymentRepository(db)
        audit_log_repo      = AuditLogRepository(db)
        report_repo         = ReportRepository(db)

        roles_repo.insert_roles()
        user_repo.populate_user_table_with_fake_data()
        category_repo.populate_category_table_with_fake_data()
        supplier_repo.populate_suppliers_table_with_fake_data()
        client_repo.populate_client_table_with_fake_data()
        product_repo.populate_products_table_with_fake_data()
        sale_repo.populate_sales_table_with_fake_data()
        sale_item_repo.populate_sale_items_table_with_fake_data()
        purchase_repo.populate_purchases_table_with_fake_data()
        purchase_items_repo.populate_purchase_items_table_with_fake_data()
        payment_repo.populate_payments_table_with_fake_data()
        audit_log_repo.populate_audit_logs_table_with_fake_data()
        report_repo.populate_reports_table_with_fake_data()

def main():
    print("Hello from pos-database-with-fake-data!")

    read_data()

if __name__ == "__main__":
    main()