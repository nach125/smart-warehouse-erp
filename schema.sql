-- ====================================================================
-- SMART WAREHOUSE AND ORDER FULFILLMENT ERP SYSTEM
-- Database Schema: PostgreSQL 15+ / 16
-- Programme: E-commerce and ERP | Semester V | Session 2026-2027
-- Ramdeobaba University - CSE Core
-- Authors: Nachiket Jagdale (A7-20), Mayank Ruchandani (A7-15), Yash Jagyasi (A7-49)
-- Subject Coordinator: Prof. Kaushik R. Roy
-- ====================================================================

-- 1. USERS & ROLES
CREATE TYPE user_role_enum AS ENUM ('admin', 'staff', 'manager');

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(160) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role user_role_enum NOT NULL DEFAULT 'staff',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. WAREHOUSES & LOCATIONS (de Koster et al. 2007)
CREATE TABLE warehouses (
    id VARCHAR(32) PRIMARY KEY, -- e.g. 'WH-NAG-01'
    name VARCHAR(150) NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(80) NOT NULL,
    total_capacity_units INT NOT NULL DEFAULT 20000,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE warehouse_bins (
    id SERIAL PRIMARY KEY,
    warehouse_id VARCHAR(32) REFERENCES warehouses(id) ON DELETE CASCADE,
    zone VARCHAR(50) NOT NULL,     -- e.g. 'Zone A'
    aisle VARCHAR(50) NOT NULL,    -- e.g. 'Aisle 2'
    shelf VARCHAR(50) NOT NULL,    -- e.g. 'Tier 3'
    bin_code VARCHAR(50) NOT NULL, -- e.g. 'Bin 14'
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    UNIQUE(warehouse_id, zone, aisle, shelf, bin_code)
);

-- 3. PRODUCTS & INVENTORY
CREATE TABLE product_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(80) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    sku VARCHAR(50) UNIQUE NOT NULL, -- e.g. 'SKU-SRV-901'
    name VARCHAR(200) NOT NULL,
    category_id INT REFERENCES product_categories(id),
    unit_price NUMERIC(12, 2) NOT NULL,
    cost_price NUMERIC(12, 2) NOT NULL,
    safety_stock INT NOT NULL DEFAULT 10,
    daily_sales_rate NUMERIC(6, 2) NOT NULL DEFAULT 1.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(id) ON DELETE RESTRICT,
    warehouse_id VARCHAR(32) REFERENCES warehouses(id) ON DELETE CASCADE,
    bin_id INT REFERENCES warehouse_bins(id) ON DELETE SET NULL,
    physical_stock INT NOT NULL DEFAULT 0,
    reserved_stock INT NOT NULL DEFAULT 0, -- Locked for open orders
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_positive_stock CHECK (physical_stock >= 0),
    CONSTRAINT chk_valid_reserved CHECK (reserved_stock >= 0 AND reserved_stock <= physical_stock)
);

-- 4. SUPPLIERS & PURCHASING (PO & GRN)
CREATE TABLE suppliers (
    id VARCHAR(32) PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    contact_person VARCHAR(100),
    email VARCHAR(120),
    phone VARCHAR(30),
    lead_time_days INT NOT NULL DEFAULT 5,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TYPE po_status_enum AS ENUM ('Draft', 'Issued', 'In Transit', 'Received', 'Cancelled');

CREATE TABLE purchase_orders (
    id VARCHAR(50) PRIMARY KEY, -- e.g. 'PO-2026-081'
    supplier_id VARCHAR(32) REFERENCES suppliers(id),
    warehouse_id VARCHAR(32) REFERENCES warehouses(id),
    order_date DATE NOT NULL DEFAULT CURRENT_DATE,
    expected_delivery_date DATE,
    status po_status_enum NOT NULL DEFAULT 'Issued',
    total_amount NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    created_by INT REFERENCES users(id)
);

CREATE TABLE purchase_order_items (
    id SERIAL PRIMARY KEY,
    po_id VARCHAR(50) REFERENCES purchase_orders(id) ON DELETE CASCADE,
    product_id INT REFERENCES products(id),
    quantity_ordered INT NOT NULL,
    unit_cost NUMERIC(12, 2) NOT NULL
);

CREATE TABLE goods_receipt_notes (
    id SERIAL PRIMARY KEY,
    grn_number VARCHAR(50) UNIQUE NOT NULL, -- e.g. 'GRN-2026-0042'
    po_id VARCHAR(50) REFERENCES purchase_orders(id),
    received_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    received_by INT REFERENCES users(id),
    notes TEXT
);

-- 5. CUSTOMER ORDERS & FULFILLMENT PIPELINE
CREATE TYPE order_status_enum AS ENUM (
    'Draft',
    'Stock Reserved',
    'Picking',
    'Packing',
    'Dispatched',
    'Delivered',
    'Cancelled'
);

CREATE TABLE customer_orders (
    id VARCHAR(50) PRIMARY KEY, -- e.g. 'ORD-2026-1049'
    customer_name VARCHAR(150) NOT NULL,
    warehouse_id VARCHAR(32) REFERENCES warehouses(id),
    order_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    status order_status_enum NOT NULL DEFAULT 'Stock Reserved',
    total_amount NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    tracking_number VARCHAR(80),
    created_by INT REFERENCES users(id)
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id VARCHAR(50) REFERENCES customer_orders(id) ON DELETE CASCADE,
    product_id INT REFERENCES products(id),
    quantity INT NOT NULL,
    unit_price NUMERIC(12, 2) NOT NULL
);

-- 6. STOCK MOVEMENT AUDIT TRAIL
CREATE TABLE stock_movement_audit (
    id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(id),
    warehouse_id VARCHAR(32) REFERENCES warehouses(id),
    change_quantity INT NOT NULL,
    reference_type VARCHAR(50) NOT NULL, -- 'PO_GRN', 'ORDER_DISPATCH', 'RESERVATION'
    reference_id VARCHAR(50) NOT NULL,
    logged_by VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
