"""
Smart Warehouse & Order Fulfillment ERP Platform
Enterprise Cloud & Localhost Streamlit Application
"""

import streamlit as st
import pandas as pd
import datetime

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="OmniLogix | Enterprise Warehouse ERP",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- MODERN ENTERPRISE DESIGN CSS -----------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, sans-serif;
    }

    .main-header {
        background: linear-gradient(135deg, #090d16 0%, #172554 50%, #090d16 100%);
        padding: 24px 28px;
        border-radius: 12px;
        color: white;
        border: 1px solid #1e293b;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
        margin-bottom: 24px;
    }
    
    .cred-box {
        background-color: #0b1120;
        padding: 16px 20px;
        border-radius: 8px;
        border: 1px solid #1e293b;
        border-left: 5px solid #3b82f6;
        font-family: 'JetBrains Mono', monospace;
        font-size: 13px;
        color: #93c5fd;
        margin-bottom: 20px;
        line-height: 1.7;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- CREDENTIALS STORE -----------------
USERS_DATABASE = {
    "admin": {
        "password": "admin123",
        "name": "Global Operations Director",
        "role": "Administrator",
        "badge": "ENTERPRISE PRIVILEGES"
    },
    "staff": {
        "password": "staff123",
        "name": "Fulfillment Center Lead",
        "role": "Staff",
        "badge": "DISPATCH OPS"
    }
}

# ----------------- SESSION STATE SEEDING -----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None

if "products" not in st.session_state:
    st.session_state.products = [
        {
            "id": 1, "sku": "SKU-HPC-9400", "name": "Dell PowerEdge R760 High-Compute Rack Server (Dual Xeon Platinum, 512GB ECC)",
            "category": "Enterprise Compute", "unit_price": 485000, "cost_price": 395000,
            "current_stock": 22, "reserved_stock": 4, "safety_stock": 8,
            "warehouse": "Nagpur Regional Fulfillment Hub (MIHAN Logistics Corridor)",
            "location": "Aisle 02 / Bay C / Tier 04", "daily_sales": 1.5
        },
        {
            "id": 2, "sku": "SKU-NET-8848", "name": "Cisco Catalyst 9300 Series 48-Port Multi-Gigabit PoE+ Core Switch",
            "category": "Carrier-Grade Networking", "unit_price": 182000, "cost_price": 142000,
            "current_stock": 30, "reserved_stock": 6, "safety_stock": 10,
            "warehouse": "Nagpur Regional Fulfillment Hub (MIHAN Logistics Corridor)",
            "location": "Aisle 04 / Bay A / Tier 02", "daily_sales": 2.2
        },
        {
            "id": 3, "sku": "SKU-SSD-7680", "name": "Micron 9400 PRO Enterprise U.3 NVMe PCIe 4.0 7.68TB Solid State Drive",
            "category": "High-Throughput Storage", "unit_price": 54000, "cost_price": 41000,
            "current_stock": 11, "reserved_stock": 3, "safety_stock": 15,
            "warehouse": "Mumbai Port Distribution Gateway (Bhiwandi Hub)",
            "location": "Aisle 01 / Bay D / Tier 03", "daily_sales": 3.8
        },
        {
            "id": 4, "sku": "SKU-BAR-9900", "name": "Zebra TC58 Enterprise Rugged Mobile Industrial Barcode Terminal",
            "category": "Logistics Hardware", "unit_price": 38500, "cost_price": 27500,
            "current_stock": 45, "reserved_stock": 5, "safety_stock": 14,
            "warehouse": "Pune Technology Logistics Park (Chakan MIDC)",
            "location": "Aisle 01 / Bay B / Tier 01", "daily_sales": 2.8
        },
        {
            "id": 5, "sku": "SKU-UPS-10KV", "name": "Schneider Electric APC Smart-UPS On-Line 10kVA Rackmount Power System",
            "category": "Critical Power Infrastructure", "unit_price": 215000, "cost_price": 175000,
            "current_stock": 7, "reserved_stock": 2, "safety_stock": 8,
            "warehouse": "Nagpur Regional Fulfillment Hub (MIHAN Logistics Corridor)",
            "location": "Heavy Bay 01 / Ground Pallet", "daily_sales": 1.1
        },
        {
            "id": 6, "sku": "SKU-ECC-256G", "name": "Samsung Enterprise 256GB DDR5 Quad-Rank Registered ECC Server Memory Module",
            "category": "High-Throughput Storage", "unit_price": 89000, "cost_price": 71000,
            "current_stock": 55, "reserved_stock": 8, "safety_stock": 16,
            "warehouse": "Nagpur Regional Fulfillment Hub (MIHAN Logistics Corridor)",
            "location": "Aisle 03 / Bay A / Tier 05", "daily_sales": 4.5
        }
    ]

if "orders" not in st.session_state:
    st.session_state.orders = [
        {
            "id": "SO-2026-9041", "customer": "Persistent Systems Global Delivery Center",
            "sku": "SKU-HPC-9400", "qty": 2, "total": 970000, "status": "Picking",
            "warehouse": "Nagpur Regional Fulfillment Hub (MIHAN Logistics Corridor)",
            "tracking": "TRK-PENDING", "created_at": "2026-11-15 10:30"
        },
        {
            "id": "SO-2026-9042", "customer": "Tata Consultancy Services (TCS) Cloud Infrastructure Division",
            "sku": "SKU-NET-8848", "qty": 3, "total": 546000, "status": "Packing",
            "warehouse": "Nagpur Regional Fulfillment Hub (MIHAN Logistics Corridor)",
            "tracking": "TRK-PENDING", "created_at": "2026-11-15 11:45"
        },
        {
            "id": "SO-2026-9043", "customer": "Infosys Data Center Operations Group",
            "sku": "SKU-SSD-7680", "qty": 5, "total": 270000, "status": "Dispatched",
            "warehouse": "Mumbai Port Distribution Gateway (Bhiwandi Hub)",
            "tracking": "DHL-EXP-940214", "created_at": "2026-11-14 16:10"
        },
        {
            "id": "SO-2026-9044", "customer": "HCL Technologies Enterprise Networks Unit",
            "sku": "SKU-BAR-9900", "qty": 4, "total": 154000, "status": "Delivered",
            "warehouse": "Pune Technology Logistics Park (Chakan MIDC)",
            "tracking": "BLUEDART-EXP-88120", "created_at": "2026-11-13 09:20"
        }
    ]

if "purchase_orders" not in st.session_state:
    st.session_state.purchase_orders = [
        {
            "id": "PO-2026-081", "supplier": "Micron Semiconductor Industrial Solutions",
            "sku": "SKU-SSD-7680", "qty": 35, "total": 1435000, "status": "Received",
            "grn": "GRN-2026-0042", "warehouse": "Mumbai Port Distribution Gateway (Bhiwandi Hub)",
            "date": "2026-11-10"
        },
        {
            "id": "PO-2026-094", "supplier": "Cisco Systems Direct OEM Wholesale",
            "sku": "SKU-NET-8848", "qty": 20, "total": 2840000, "status": "In Transit",
            "grn": "Pending Inbound Inspection", "warehouse": "Nagpur Regional Fulfillment Hub (MIHAN Logistics Corridor)",
            "date": "2026-11-12"
        }
    ]

if "audit_logs" not in st.session_state:
    st.session_state.audit_logs = [
        {"timestamp": "2026-11-15 09:12", "user": "Global Operations Director", "action": "Inbound Verification & GRN", "details": "GRN-2026-0042 verified. +35 units SKU-SSD-7680 received into Mumbai Port Gateway."},
        {"timestamp": "2026-11-15 10:32", "user": "Real-Time Allocation Engine", "action": "Stock Reserved", "details": "SO-2026-9041 allocated 2x SKU-HPC-9400 for Persistent Systems Global Center."},
        {"timestamp": "2026-11-15 11:50", "user": "Fulfillment Center Lead", "action": "Pick Completed", "details": "SO-2026-9042 successfully picked from Aisle 04 / Bay A. Routed to Packing Station 02."}
    ]

# ================= LOGIN INTERFACE =================
if not st.session_state.logged_in:
    col_center = st.columns([1, 2, 1])[1]
    with col_center:
        st.markdown("""
        <div style="text-align: center; margin-top: 35px; margin-bottom: 24px;">
            <div style="font-size: 52px; margin-bottom: 8px;">🏢</div>
            <h1 style="margin: 0; font-size: 30px; font-weight: 800; letter-spacing: -0.5px;">OmniLogix ERP</h1>
            <p style="color: #94a3b8; font-size: 14px; margin-top: 6px;">Enterprise Warehouse Management & Multi-Facility Fulfillment Platform</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="cred-box">
            <strong style="color: #60a5fa; font-size: 14px;">🔑 Portal Access Credentials:</strong><br/>
            <div style="margin-top: 8px;">
                • <b>Administrator:</b> Username: <code style="color:#f8fafc">admin</code> | Password: <code style="color:#f8fafc">admin123</code><br/>
                • <b>Operations Lead:</b> Username: <code style="color:#f8fafc">staff</code> | Password: <code style="color:#f8fafc">staff123</code>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<p style='font-size:12px; color:#94a3b8; font-weight:600; margin-bottom:8px;'>⚡ 1-CLICK DEMO ACCESS:</p>", unsafe_allow_html=True)
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🚀 Sign In as Administrator", use_container_width=True):
                st.session_state.logged_in = True
                st.session_state.current_user = USERS_DATABASE["admin"]
                st.session_state.username = "admin"
                st.rerun()
        with col_btn2:
            if st.button("👷 Sign In as Operations Lead", use_container_width=True):
                st.session_state.logged_in = True
                st.session_state.current_user = USERS_DATABASE["staff"]
                st.session_state.username = "staff"
                st.rerun()

        st.markdown("<div style='margin: 18px 0; border-top: 1px solid #334155; text-align: center;'><span style='position: relative; top: -10px; background: #0b0f19; padding: 0 10px; color: #64748b; font-size: 11px;'>OR ENTER CREDENTIALS MANUALLY</span></div>", unsafe_allow_html=True)

        with st.form("manual_login_form"):
            username_input = st.text_input("Enterprise ID / Username", placeholder="e.g. admin or staff").strip().lower()
            password_input = st.text_input("Password", type="password", placeholder="Enter secure password")
            submit_login = st.form_submit_button("Sign In to ERP Portal", type="primary", use_container_width=True)

            if submit_login:
                if username_input in USERS_DATABASE and USERS_DATABASE[username_input]["password"] == password_input:
                    st.session_state.logged_in = True
                    st.session_state.current_user = USERS_DATABASE[username_input]
                    st.session_state.username = username_input
                    st.success(f"Access Authorized: {USERS_DATABASE[username_input]['name']}")
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please click the 1-Click Demo buttons above or check username and password.")
        
        st.stop()

# ================= AUTHENTICATED PORTAL =================

with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/warehouse-outloading.png", width=52)
    st.markdown(f"### {st.session_state.current_user['name']}")
    st.caption(f"Role: **{st.session_state.current_user['role']}** • `{st.session_state.current_user['badge']}`")

    if st.button("🚪 Sign Out", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()

    st.divider()
    nav = st.radio("Enterprise Navigation:", [
        "📊 Operations Command Center",
        "📦 Stock Master & Real-Time Allocation",
        "⚡ Order Fulfillment Pipeline",
        "🛒 Procurement & Goods Receipt (GRN)",
        "📜 System Audit Trail"
    ])

is_admin = (st.session_state.current_user["role"] == "Administrator")

# Main Header Banner
st.markdown(f"""
<div class="main-header">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
        <div>
            <h2 style="margin:0; font-size:24px; font-weight:800; letter-spacing:-0.5px;">OmniLogix Warehouse &amp; Fulfillment Platform</h2>
            <p style="margin:4px 0 0; color:#94a3b8; font-size:13px;">Enterprise Distribution Logistics • Dynamic Stock Locking • Precision Picking Protocols</p>
        </div>
        <div style="display:flex; align-items:center; gap:10px;">
            <span style="background:rgba(59, 130, 246, 0.2); border: 1px solid rgba(59, 130, 246, 0.4); color: #93c5fd; padding:6px 14px; border-radius:6px; font-weight:700; font-size:12px;">
                SESSION: {st.session_state.current_user['role'].upper()}
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------- VIEW 1: DASHBOARD & WAREHOUSE BINS -----------------
if nav == "📊 Operations Command Center":
    st.subheader("Global Logistics & Fulfillment Telemetry")
    
    total_physical = sum(p["current_stock"] for p in st.session_state.products)
    total_reserved = sum(p["reserved_stock"] for p in st.session_state.products)
    free_available = total_physical - total_reserved
    low_stock_count = sum(1 for p in st.session_state.products if (p["current_stock"] - p["reserved_stock"]) <= p["safety_stock"])
    active_orders = sum(1 for o in st.session_state.orders if o["status"] != "Delivered")

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Active Catalog SKUs", len(st.session_state.products), "3 Facilities")
    c2.metric("Available Free Stock", f"{free_available:,} Units", "Ready for Allocation")
    c3.metric("Allocated / Reserved", f"{total_reserved:,} Units", "Locked in Pipeline")
    c4.metric("Active Sales Orders", active_orders, "In Fulfillment")
    c5.metric("Replenishment Alerts", low_stock_count, "Safety Buffer Breach", delta_color="inverse")

    st.divider()

    st.subheader("Physical Logistics Layout & Tiered Storage Bins")
    st.caption("Distribution topology, high-density zoning, and aisle storage coordinates across strategic distribution nodes")

    b1, b2, b3, b4 = st.columns(4)
    with b1:
        st.info("**Zone A — High-Performance Compute & Switching**\nAisles 01 - 04 • High Security\n- Bay C / Tier 04: PowerEdge R760 (18 Free)\n- Bay A / Tier 02: Catalyst 9300 Switches (24 Free)\n- Bay A / Tier 05: Samsung DDR5 ECC Modules (47 Free)")
    with b2:
        st.warning("**Zone B — Solid-State Enterprise Storage**\nAisles 01 - 02 • Static-Dissipative\n- Bay D / Tier 03: Micron NVMe 7.68TB (8 Free ⚠️)\n- Bay B / Tier 02: Unallocated Slot\n- Bay B / Tier 04: Unallocated Slot")
    with b3:
        st.success("**Zone C — Logistics & Mobile Terminals**\nAisles 01 - 03 • Fast-Pick Bins\n- Bay B / Tier 01: Zebra TC58 Barcode Scanners (40 Free)\n- Bay C / Tier 02: Unallocated Slot\n- Bay C / Tier 03: Unallocated Slot")
    with b4:
        st.error("**Heavy Pallet Staging — Critical Power Backup**\nGround Bays • High-Load Structural Racks\n- Pallet 01: Schneider APC 10kVA UPS (5 Free ⚠️)\n- Pallet 02: Empty Staging Bay\n- Pallet 03: Empty Staging Bay")

# ----------------- VIEW 2: INVENTORY & STOCK CHECKING -----------------
elif nav == "📦 Stock Master & Real-Time Allocation":
    st.subheader("Global Inventory Ledger & Sales-Velocity Runout Forecasting")

    f_col1, f_col2 = st.columns([2, 1])
    search_q = f_col1.text_input("🔍 Search Inventory by SKU, Specification, or Warehouse Bay", "").lower()
    selected_wh = f_col2.selectbox("Filter Distribution Facility", [
        "All Regional Hubs",
        "Nagpur Regional Fulfillment Hub (MIHAN Logistics Corridor)",
        "Mumbai Port Distribution Gateway (Bhiwandi Hub)",
        "Pune Technology Logistics Park (Chakan MIDC)"
    ])

    df_inv = []
    for p in st.session_state.products:
        if search_q and not (search_q in p["name"].lower() or search_q in p["sku"].lower() or search_q in p["location"].lower()):
            continue
        if selected_wh != "All Regional Hubs" and p["warehouse"] != selected_wh:
            continue

        avail = p["current_stock"] - p["reserved_stock"]
        runout_days = round(avail / p["daily_sales"], 1) if p["daily_sales"] > 0 else 999
        status = "CRITICAL REORDER" if runout_days < 5 else ("WARNING: Safety Stock Trigger" if avail <= p["safety_stock"] else "Optimal")
        
        df_inv.append({
            "SKU": p["sku"],
            "Item Specification & Model": p["name"],
            "Category": p["category"],
            "Facility & Storage Bay": f"{p['warehouse'].split('(')[0].strip()} • {p['location']}",
            "Unit List Price (₹)": f"₹{p['unit_price']:,}",
            "On-Hand": p["current_stock"],
            "Allocated": p["reserved_stock"],
            "Free Stock": avail,
            "Runout Est.": f"{runout_days} days",
            "Inventory Health": status
        })

    st.dataframe(pd.DataFrame(df_inv), use_container_width=True)

    if df_inv:
        csv_data = pd.DataFrame(df_inv).to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export Global Stock Ledger (CSV)", data=csv_data, file_name="omnilogix_inventory_ledger.csv", mime="text/csv")

    st.divider()
    st.subheader("Create Customer Sales Order (With Stock Checking & Real-Time Stock Reservation)")
    
    with st.form("new_order_form"):
        col_c, col_wh = st.columns(2)
        cust_name = col_c.selectbox("Select Enterprise Client", [
            "Persistent Systems Global Delivery Center",
            "Tata Consultancy Services (TCS) Cloud Infrastructure Division",
            "Infosys Data Center Operations Group",
            "Wipro Technologies Enterprise Networks Unit",
            "LTIMindtree Digital Infrastructure Group",
            "Tech Mahindra Cloud & Compute Services"
        ])
        wh_select = col_wh.selectbox("Fulfillment Facility", [
            "Nagpur Regional Fulfillment Hub (MIHAN Logistics Corridor)",
            "Mumbai Port Distribution Gateway (Bhiwandi Hub)",
            "Pune Technology Logistics Park (Chakan MIDC)"
        ])

        prod_options = {f"{p['name']} ({p['sku']}) - Available: {p['current_stock'] - p['reserved_stock']}": p for p in st.session_state.products}
        selected_label = st.selectbox("Product Line Item", list(prod_options.keys()))
        selected_prod = prod_options[selected_label]

        order_qty = st.number_input("Order Quantity (Units)", min_value=1, max_value=50, value=2)
        submitted = st.form_submit_button("Verify Stock & Lock Allocation", type="primary")

        if submitted:
            free_avail = selected_prod["current_stock"] - selected_prod["reserved_stock"]
            if order_qty > free_avail:
                st.error(f"❌ Allocation Denied: Requested {order_qty} units, but only {free_avail} are currently unallocated.")
            else:
                selected_prod["reserved_stock"] += order_qty
                order_id = f"SO-2026-{9040 + len(st.session_state.orders) + 1}"
                total_val = order_qty * selected_prod["unit_price"]

                st.session_state.orders.insert(0, {
                    "id": order_id,
                    "customer": cust_name,
                    "sku": selected_prod["sku"],
                    "qty": order_qty,
                    "total": total_val,
                    "status": "Stock Reserved",
                    "warehouse": wh_select,
                    "tracking": "TRK-PENDING",
                    "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                })

                st.session_state.audit_logs.insert(0, {
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "user": st.session_state.current_user["name"],
                    "action": "Stock Reserved",
                    "details": f"Sales Order {order_id} generated for {cust_name}. Reserved {order_qty}x {selected_prod['sku']}. Available unreserved balance: {selected_prod['current_stock'] - selected_prod['reserved_stock']}."
                })
                st.success(f"✓ Inventory Locked: Sales Order {order_id} confirmed. {order_qty} units assigned to fulfillment staging.")
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
                    st.write(f"**Client:** {o['customer']}")
                    st.write(f"**Item:** {o['qty']}x {o['sku']}")
                    st.write(f"**Facility:** {o['warehouse'].split('(')[0]}")
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
                            o["tracking"] = f"DHL-EXP-{datetime.datetime.now().strftime('%S%M%H')}"
                            for p in st.session_state.products:
                                if p["sku"] == o["sku"]:
                                    p["current_stock"] -= o["qty"]
                                    p["reserved_stock"] = max(0, p["reserved_stock"] - o["qty"])
                            st.session_state.audit_logs.insert(0, {
                                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "user": st.session_state.current_user["name"],
                                "action": "Order Dispatched",
                                "details": f"Physical inventory deducted for {o['id']}. Waybill {o['tracking']} generated."
                            })
                            st.rerun()
                    elif stage == "Dispatched":
                        if st.button("Confirm Delivery", key=f"btn_{o['id']}"):
                            o["status"] = "Delivered"
                            st.rerun()

# ----------------- VIEW 4: PURCHASING & GRN -----------------
elif nav == "🛒 Procurement & Goods Receipt (GRN)":
    st.subheader("Inbound Supplier Purchase Orders & Goods Receipt Notes (GRN)")

    po_data = []
    for po in st.session_state.purchase_orders:
        po_data.append({
            "PO Reference": po["id"],
            "OEM / Supplier": po["supplier"],
            "Product SKU": po["sku"],
            "Quantity": po["qty"],
            "Total Value (₹)": f"₹{po['total']:,}",
            "Destination Hub": po["warehouse"].split('(')[0],
            "PO Status": po["status"],
            "GRN Inspection": po["grn"]
        })

    st.dataframe(pd.DataFrame(po_data), use_container_width=True)

    st.divider()
    col_grn, col_new_po = st.columns(2)

    with col_grn:
        st.subheader("Process Goods Receipt Note (GRN)")
        transit_pos = [po for po in st.session_state.purchase_orders if po["status"] == "In Transit"]
        if not transit_pos:
            st.info("All issued purchase orders have been verified and received.")
        else:
            po_to_receive = st.selectbox("Select Pending Shipment to Verify", [po["id"] for po in transit_pos])
            if st.button("Verify Inbound Shipment & Credit Inventory", type="primary"):
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
                    "details": f"{grn_no} confirmed for {target_po['id']}. +{target_po['qty']}x {target_po['sku']} credited to {target_po['warehouse']}."
                })
                st.success(f"✓ Inbound Shipment Verified: {grn_no} logged. Inventory ledger updated.")
                st.rerun()

    with col_new_po:
        st.subheader("Issue Inbound OEM Purchase Order")
        if not is_admin:
            st.warning("🔒 Restricted Action: Procurement PO issuance requires Global Administrator privileges.")
        else:
            with st.form("raise_po_form"):
                supp_name = st.selectbox("Authorized OEM Supplier", [
                    "Dell Technologies Direct Enterprise Supply",
                    "Cisco Systems Direct OEM Wholesale",
                    "Micron Semiconductor Industrial Solutions",
                    "Schneider Electric APC OEM Distribution",
                    "Samsung Semiconductor Solutions Global",
                    "Zebra Technologies Enterprise Supply"
                ])
                po_sku = st.selectbox("Product Line Item SKU", [p["sku"] for p in st.session_state.products])
                po_qty = st.number_input("Replenishment Volume (Units)", min_value=5, max_value=200, value=25)
                po_wh = st.selectbox("Consignee Hub", [
                    "Nagpur Regional Fulfillment Hub (MIHAN Logistics Corridor)",
                    "Mumbai Port Distribution Gateway (Bhiwandi Hub)",
                    "Pune Technology Logistics Park (Chakan MIDC)"
                ])
                
                if st.form_submit_button("Transmit Purchase Order"):
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
                        "grn": "Pending Inbound Inspection",
                        "warehouse": po_wh,
                        "date": datetime.datetime.now().strftime("%Y-%m-%d")
                    })
                    st.success(f"✓ Purchase Order {new_po_id} transmitted to {supp_name} for ₹{total_cost:,}!")
                    st.rerun()

# ----------------- VIEW 5: AUDIT TRAIL -----------------
elif nav == "📜 System Audit Trail":
    st.subheader("Enterprise Stock Movement & Custody Ledger")
    st.dataframe(pd.DataFrame(st.session_state.audit_logs), use_container_width=True)
