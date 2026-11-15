# Smart Warehouse & Order Fulfillment ERP System

**Programme:** E-commerce and ERP  
**Semester:** V (Session 2026–2027)  
**Department:** Computer Science & Engineering (CSE CORE)  
**Institution:** Ramdeobaba University  

### Team Members:
- **Nachiket Jagdale** (Roll No: 20, Section: A7)
- **Mayank Ruchandani** (Roll No: 15, Section: A7)
- **Yash Jagyasi** (Roll No: 49, Section: A7)
- **Subject Coordinator:** Prof. Kaushik R. Roy

---

## 1. Project Background & Synopsis Compliance

This project directly addresses the research gap identified in the academic synopsis:
- **Gu et al. (2007) & de Koster et al. (2007)** reviewed receiving, storage, zoning, batching, and routing, but noted a lack of an integrated end-to-end ERP workflow.
- **Haddara & Zach (2011)** examined ERP adoption challenges in small-to-medium enterprises.
- This system solves these issues by maintaining product, supplier, warehouse, inventory, and order records in **one unified database** and seamlessly tracking items through the fulfillment lifecycle.

---

## 2. Key Modules & Functional Features

1. **Role-Based Access Control (RBAC):**
   - Toggle between **Administrator** (full inventory, supplier, PO generation access) and **Warehouse Staff** (focused on picking, packing, and dispatch execution).
2. **Multi-Warehouse & Bin Mapping:**
   - 2D visual layout of warehouse storage across **Nagpur Central Hub (MIHAN)**, **Mumbai Bhiwandi Depot**, and **Pune Chakan Spoke**.
   - Physical hierarchy: `Warehouse -> Zone -> Aisle -> Shelf -> Bin`.
3. **Stock Checking & Real-Time Reservation:**
   - When placing a customer order, the system checks whether `physical_stock - reserved_stock >= requested_qty`.
   - On success, stock is instantly **locked into reserved status** to prevent double-allocation or race conditions.
4. **Order-to-Delivery Pipeline (Kanban & Step Wizard):**
   - Stage progression: `Stock Reserved -> Picking (Generates Aisle Pick List) -> Packing (Generates Packing Slip) -> Dispatched (Generates Tracking Manifest & Deducts Physical Stock) -> Delivered`.
5. **Purchasing & Goods Receipt Notes (GRN):**
   - Automatic and manual Purchase Order issuance to suppliers.
   - Verification of inbound goods generates a **GRN** and automatically increments warehouse physical inventory.
6. **Stock Runout Forecasting & Low-Stock Alerts:**
   - Calculates depletion runout days based on sales velocity:
     $$\text{Runout Days} = \frac{\text{Physical Stock} - \text{Reserved Stock}}{\text{Daily Sales Rate}}$$
   - Flags critical reorder points when stock falls below safety buffer levels.
7. **Complete Stock Movement Audit Ledger:**
   - Transparent audit records with timestamps and actor tracking.

---

## 3. Technology Stack

- **Frontend:** HTML5, CSS3, Modern JavaScript (ES6+), Responsive CSS Grid & Flexbox.
- **Backend API:** Python 3.10+, FastAPI, Pydantic, OAuth2/JWT tokens (`backend_api/main.py`).
- **Database:** PostgreSQL schema with referential integrity and check constraints (`schema.sql`).

---

## 4. How to Run the Project

### Option A: Launch Web ERP Frontend Instantly
Double-click or open `index.html` in any web browser (Chrome, Edge, Firefox, Safari).

### Option B: Run with Python FastAPI Backend
1. Navigate to the backend directory:
   ```bash
   cd backend_api
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the FastAPI development server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
4. Access interactive Swagger API documentation at:
   [http://localhost:8000/docs](http://localhost:8000/docs)
