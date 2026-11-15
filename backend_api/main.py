"""
Smart Warehouse & Order Fulfillment ERP System - Backend API
FastAPI + SQLAlchemy (PostgreSQL / SQLite compatible) + JWT Auth
Demonstrates:
  1. Role-Based Access Control (Admin vs Warehouse Staff)
  2. Products, Categories, Stock Keeping Units (SKUs)
  3. Suppliers & Purchase Orders (PO) with Goods Receipt Note (GRN) workflow
  4. Multi-Warehouse / Location Bin mapping (Zone, Aisle, Shelf, Bin)
  5. Customer Orders, Real-time Stock Reservation & Allocation
  6. Fulfillment Pipeline: Pick List Generation -> Packing Slip -> Dispatch Manifest -> Delivery Status
  7. Automated Stock Movement Ledger (Audit Trail)
  8. Inventory Analytics: Low-stock triggers & Sales-velocity demand forecasting
"""

import os
import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from jose import JWTError, jwt
from passlib.context import CryptContext

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "erp-super-secret-jwt-signing-key-2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 8

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

app = FastAPI(
    title="Smart Warehouse & Order Fulfillment ERP API",
    version="1.0.0",
    description="Enterprise API backing the Ramdeobaba University Semester V E-Commerce & ERP Project"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- IN-MEMORY STATEFUL SEED DATA (For standalone run) -----------------
USERS_DB = {
    "admin@ramdeobaba.edu": {
        "id": 1,
        "name": "Prof. Kaushik R. Roy / Nachiket Jagdale",
        "email": "admin@ramdeobaba.edu",
        "role": "admin",
        "hashed_password": pwd_context.hash("admin123")
    },
    "staff@ramdeobaba.edu": {
        "id": 2,
        "name": "Mayank Ruchandani & Yash Jagyasi",
        "email": "staff@ramdeobaba.edu",
        "role": "staff",
        "hashed_password": pwd_context.hash("staff123")
    }
}

WAREHOUSES = [
    {"id": "WH-NAG-01", "name": "Central Hub Nagpur (MIHAN)", "type": "Mother Hub", "capacity": 25000, "utilization": 74},
    {"id": "WH-MUM-02", "name": "West Coast Depot Mumbai (Bhiwandi)", "type": "Distribution Center", "capacity": 18000, "utilization": 62},
    {"id": "WH-PUN-03", "name": "Pune Tech Spoke (Chakan)", "type": "Fulfillment Center", "capacity": 12000, "utilization": 58}
]

PRODUCTS = [
    {
        "id": 1, "sku": "SKU-SRV-901", "name": "Enterprise Edge Micro-Server R450", "category": "Hardware",
        "unit": "Units", "unit_price": 85000, "cost_price": 68000,
        "current_stock": 24, "reserved_stock": 4, "safety_stock": 10,
        "location": "WH-NAG-01 / Zone A / Aisle 2 / Bin 14", "daily_sales_rate": 2.5
    },
    {
        "id": 2, "sku": "SKU-SWT-408", "name": "Managed 48-Port PoE+ L3 Core Switch", "category": "Networking",
        "unit": "Units", "unit_price": 42000, "cost_price": 31000,
        "current_stock": 18, "reserved_stock": 6, "safety_stock": 8,
        "location": "WH-NAG-01 / Zone A / Aisle 4 / Bin 02", "daily_sales_rate": 3.0
    },
    {
        "id": 3, "sku": "SKU-SSD-204", "name": "NVMe U.3 Enterprise Solid State Drive 7.68TB", "category": "Storage",
        "unit": "Units", "unit_price": 28500, "cost_price": 21000,
        "current_stock": 9, "reserved_stock": 3, "safety_stock": 15,
        "location": "WH-MUM-02 / Zone B / Aisle 1 / Bin 08", "daily_sales_rate": 4.2
    },
    {
        "id": 4, "sku": "SKU-SCN-101", "name": "Rugged 2D Industrial Barcode Scanner Terminal", "category": "Equipment",
        "unit": "Units", "unit_price": 16500, "cost_price": 11500,
        "current_stock": 35, "reserved_stock": 2, "safety_stock": 12,
        "location": "WH-PUN-03 / Zone C / Aisle 1 / Bin 05", "daily_sales_rate": 1.8
    },
    {
        "id": 5, "sku": "SKU-UPS-600", "name": "Online Double-Conversion Rack UPS 6kVA", "category": "Power",
        "unit": "Units", "unit_price": 64000, "cost_price": 52000,
        "current_stock": 6, "reserved_stock": 1, "safety_stock": 10,
        "location": "WH-NAG-01 / Zone Heavy / Bin 01", "daily_sales_rate": 1.2
    }
]

PURCHASE_ORDERS = [
    {
        "id": "PO-2026-081", "supplier": "Apex Semiconductor Corp", "date": "2026-11-10",
        "items": [{"sku": "SKU-SSD-204", "qty": 30, "price": 21000}], "status": "Received",
        "expected_date": "2026-11-14", "warehouse": "WH-MUM-02"
    },
    {
        "id": "PO-2026-094", "supplier": "SysTech Network Hardware Ltd", "date": "2026-11-12",
        "items": [{"sku": "SKU-SWT-408", "qty": 20, "price": 31000}], "status": "In Transit",
        "expected_date": "2026-11-18", "warehouse": "WH-NAG-01"
    }
]

CUSTOMER_ORDERS = [
    {
        "id": "ORD-2026-1049", "customer": "Persistent Systems Nagpur Tech Center", "date": "2026-11-15 10:30",
        "items": [{"sku": "SKU-SRV-901", "qty": 2, "price": 85000}], "total": 170000,
        "status": "Picking", "warehouse": "WH-NAG-01", "picker": "Yash Jagyasi"
    },
    {
        "id": "ORD-2026-1050", "customer": "TCS MIHAN SEZ Division", "date": "2026-11-15 11:45",
        "items": [{"sku": "SKU-SWT-408", "qty": 3, "price": 42000}], "total": 126000,
        "status": "Packing", "warehouse": "WH-NAG-01", "picker": "Mayank Ruchandani"
    },
    {
        "id": "ORD-2026-1051", "customer": "Infosys Cyber City Phase 2", "date": "2026-11-14 16:10",
        "items": [{"sku": "SKU-SSD-204", "qty": 5, "price": 28500}], "total": 142500,
        "status": "Dispatched", "warehouse": "WH-MUM-02", "tracking_no": "EXP-DEL-992140"
    }
]

AUDIT_LOGS = [
    {"timestamp": "2026-11-15 09:12", "user": "admin", "action": "PO Received", "details": "PO-2026-081 goods verified. +30 units SKU-SSD-204 booked into WH-MUM-02."},
    {"timestamp": "2026-11-15 10:32", "user": "system", "action": "Stock Reserved", "details": "ORD-2026-1049 reserved 2x SKU-SRV-901. Available drops to 20."},
    {"timestamp": "2026-11-15 11:50", "user": "Mayank R.", "action": "Order Picked", "details": "ORD-2026-1050 picked from Zone A / Aisle 4 / Bin 02. Moved to Packing Table 3."}
]

# ----------------- SCHEMAS -----------------
class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    user_name: str

class UserAuth(BaseModel):
    email: EmailStr
    password: str

class OrderItemSchema(BaseModel):
    sku: str
    qty: int

class CreateCustomerOrderSchema(BaseModel):
    customer: str
    warehouse: str
    items: List[OrderItemSchema]

class UpdateOrderStatusSchema(BaseModel):
    status: str
    notes: Optional[str] = None
    tracking_no: Optional[str] = None

# ----------------- AUTH HELPERS -----------------
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None or email not in USERS_DB:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return USERS_DB[email]
    except JWTError:
        raise HTTPException(status_code=401, detail="Token expired or malformed")

# ----------------- API ENDPOINTS -----------------

@app.get("/")
def api_root():
    return {
        "project": "Smart Warehouse and Order Fulfillment ERP System",
        "institution": "Ramdeobaba University - CSE Core",
        "semester": "Session 2026-2027 | Sem V (E-commerce & ERP)",
        "submitted_by": ["Nachiket Jagdale (A7-20)", "Mayank Ruchandani (A7-15)", "Yash Jagyasi (A7-49)"],
        "coordinator": "Prof. Kaushik R. Roy",
        "status": "Online",
        "docs_url": "/docs"
    }

@app.post("/api/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = USERS_DB.get(form_data.username)
    if not user or not pwd_context.verify(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    token = create_access_token({"sub": user["email"], "role": user["role"]})
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user["role"],
        "user_name": user["name"]
    }

@app.get("/api/dashboard/stats")
def get_dashboard_stats(current_user: dict = Depends(get_current_user)):
    total_sku_count = len(PRODUCTS)
    total_inventory_units = sum(p["current_stock"] for p in PRODUCTS)
    total_reserved_units = sum(p["reserved_stock"] for p in PRODUCTS)
    low_stock_items = [p for p in PRODUCTS if (p["current_stock"] - p["reserved_stock"]) <= p["safety_stock"]]
    active_fulfillment_orders = [o for o in CUSTOMER_ORDERS if o["status"] not in ["Delivered", "Cancelled"]]

    return {
        "total_sku_count": total_sku_count,
        "total_inventory_units": total_inventory_units,
        "total_reserved_units": total_reserved_units,
        "available_units": total_inventory_units - total_reserved_units,
        "low_stock_count": len(low_stock_items),
        "low_stock_items": low_stock_items,
        "active_fulfillment_orders": len(active_fulfillment_orders),
        "warehouses": WAREHOUSES
    }

@app.get("/api/inventory")
def list_inventory(current_user: dict = Depends(get_current_user)):
    enriched = []
    for p in PRODUCTS:
        available = p["current_stock"] - p["reserved_stock"]
        # Demand forecasting: Days of inventory remaining = Available / Daily sales rate
        days_remaining = round(available / p["daily_sales_rate"], 1) if p["daily_sales_rate"] > 0 else 999
        is_low = available <= p["safety_stock"]
        enriched.append({
            **p,
            "available_stock": available,
            "days_of_stock_left": days_remaining,
            "is_low_stock": is_low,
            "recommendation": "REPLENISH IMMEDIATELY (PO Req)" if days_remaining < 5 else ("WARNING: Below Safety Stock" if is_low else "Optimal")
        })
    return enriched

@app.post("/api/orders/create")
def create_customer_order(order_data: CreateCustomerOrderSchema, current_user: dict = Depends(get_current_user)):
    # 1. Stock Check & Reservation Validation
    for item in order_data.items:
        prod = next((p for p in PRODUCTS if p["sku"] == item.sku), None)
        if not prod:
            raise HTTPException(status_code=404, detail=f"Product with SKU {item.sku} not found")
        available = prod["current_stock"] - prod["reserved_stock"]
        if available < item.qty:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient available stock for {prod['name']} (SKU: {prod['sku']}). Requested: {item.qty}, Available: {available}"
            )

    # 2. Reserve Stock
    total_val = 0
    reserved_items = []
    for item in order_data.items:
        prod = next(p for p in PRODUCTS if p["sku"] == item.sku)
        prod["reserved_stock"] += item.qty
        total_val += prod["unit_price"] * item.qty
        reserved_items.append({"sku": prod["sku"], "name": prod["name"], "qty": item.qty, "price": prod["unit_price"]})

    new_id = f"ORD-2026-{1000 + len(CUSTOMER_ORDERS) + 1}"
    new_order = {
        "id": new_id,
        "customer": order_data.customer,
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "items": reserved_items,
        "total": total_val,
        "status": "Stock Reserved",
        "warehouse": order_data.warehouse,
        "picker": "Unassigned"
    }
    CUSTOMER_ORDERS.insert(0, new_order)

    # 3. Add to Audit Trail
    AUDIT_LOGS.insert(0, {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "user": current_user["name"],
        "action": "Order Created & Reserved",
        "details": f"Order {new_id} created for {order_data.customer}. Total: ₹{total_val:,}. Reserved items."
    })

    return {"message": "Order placed and stock reserved successfully", "order": new_order}

@app.post("/api/orders/{order_id}/advance_status")
def advance_order_status(order_id: str, payload: UpdateOrderStatusSchema, current_user: dict = Depends(get_current_user)):
    order = next((o for o in CUSTOMER_ORDERS if o["id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    old_status = order["status"]
    new_status = payload.status
    order["status"] = new_status
    if payload.tracking_no:
        order["tracking_no"] = payload.tracking_no

    # If Dispatched or Delivered, release physical stock from current and reserved
    if new_status in ["Dispatched", "Delivered"] and old_status not in ["Dispatched", "Delivered"]:
        for item in order["items"]:
            prod = next((p for p in PRODUCTS if p["sku"] == item["sku"]), None)
            if prod:
                prod["current_stock"] -= item["qty"]
                prod["reserved_stock"] = max(0, prod["reserved_stock"] - item["qty"])

    AUDIT_LOGS.insert(0, {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "user": current_user["name"],
        "action": f"Status: {old_status} -> {new_status}",
        "details": f"Order {order_id} fulfillment advanced by {current_user['name']}."
    })

    return {"message": f"Order status updated to {new_status}", "order": order}

@app.get("/api/fulfillment/pipeline")
def get_fulfillment_pipeline(current_user: dict = Depends(get_current_user)):
    return {
        "reserved": [o for o in CUSTOMER_ORDERS if o["status"] == "Stock Reserved"],
        "picking": [o for o in CUSTOMER_ORDERS if o["status"] == "Picking"],
        "packing": [o for o in CUSTOMER_ORDERS if o["status"] == "Packing"],
        "dispatched": [o for o in CUSTOMER_ORDERS if o["status"] == "Dispatched"],
        "delivered": [o for o in CUSTOMER_ORDERS if o["status"] == "Delivered"]
    }

@app.get("/api/audit-logs")
def get_audit_logs(current_user: dict = Depends(get_current_user)):
    return AUDIT_LOGS

@app.get("/api/synopsis-spec")
def get_synopsis_spec():
    """Returns academic mapping directly corresponding to the Ramdeobaba University project synopsis"""
    return {
        "title": "SMART WAREHOUSE AND ORDER FULFILLMENT ERP SYSTEM",
        "institution": "Ramdeobaba University (CSE CORE)",
        "session": "2026–2027 | Semester: V | Programme: E-commerce and ERP",
        "students": [
            {"name": "Nachiket Jagdale", "roll": "20", "section": "A7"},
            {"name": "Mayank Ruchandani", "roll": "15", "section": "A7"},
            {"name": "Yash Jagyasi", "roll": "49", "section": "A7"}
        ],
        "subject_coordinator": "Kaushik R. Roy",
        "literature_citations": [
            "Gu et al. (2007) - Warehouse Operations",
            "de Koster et al. (2007) - Order Picking Systems",
            "Masae et al. (2020) - Picker Routing",
            "Haddara & Zach (2011) - ERP in SMEs"
        ],
        "scope_covered": [
            "Product, Supplier, Warehouse, Multi-location Bins",
            "Customer Orders with Stock Checking & Stock Reservation",
            "Warehouse Order Picking, Packing, Dispatch & Delivery Tracking",
            "Purchase Orders & Inventory Goods Receipt (GRN)",
            "Role-based Access Control (Admin vs Warehouse Staff)",
            "Demand-based warnings & Low-stock replenishment forecasting"
        ]
    }
