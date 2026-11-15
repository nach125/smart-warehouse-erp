"""
Smart Warehouse & Order Fulfillment ERP System
Enterprise Cloud & Localhost Streamlit Application
"""

import streamlit as st
import pandas as pd
import datetime

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="Smart Warehouse ERP Platform",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- CUSTOM CSS -----------------
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
        padding: 20px 24px;
        border-radius: 10px;
        color: white;
        border: 1px solid #334155;
        margin-bottom: 20px;
    }
    .cred-box {
        background-color: #0f172a;
        padding: 14px 18px;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
        font-family: monospace;
        font-size: 13px;
        color: #93c5fd;
        margin-bottom: 18px;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- CREDENTIALS STORE -----------------
USERS_DATABASE = {
    "admin": {
        "password": "admin123",
        "name": "System Administrator",
        "role": "Administrator",
        "badge": "SUPERUSER"
    },
    "staff": {
        "password": "staff123",
        "name": "Warehouse Operations Staff",
        "role": "Staff",
        "badge": "OPERATOR"
    }
}

# ----------------- SESSION STATE SEEDING -----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None

if "products" not in st.session_state:
    st.session_state.products = [
        {"id": 1, "sku": "SKU-SRV-901", "name": "Enterprise Edge Micro-Server R450", "category": "Hardware", "unit_price": 85000, "cost_price": 68000, "current_stock": 24, "reserved_stock": 4, "safety_stock": 10, "warehouse": "Central Hub (MIHAN)", "location": "Zone A / A2 / B14", "daily_sales": 2.5},
        {"id": 2, "sku": "SKU-SWT-408", "name": "Managed 48-Port PoE+ L3 Core Switch", "category": "Networking", "unit_price": 42000, "cost_price": 31000, "current_stock": 18, "reserved_stock": 6, "safety_stock": 8, "warehouse": "Central Hub (MIHAN)", "location": "Zone A / A4 / B02", "daily_sales": 3.0},
        {"id": 3, "sku": "SKU-SSD-204", "name": "NVMe U.3 Enterprise SSD 7.68TB", "category": "Storage", "unit_price": 28500, "cost_price": 21000, "current_stock": 9, "reserved_stock": 3, "safety_stock": 15, "warehouse": "West Coast Depot", "location": "Zone B / A1 / B08", "daily_sales": 4.2},
        {"id": 4, "sku": "SKU-SCN-101", "name": "Rugged 2D Barcode Scanner Terminal", "category": "Equipment", "unit_price": 16500, "cost_price": 11500, "current_stock": 35, "reserved_stock": 2, "safety_stock": 12, "warehouse": "Pune Logistics Spoke", "location": "Zone C / A1 / B05", "daily_sales": 1.8},
        {"id": 5, "sku": "SKU-UPS-600", "name": "Online Double-Conversion Rack UPS 6kVA", "category": "Power", "unit_price": 64000, "cost_price": 52000, "current_stock": 6, "reserved_stock": 1, "safety_stock": 10, "warehouse": "Central Hub (MIHAN)", "location": "Zone Heavy / Pallet 01", "daily_sales": 1.2},
        {"id": 6, "sku": "SKU-RAM-128", "name": "128GB DDR5 ECC Registered Server Memory Kit", "category": "Storage", "unit_price": 48000, "cost_price": 38000, "current_stock": 40, "reserved_stock": 5, "safety_stock": 14, "warehouse": "Central Hub (MIHAN)", "location": "Zone A / A1 / B09", "daily_sales": 3.5}
    ]

if "orders" not in st.session_state:
    st.session_state.orders = [
        {"id": "ORD-2026-1049", "customer": "Persistent Systems Enterprise Center", "sku": "SKU-SRV-901", "qty": 2, "total": 170000, "status": "Picking", "warehouse": "Central Hub (MIHAN)", "tracking": "TRK-PENDING"},
        {"id": "ORD-2026-1050", "customer": "Tata Consultancy Services SEZ", "sku": "SKU-SWT-408", "qty": 3, "total": 126000, "status": "Packing", "warehouse": "Central Hub (MIHAN)", "tracking": "TRK-PENDING"},
        {"id": "ORD-2026-1051", "customer": "Infosys Cyber City Campus", "sku": "SKU-SSD-204", "qty": 5, "total": 142500, "status": "Dispatched", "warehouse": "West Coast Depot", "tracking": "EXP-DEL-992140"},
        {"id": "ORD-2026-1052", "customer": "Wipro Technologies Circle", "sku": "SKU-SCN-101", "qty": 4, "total": 66000, "status": "Delivered", "warehouse": "Pune Logistics Spoke", "tracking": "BLUE-DART-554109"}
    ]

if "purchase_orders" not in st.session_state:
    st.session_state.purchase_orders = [
        {"id": "PO-2026-081", "supplier": "Apex Semiconductor Corp", "sku": "SKU-SSD-204", "qty": 30, "total": 630000, "status": "Received", "grn": "GRN-2026-0042", "warehouse": "West Coast Depot"},
        {"id": "PO-2026-094", "supplier": "SysTech Network Hardware Ltd", "sku": "SKU-SWT-408", "qty": 20, "total": 620000, "status": "In Transit", "grn": "Pending Receipt", "warehouse": "Central Hub (MIHAN)"}
    ]

if "audit_logs" not in st.session_state:
    st.session_state.audit_logs = [
        {"timestamp": "2026-11-15 09:12", "user": "Admin User", "action": "PO Received", "details": "GRN-2026-0042 processed. +30 units SKU-SSD-204 booked into West Coast Depot."},
        {"timestamp": "2026-11-15 10:32", "user": "System (Auto-Reserve)", "action": "Stock Reserved", "details": "ORD-2026-1049 locked 2x SKU-SRV-901 in Central Hub."},
        {"timestamp": "2026-11-15 11:50", "user": "Staff Operator", "action": "Order Picked", "details": "ORD-2026-1050 picked from Zone A / Aisle 4. Moved to packing table."}
    ]

# ================= LOGIN INTERFACE =================
if not st.session_state.logged_in:
    col_center = st.columns([1, 2, 1])[1]
    with col_center:
        st.markdown("""
        <div style="text-align: center; margin-top: 40px; margin-bottom: 24px;">
            <div style="font-size: 48px;">📦</div>
            <h1 style="margin: 0; font-size: 28px;">Smart Warehouse ERP</h1>
            <p style="color: #94a3b8; font-size: 14px;">Enterprise Order Fulfillment & Inventory Control System</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="cred-box">
            <strong>🔑 Demo Login Credentials:</strong><br/>
            • <b>Administrator:</b> Username: <code>admin</code> | Password: <code>admin123</code><br/>
            • <b>Staff Operator:</b> Username: <code>staff</code> | Password: <code>staff123</code>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            username_input = st.text_input("Username", placeholder="e.g. admin or staff").strip().lower()
            password_input = st.text_input("Password", type="password", placeholder="Enter your password")
            submit_login = st.form_submit_button("Sign In to Portal", type="primary", use_container_width=True)

            if submit_login:
                if username_input in USERS_DATABASE and USERS_DATABASE[username_input]["password"] == password_input:
                    st.session_state.logged_in = True
                    st.session_state.current_user = USERS_DATABASE[username_input]
                    st.session_state.username = username_input
                    st.success(f"Welcome back, {USERS_DATABASE[username_input]['name']}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password. Please use the credentials shown above.")
        
        st.stop()

# ================= AUTHENTICATED DASHBOARD =================

# Sidebar: User Profile & Navigation
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/warehouse-outloading.png", width=56)
    st.markdown(f"### {st.session_state.current_user['name']}")
    st.caption(f"Role: **{st.session_state.current_user['role']}** • `{st.session_state.current_user['badge']}`")

    if st.button("🚪 Log Out", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()

    st.divider()
    nav = st.radio("Navigation Menu:", [
        "📊 Dashboard & Warehouse Layout",
        "📦 Inventory & Stock Checking",
        "⚡ Order Fulfillment Pipeline",
        "🛒 Purchasing & Goods Receipt (GRN)",
        "📜 Stock Movement Audit Trail"
    ])

is_admin = (st.session_state.current_user["role"] == "Administrator")

# Main Page Banner
st.markdown(f"""
<div class="main-header">
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <div>
            <h2 style="margin:0; font-size:24px;">Smart Warehouse & Order Fulfillment ERP</h2>
            <p style="margin:4px 0 0; color:#94a3b8; font-size:14px;">Multi-Warehouse Management • Real-Time Stock Reservation • Stage-Gate Fulfillment</p>
        </div>
        <div style="text-align:right;">
            <span style="background:#2563eb; padding:6px 14px; border-radius:6px; font-weight:700; font-size:12px;">{st.session_state.current_user['role'].upper()} ACTIVE</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------- VIEW 1: DASHBOARD & WAREHOUSE BINS -----------------
if nav == "📊 Dashboard & Warehouse Layout":
    st.subheader("Warehouse Operations Overview")
    
    total_physical = sum(p["current_stock"] for p in st.session_state.products)
    total_reserved = sum(p["reserved_stock"] for p in st.session_state.products)
    free_available = total_physical - total_reserved
    low_stock_count = sum(1 for p in st.session_state.products if (p["current_stock"] - p["reserved_stock"]) <= p["safety_stock"])
    active_orders = sum(1 for o in st.session_state.orders if o["status"] != "Delivered")

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Active SKUs", len(st.session_state.products), "3 Facilities")
    c2.metric("Free Stock", f"{free_available:,} Units", "Ready for Allocation")
    c3.metric("Reserved Stock", f"{total_reserved:,} Units", "Locked in Pipeline")
    c4.metric("Active Orders", active_orders, "In Fulfillment")
    c5.metric("Low Stock Alerts", low_stock_count, "Safety Buffer", delta_color="inverse")

    st.divider()

    st.subheader("Physical Warehouse Layout & Storage Bins")
    st.caption("Zone matrix, aisle routing, and storage slot utilization")

    b1, b2, b3, b4 = st.columns(4)
    with b1:
        st.info("**Zone A — Server & Switching**\nAisle 1 - 4 • High Security\n- Bin 02: Core Switch (12 Free)\n- Bin 09: DDR5 RAM (35 Free)\n- Bin 14: Micro-Servers (20 Free)")
    with b2:
        st.warning("**Zone B — Solid State Storage**\nAisle 1 - 2 • Static-Safe\n- Bin 08: NVMe SSD (6 Free ⚠️)\n- Bin 12: Empty Slot Available\n- Bin 16: Empty Slot Available")
    with b3:
        st.success("**Zone C — Mobile Hardware**\nAisle 1 - 3 • High Velocity\n- Bin 05: Barcode Scanners (33 Free)\n- Bin 10: Empty Slot Available\n- Bin 11: Empty Slot Available")
    with b4:
        st.error("**Zone Heavy — Power & UPS**\nFloor Bays • Pallet Racks\n- Pallet 01: Rack UPS (5 Free ⚠️)\n- Pallet 02: Empty Bay Available\n- Pallet 03: Empty Bay Available")

# ----------------- VIEW 2: INVENTORY & STOCK CHECKING -----------------
elif nav == "📦 Inventory & Stock Checking":
    st.subheader("Inventory Stock Master & Sales-Velocity Runout Forecasting")

    df_inv = []
    for p in st.session_state.products:
        avail = p["current_stock"] - p["reserved_stock"]
        runout_days = round(avail / p["daily_sales"], 1) if p["daily_sales"] > 0 else 999
        status = "CRITICAL REORDER" if runout_days < 5 else ("WARNING: Safety Stock Trigger" if avail <= p["safety_stock"] else "Optimal")
        df_inv.append({
            "SKU": p["sku"],
            "Product Name": p["name"],
            "Category": p["category"],
            "Location / Bin": p["location"],
            "Unit Price (₹)": f"₹{p['unit_price']:,}",
            "Physical Stock": p["current_stock"],
            "Reserved Stock": p["reserved_stock"],
            "Free Available": avail,
            "Runout Est.": f"{runout_days} days",
            "Health Status": status
        })

    st.dataframe(pd.DataFrame(df_inv), use_container_width=True)

    st.divider()
    st.subheader("Create Customer Order (With Stock Checking & Real-Time Stock Reservation)")
    
    with st.form("new_order_form"):
        col_c, col_wh = st.columns(2)
        cust_name = col_c.text_input("Customer Name", value="Enterprise Procurement Dept")
        wh_select = col_wh.selectbox("Fulfillment Facility", ["Central Hub (MIHAN)", "West Coast Depot", "Pune Logistics Spoke"])

        prod_options = {f"{p['name']} ({p['sku']}) - Available: {p['current_stock'] - p['reserved_stock']}": p for p in st.session_state.products}
        selected_label = st.selectbox("Select Product", list(prod_options.keys()))
        selected_prod = prod_options[selected_label]

        order_qty = st.number_input("Order Quantity", min_value=1, max_value=50, value=2)
        submitted = st.form_submit_button("Check Stock & Reserve Order", type="primary")

        if submitted:
            free_avail = selected_prod["current_stock"] - selected_prod["reserved_stock"]
            if order_qty > free_avail:
                st.error(f"❌ Stock Check Failed! Requested {order_qty} units, but only {free_avail} are available for reservation.")
            else:
                selected_prod["reserved_stock"] += order_qty
                order_id = f"ORD-2026-{1050 + len(st.session_state.orders) + 1}"
                total_val = order_qty * selected_prod["unit_price"]

                st.session_state.orders.insert(0, {
                    "id": order_id,
                    "customer": cust_name,
                    "sku": selected_prod["sku"],
                    "qty": order_qty,
                    "total": total_val,
                    "status": "Stock Reserved",
                    "warehouse": wh_select,
                    "tracking": "TRK-PENDING"
                })

                st.session_state.audit_logs.insert(0, {
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "user": st.session_state.current_user["name"],
                    "action": "Stock Reserved",
                    "details": f"Order {order_id} created for {cust_name}. Reserved {order_qty}x {selected_prod['sku']}. Available drops to {selected_prod['current_stock'] - selected_prod['reserved_stock']}."
                })
                st.success(f"✓ Stock Reserved Successfully! Order {order_id} has locked {order_qty} unit(s) into the fulfillment pipeline.")
                st.rerun()

# ----------------- VIEW 3: ORDER FULFILLMENT PIPELINE -----------------
elif nav == "⚡ Order Fulfillment Pipeline":
    st.subheader("Stage-Gate Order Fulfillment Pipeline")
    st.caption("Workflow: Stock Reserved ➔ Picking (Aisle Pick List) ➔ Packing (Slip) ➔ Dispatched (Physical Stock Deduction) ➔ Delivered")

    stages = ["Stock Reserved", "Picking", "Packing", "Dispatched", "Delivered"]
    cols = st.columns(5)

    for i, stage in enumerate(stages):
        with cols[i]:
            orders_in_stage = [o for o in st.session_state.orders if o["status"] == stage]
            st.markdown(f"### {stage} ({len(orders_in_stage)})")
            
            for o in orders_in_stage:
                with st.expander(f"{o['id']} - ₹{o['total']:,}"):
                    st.write(f"**Customer:** {o['customer']}")
                    st.write(f"**Item:** {o['qty']}x {o['sku']}")
                    st.write(f"**Warehouse:** {o['warehouse']}")
                    if o["tracking"] != "TRK-PENDING":
                        st.write(f"**Tracking:** `{o['tracking']}`")

                    if stage == "Stock Reserved":
                        if st.button("Generate Pick List", key=f"btn_{o['id']}"):
                            o["status"] = "Picking"
                            st.rerun()
                    elif stage == "Picking":
                        if st.button("Complete Pick ➔ Pack", key=f"btn_{o['id']}"):
                            o["status"] = "Packing"
                            st.rerun()
                    elif stage == "Packing":
                        if st.button("Dispatch Package", key=f"btn_{o['id']}"):
                            o["status"] = "Dispatched"
                            o["tracking"] = f"EXP-DEL-{datetime.datetime.now().strftime('%S%M%H')}"
                            for p in st.session_state.products:
                                if p["sku"] == o["sku"]:
                                    p["current_stock"] -= o["qty"]
                                    p["reserved_stock"] = max(0, p["reserved_stock"] - o["qty"])
                            st.session_state.audit_logs.insert(0, {
                                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "user": st.session_state.current_user["name"],
                                "action": "Order Dispatched",
                                "details": f"Physical stock deducted for {o['id']}. Tracking {o['tracking']} created."
                            })
                            st.rerun()
                    elif stage == "Dispatched":
                        if st.button("Mark Delivered", key=f"btn_{o['id']}"):
                            o["status"] = "Delivered"
                            st.rerun()

# ----------------- VIEW 4: PURCHASING & GRN -----------------
elif nav == "🛒 Purchasing & Goods Receipt (GRN)":
    st.subheader("Purchase Orders & Goods Receipt Notes (GRN)")

    po_data = []
    for po in st.session_state.purchase_orders:
        po_data.append({
            "PO Number": po["id"],
            "Supplier": po["supplier"],
            "Item SKU": po["sku"],
            "Quantity": po["qty"],
            "Total (₹)": f"₹{po['total']:,}",
            "Destination Hub": po["warehouse"],
            "Status": po["status"],
            "GRN Number": po["grn"]
        })

    st.dataframe(pd.DataFrame(po_data), use_container_width=True)

    st.divider()
    col_grn, col_new_po = st.columns(2)

    with col_grn:
        st.subheader("Process Goods Receipt Note (GRN)")
        transit_pos = [po for po in st.session_state.purchase_orders if po["status"] == "In Transit"]
        if not transit_pos:
            st.info("No purchase orders currently in transit.")
        else:
            po_to_receive = st.selectbox("Select PO to Receive", [po["id"] for po in transit_pos])
            if st.button("Receive Goods & Credit Inventory", type="primary"):
                target_po = next(p for p in st.session_state.purchase_orders if p["id"] == po_to_receive)
                target_po["status"] = "Received"
                grn_no = f"GRN-2026-00{datetime.datetime.now().strftime('%M%S')}"
                target_po["grn"] = grn_no

                for p in st.session_state.products:
                    if p["sku"] == target_po["sku"]:
                        p["current_stock"] += target_po["qty"]

                st.session_state.audit_logs.insert(0, {
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "user": st.session_state.current_user["name"],
                    "action": "GRN Processed",
                    "details": f"{grn_no} generated for {target_po['id']}. +{target_po['qty']}x {target_po['sku']} added to stock."
                })
                st.success(f"✓ {grn_no} generated! Stock has been credited to {target_po['warehouse']}.")
                st.rerun()

    with col_new_po:
        st.subheader("Raise New Purchase Order")
        if not is_admin:
            st.warning("🔒 Only Administrator accounts have permission to issue new Purchase Orders to suppliers.")
        else:
            with st.form("raise_po_form"):
                supp_name = st.selectbox("Supplier", ["Apex Semiconductor Corp", "SysTech Network Hardware Ltd", "VoltMaster Power Solutions"])
                po_sku = st.selectbox("Product SKU", [p["sku"] for p in st.session_state.products])
                po_qty = st.number_input("Quantity to Order", min_value=5, max_value=200, value=20)
                po_wh = st.selectbox("Destination Warehouse", ["Central Hub (MIHAN)", "West Coast Depot", "Pune Logistics Spoke"])
                
                if st.form_submit_button("Transmit PO to Supplier"):
                    matched_prod = next(p for p in st.session_state.products if p["sku"] == po_sku)
                    new_po_id = f"PO-2026-{100 + len(st.session_state.purchase_orders) + 1}"
                    total_cost = po_qty * matched_prod["cost_price"]

                    st.session_state.purchase_orders.insert(0, {
                        "id": new_po_id,
                        "supplier": supp_name,
                        "sku": po_sku,
                        "qty": po_qty,
                        "total": total_cost,
                        "status": "In Transit",
                        "grn": "Pending Receipt",
                        "warehouse": po_wh
                    })
                    st.success(f"✓ Purchase Order {new_po_id} issued to {supp_name} for ₹{total_cost:,}!")
                    st.rerun()

# ----------------- VIEW 5: AUDIT TRAIL -----------------
elif nav == "📜 Stock Movement Audit Trail":
    st.subheader("Tamper-Evident Stock Movement Audit Trail")
    st.dataframe(pd.DataFrame(st.session_state.audit_logs), use_container_width=True)
