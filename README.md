# POS-Database
A **Point of Sale database** with SQL schema and Python data generation for testing and development.

Entity Relationship Diagram - https://app.eraser.io/workspace/KiwSBuHQFKW3zvTylDfh

## What's Included

- **SQL Schema** — Tables for products, transactions, customers, inventory
- **Test Data** — Python scripts to generate realistic fake data at scale
- **Queries** — Sample queries for common POS operations


## Quick Start

### 1. Set Up the Database

```bash
# Create tables
sqlite3 pos.db < pos_tables.sql
sqlite3 pos.db < extra_tables.sql

# Load initial data
sqlite3 pos.db < initial_data.sql
```

### 2. Generate Fake Data

```bash
cd pos_database_with_fake_data
python main.py  # Populates database with synthetic transactions
```

### 3. Explore Queries

```bash
# View example queries for analysis
cat queries.sql
```

<img width="1818" height="936" alt="image" src="https://github.com/user-attachments/assets/fd0e56bd-2817-4b89-a5e8-80f1154e9816" />

## Schema

See the **[Entity Relationship Diagram](https://app.eraser.io/workspace/KiwSBuHQFKW3zvTylDfh)** for full data model.

**Core tables:**
- `products` — Inventory items
- `customers` — Customer profiles
- `transactions` — Sales records
- `inventory` — Stock levels

## Use Cases

- Development and testing of POS applications
- Database design exploration
- Query optimization practice
- Architectural prototyping

## License

MIT


