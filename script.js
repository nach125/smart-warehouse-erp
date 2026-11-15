/**
 * Smart Warehouse & Order Fulfillment ERP System
 * Academic Implementation for Ramdeobaba University - CSE Core
 * Session: 2026-2027 | Sem V | Programme: E-commerce and ERP
 * Developed by:
 *   Nachiket Jagdale (A7-20)
 *   Mayank Ruchandani (A7-15)
 *   Yash Jagyasi (A7-49)
 * Subject Coordinator: Prof. Kaushik R. Roy
 */

'use strict';

// ================= GLOBAL STATE =================
const ERP_STATE = {
  currentUser: {
    name: 'Nachiket Jagdale (A7-20)',
    role: 'admin', // 'admin' or 'staff'
    email: 'admin@ramdeobaba.edu'
  },
  activeTab: 'dashboard',
  warehouses: [
    { id: 'WH-NAG-01', name: 'Central Hub Nagpur (MIHAN)', location: 'MIHAN SEZ, Nagpur', capacity: 25000, current: 18500 },
    { id: 'WH-MUM-02', name: 'West Coast Depot Mumbai', location: 'Bhiwandi Logistics Park', capacity: 18000, current: 11160 },
    { id: 'WH-PUN-03', name: 'Pune Tech Spoke', location: 'Chakan MIDC Phase 2', capacity: 12000, current: 6960 }
  ],
  products: [
    {
      id: 1, sku: 'SKU-SRV-901', name: 'Enterprise Edge Micro-Server R450', category: 'Hardware',
      unit_price: 85000, cost_price: 68000, current_stock: 24, reserved_stock: 4, safety_stock: 10,
      warehouse: 'WH-NAG-01', zone: 'Zone A', aisle: 'Aisle 2', bin: 'Bin 14', daily_sales: 2.5
    },
    {
      id: 2, sku: 'SKU-SWT-408', name: 'Managed 48-Port PoE+ L3 Core Switch', category: 'Networking',
      unit_price: 42000, cost_price: 31000, current_stock: 18, reserved_stock: 6, safety_stock: 8,
      warehouse: 'WH-NAG-01', zone: 'Zone A', aisle: 'Aisle 4', bin: 'Bin 02', daily_sales: 3.0
    },
    {
      id: 3, sku: 'SKU-SSD-204', name: 'NVMe U.3 Enterprise SSD 7.68TB', category: 'Storage',
      unit_price: 28500, cost_price: 21000, current_stock: 9, reserved_stock: 3, safety_stock: 15,
      warehouse: 'WH-MUM-02', zone: 'Zone B', aisle: 'Aisle 1', bin: 'Bin 08', daily_sales: 4.2
    },
    {
      id: 4, sku: 'SKU-SCN-101', name: 'Rugged 2D Industrial Barcode Scanner Terminal', category: 'Equipment',
      unit_price: 16500, cost_price: 11500, current_stock: 35, reserved_stock: 2, safety_stock: 12,
      warehouse: 'WH-PUN-03', zone: 'Zone C', aisle: 'Aisle 1', bin: 'Bin 05', daily_sales: 1.8
    },
    {
      id: 5, sku: 'SKU-UPS-600', name: 'Online Double-Conversion Rack UPS 6kVA', category: 'Power',
      unit_price: 64000, cost_price: 52000, current_stock: 6, reserved_stock: 1, safety_stock: 10,
      warehouse: 'WH-NAG-01', zone: 'Zone Heavy', aisle: 'Floor 1', bin: 'Pallet 01', daily_sales: 1.2
    },
    {
      id: 6, sku: 'SKU-RAM-128', name: '128GB DDR5 ECC Registered Server Memory Kit', category: 'Storage',
      unit_price: 48000, cost_price: 38000, current_stock: 40, reserved_stock: 5, safety_stock: 14,
      warehouse: 'WH-NAG-01', zone: 'Zone A', aisle: 'Aisle 1', bin: 'Bin 09', daily_sales: 3.5
    }
  ],
  suppliers: [
    { id: 'SUP-01', name: 'Apex Semiconductor Corp', contact: 'Kailash Joshi', email: 'sales@apexsemi.com', phone: '+91 98230 44102', lead_days: 4, rating: 4.9 },
    { id: 'SUP-02', name: 'SysTech Network Hardware Ltd', contact: 'Rohit Deshmukh', email: 'orders@systech-in.com', phone: '+91 98901 22340', lead_days: 6, rating: 4.7 },
    { id: 'SUP-03', name: 'VoltMaster Power Solutions', contact: 'Sunil Kulkarni', email: 'b2b@voltmaster.in', phone: '+91 97645 88901', lead_days: 5, rating: 4.8 }
  ],
  purchaseOrders: [
    {
      id: 'PO-2026-081', supplierId: 'SUP-01', supplierName: 'Apex Semiconductor Corp',
      date: '2026-11-10', expectedDate: '2026-11-14', warehouse: 'WH-MUM-02',
      status: 'Received', items: [{ sku: 'SKU-SSD-204', name: 'NVMe U.3 Enterprise SSD 7.68TB', qty: 30, unitCost: 21000 }],
      total: 630000, grnNumber: 'GRN-2026-0042'
    },
    {
      id: 'PO-2026-094', supplierId: 'SUP-02', supplierName: 'SysTech Network Hardware Ltd',
      date: '2026-11-12', expectedDate: '2026-11-18', warehouse: 'WH-NAG-01',
      status: 'In Transit', items: [{ sku: 'SKU-SWT-408', name: 'Managed 48-Port PoE+ L3 Core Switch', qty: 20, unitCost: 31000 }],
      total: 620000, grnNumber: null
    }
  ],
  orders: [
    {
      id: 'ORD-2026-1049', customer: 'Persistent Systems Tech Center Nagpur',
      date: '2026-11-15 10:30', warehouse: 'WH-NAG-01', status: 'Picking',
      items: [{ sku: 'SKU-SRV-901', name: 'Enterprise Edge Micro-Server R450', qty: 2, price: 85000, bin: 'Zone A / A2 / B14' }],
      total: 170000, picker: 'Yash Jagyasi', trackingNo: null
    },
    {
      id: 'ORD-2026-1050', customer: 'TCS MIHAN SEZ Division',
      date: '2026-11-15 11:45', warehouse: 'WH-NAG-01', status: 'Packing',
      items: [{ sku: 'SKU-SWT-408', name: 'Managed 48-Port PoE+ L3 Core Switch', qty: 3, price: 42000, bin: 'Zone A / A4 / B02' }],
      total: 126000, picker: 'Mayank Ruchandani', trackingNo: null
    },
    {
      id: 'ORD-2026-1051', customer: 'Infosys Hinjewadi Phase 2',
      date: '2026-11-14 16:10', warehouse: 'WH-MUM-02', status: 'Dispatched',
      items: [{ sku: 'SKU-SSD-204', name: 'NVMe U.3 Enterprise SSD 7.68TB', qty: 5, price: 28500, bin: 'Zone B / A1 / B08' }],
      total: 142500, picker: 'Warehouse Robot Dispatch', trackingNo: 'EXP-DEL-992140'
    },
    {
      id: 'ORD-2026-1052', customer: 'Wipro Technologies Pune Circle',
      date: '2026-11-13 09:20', warehouse: 'WH-PUN-03', status: 'Delivered',
      items: [{ sku: 'SKU-SCN-101', name: 'Rugged 2D Barcode Scanner Terminal', qty: 4, price: 16500, bin: 'Zone C / A1 / B05' }],
      total: 66000, picker: 'Ramesh Patil', trackingNo: 'BLUE-DART-554109'
    }
  ],
  auditLogs: [
    { timestamp: '2026-11-15 09:12', user: 'Nachiket Jagdale', action: 'PO Goods Received', details: 'GRN-2026-0042 signed. +30 units SKU-SSD-204 received from Apex Semi.' },
    { timestamp: '2026-11-15 10:32', user: 'System (Auto-Reserve)', action: 'Stock Reserved', details: 'ORD-2026-1049 locked 2x SKU-SRV-901 in WH-NAG-01. Available: 20.' },
    { timestamp: '2026-11-15 11:50', user: 'Mayank Ruchandani', action: 'Pick Completed', details: 'ORD-2026-1050 picked from Zone A/Aisle 4. Moved to Packing station.' }
  ]
};

// ================= FORMATTERS & HELPERS =================
function fmtCurrency(val) {
  return '₹' + Math.round(val).toLocaleString('en-IN');
}

function showToast(message, type = 'success') {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `<strong>${type.toUpperCase()}:</strong> ${message}`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

function logAudit(action, details) {
  const now = new Date();
  const timeStr = now.toISOString().slice(0, 16).replace('T', ' ');
  ERP_STATE.auditLogs.unshift({
    timestamp: timeStr,
    user: ERP_STATE.currentUser.name,
    action: action,
    details: details
  });
  renderAuditLogs();
}

// ================= ROLE SWITCHER =================
function switchRole(role) {
  ERP_STATE.currentUser.role = role;
  if (role === 'admin') {
    ERP_STATE.currentUser.name = 'Nachiket Jagdale (A7-20)';
    ERP_STATE.currentUser.email = 'admin@ramdeobaba.edu';
  } else {
    ERP_STATE.currentUser.name = 'Mayank Ruchandani & Yash Jagyasi';
    ERP_STATE.currentUser.email = 'staff@ramdeobaba.edu';
  }
  document.getElementById('current-user-role').textContent = role.toUpperCase();
  document.getElementById('current-user-name').textContent = ERP_STATE.currentUser.name;
  document.getElementById('user-avatar').textContent = role === 'admin' ? 'NJ' : 'WS';
  
  // Show/Hide role specific elements
  const adminOnlyEls = document.querySelectorAll('.admin-only');
  adminOnlyEls.forEach(el => {
    el.style.display = role === 'admin' ? '' : 'none';
  });

  showToast(`Switched active session to ${role.toUpperCase()} (${ERP_STATE.currentUser.name})`, 'warning');
  renderAllViews();
}

// ================= TAB NAVIGATION =================
function switchTab(tabId) {
  ERP_STATE.activeTab = tabId;
  document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.tab-view').forEach(v => v.style.display = 'none');

  const tabBtn = document.getElementById(`tab-btn-${tabId}`);
  if (tabBtn) tabBtn.classList.add('active');

  const view = document.getElementById(`view-${tabId}`);
  if (view) view.style.display = 'block';

  renderAllViews();
}

// ================= RENDER FUNCTIONS =================

function renderDashboardKPIs() {
  const totalSKUs = ERP_STATE.products.length;
  const totalPhysical = ERP_STATE.products.reduce((acc, p) => acc + p.current_stock, 0);
  const totalReserved = ERP_STATE.products.reduce((acc, p) => acc + p.reserved_stock, 0);
  const availableStock = totalPhysical - totalReserved;
  const lowStockCount = ERP_STATE.products.filter(p => (p.current_stock - p.reserved_stock) <= p.safety_stock).length;
  const activeOrders = ERP_STATE.orders.filter(o => o.status !== 'Delivered').length;

  document.getElementById('kpi-total-skus').textContent = totalSKUs;
  document.getElementById('kpi-available-units').textContent = availableStock.toLocaleString();
  document.getElementById('kpi-reserved-units').textContent = totalReserved.toLocaleString();
  document.getElementById('kpi-low-stock-count').textContent = lowStockCount;
  document.getElementById('kpi-active-orders').textContent = activeOrders;
}

function renderWarehouseRacks() {
  const container = document.getElementById('rack-zones-container');
  if (!container) return;

  const zones = [
    { name: 'Zone A - High Density Servers & Core Switching', aisle: 'Aisle 1 - 4', bins: ['B01', 'B02', 'B09', 'B14'] },
    { name: 'Zone B - High Speed Solid State Storage', aisle: 'Aisle 1 - 2', bins: ['B04', 'B08', 'B12', 'B16'] },
    { name: 'Zone C - Mobile Terminals & Industrial Hardware', aisle: 'Aisle 1 - 3', bins: ['B02', 'B05', 'B10', 'B11'] },
    { name: 'Zone Heavy - Power Distribution & Battery Backup', aisle: 'Floor Bays', bins: ['P01', 'P02', 'P03', 'P04'] }
  ];

  container.innerHTML = zones.map(z => `
    <div class="rack-zone-card">
      <div class="zone-title">
        <span>${z.name}</span>
        <span class="badge badge-purple">${z.aisle}</span>
      </div>
      <div class="bin-slots">
        ${z.bins.map(b => {
          const match = ERP_STATE.products.find(p => p.bin.includes(b.replace('P01','Pallet 01')));
          if (match) {
            const avail = match.current_stock - match.reserved_stock;
            const isLow = avail <= match.safety_stock;
            return `<div class="bin-cell ${isLow ? 'low-stock' : 'occupied'}" title="${match.name} (SKU: ${match.sku}) | Stock: ${avail} avail">
              <div><strong>${b}</strong></div>
              <div style="font-size:10px">${match.sku.split('-')[1]} (${avail})</div>
            </div>`;
          }
          return `<div class="bin-cell" title="Empty storage slot available">
            <div>${b}</div>
            <div style="font-size:10px;color:var(--text-muted)">Empty</div>
          </div>`;
        }).join('')}
      </div>
    </div>
  `).join('');
}

function renderInventoryTable() {
  const tbody = document.getElementById('inventory-table-body');
  if (!tbody) return;

  tbody.innerHTML = ERP_STATE.products.map(p => {
    const available = p.current_stock - p.reserved_stock;
    const isLow = available <= p.safety_stock;
    const daysLeft = p.daily_sales > 0 ? (available / p.daily_sales).toFixed(1) : '99';
    const isCritical = daysLeft < 5;

    return `
      <tr>
        <td>
          <strong style="color:#fff">${p.name}</strong><br/>
          <span class="mono" style="font-size:11px;color:var(--text-muted)">${p.sku} • ${p.category}</span>
        </td>
        <td>
          <span class="badge badge-blue">${p.warehouse}</span><br/>
          <span style="font-size:11px;color:var(--text-muted)">${p.zone} / ${p.aisle} / ${p.bin}</span>
        </td>
        <td><strong style="color:#fff">${fmtCurrency(p.unit_price)}</strong></td>
        <td><span class="mono">${p.current_stock}</span></td>
        <td><span class="badge badge-orange mono">${p.reserved_stock}</span></td>
        <td>
          <strong class="mono" style="color:${isLow ? 'var(--danger)' : 'var(--success)'}; font-size:14px">
            ${available}
          </strong>
        </td>
        <td>
          <div style="font-size:12px; font-weight:600; color:${isCritical ? 'var(--danger)' : (isLow ? 'var(--warning)' : 'var(--success)')}">
            ${daysLeft} days
          </div>
          <span style="font-size:10px; color:var(--text-muted)">Velocity: ${p.daily_sales}/day</span>
        </td>
        <td>
          ${isCritical ? '<span class="badge badge-red">CRITICAL REORDER</span>' : 
            (isLow ? '<span class="badge badge-orange">SAFETY STOCK TRIGGER</span>' : 
            '<span class="badge badge-green">OPTIMAL</span>')}
        </td>
        <td>
          <button class="btn btn-outline btn-sm admin-only" onclick="openReorderModal(${p.id})">
            + Raise PO
          </button>
        </td>
      </tr>
    `;
  }).join('');
}

function renderFulfillmentPipeline() {
  const stages = [
    { key: 'Stock Reserved', title: '1. Stock Reserved', color: 'blue' },
    { key: 'Picking', title: '2. Picking', color: 'purple' },
    { key: 'Packing', title: '3. Packing & Slip', color: 'orange' },
    { key: 'Dispatched', title: '4. Dispatched', color: 'green' },
    { key: 'Delivered', title: '5. Delivered', color: 'green' }
  ];

  const grid = document.getElementById('pipeline-columns-container');
  if (!grid) return;

  grid.innerHTML = stages.map(st => {
    const ordersInStage = ERP_STATE.orders.filter(o => o.status === st.key);
    return `
      <div class="pipeline-col">
        <div class="pipeline-col-header">
          <span>${st.title}</span>
          <span class="badge badge-${st.color}">${ordersInStage.length}</span>
        </div>
        <div class="pipeline-cards">
          ${ordersInStage.length === 0 ? '<div style="font-size:12px;color:var(--text-muted);text-align:center;padding:24px 0">No orders</div>' : ''}
          ${ordersInStage.map(o => `
            <div class="order-card" onclick="openOrderFulfillmentModal('${o.id}')">
              <div class="order-card-header">
                <span class="mono" style="font-weight:700;color:var(--primary)">${o.id}</span>
                <span style="color:var(--text-muted);font-size:10px">${o.date.split(' ')[1]}</span>
              </div>
              <div class="order-customer">${o.customer}</div>
              <div class="order-items-snippet">
                ${o.items.map(it => `<div>• ${it.qty}x ${it.name.slice(0, 22)}...</div>`).join('')}
              </div>
              <div class="order-card-footer">
                <span class="mono" style="font-weight:700;color:#fff">${fmtCurrency(o.total)}</span>
                <span class="badge badge-blue btn-sm">Process &rarr;</span>
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }).join('');
}

function renderPurchaseOrders() {
  const tbody = document.getElementById('po-table-body');
  if (!tbody) return;

  tbody.innerHTML = ERP_STATE.purchaseOrders.map(po => `
    <tr>
      <td><strong class="mono" style="color:var(--primary)">${po.id}</strong></td>
      <td>
        <strong style="color:#fff">${po.supplierName}</strong><br/>
        <span style="font-size:11px;color:var(--text-muted)">Created: ${po.date}</span>
      </td>
      <td>
        ${po.items.map(it => `<div>${it.qty}x ${it.name}</div>`).join('')}
      </td>
      <td><strong style="color:#fff">${fmtCurrency(po.total)}</strong></td>
      <td><span class="badge badge-blue">${po.warehouse}</span></td>
      <td>
        <span class="badge ${po.status === 'Received' ? 'badge-green' : 'badge-orange'}">
          ${po.status}
        </span>
      </td>
      <td>
        ${po.status === 'Received' ? 
          `<span class="mono" style="font-size:11px;color:var(--success)">${po.grnNumber}</span>` : 
          `<button class="btn btn-primary btn-sm" onclick="receiveGoodsGRN('${po.id}')">Receive &amp; Post GRN</button>`}
      </td>
    </tr>
  `).join('');
}

function renderAuditLogs() {
  const tbody = document.getElementById('audit-table-body');
  if (!tbody) return;

  tbody.innerHTML = ERP_STATE.auditLogs.map(log => `
    <tr>
      <td class="mono" style="font-size:11px;color:var(--text-muted)">${log.timestamp}</td>
      <td><strong style="color:#fff">${log.user}</strong></td>
      <td><span class="badge badge-blue">${log.action}</span></td>
      <td style="font-size:12px;color:var(--text-sub)">${log.details}</td>
    </tr>
  `).join('');
}

function renderAllViews() {
  renderDashboardKPIs();
  renderWarehouseRacks();
  renderInventoryTable();
  renderFulfillmentPipeline();
  renderPurchaseOrders();
  renderAuditLogs();
}

// ================= WORKFLOW ACTIONS =================

// 1. CREATE CUSTOMER ORDER (With Stock Checking & Real-Time Stock Reservation)
function openCreateOrderModal() {
  const select = document.getElementById('co-product-select');
  if (select) {
    select.innerHTML = ERP_STATE.products.map(p => {
      const avail = p.current_stock - p.reserved_stock;
      return `<option value="${p.id}" ${avail <= 0 ? 'disabled' : ''}>
        ${p.name} (SKU: ${p.sku}) — Available: ${avail} | ${fmtCurrency(p.unit_price)}
      </option>`;
    }).join('');
  }
  document.getElementById('modal-create-order').classList.add('active');
}

function submitCustomerOrder(e) {
  e.preventDefault();
  const customer = document.getElementById('co-customer-name').value.trim();
  const warehouse = document.getElementById('co-warehouse-select').value;
  const prodId = parseInt(document.getElementById('co-product-select').value, 10);
  const qty = parseInt(document.getElementById('co-qty-input').value, 10);

  const product = ERP_STATE.products.find(p => p.id === prodId);
  if (!product) return;

  const available = product.current_stock - product.reserved_stock;
  if (qty > available) {
    showToast(`Stock Check Failed! Requested ${qty} units, but only ${available} are currently free.`, 'danger');
    return;
  }

  // Stock Reservation Step
  product.reserved_stock += qty;
  const total = qty * product.unit_price;
  const newOrderId = `ORD-2026-${1050 + ERP_STATE.orders.length + 1}`;

  const newOrder = {
    id: newOrderId,
    customer: customer,
    date: new Date().toISOString().slice(0, 16).replace('T', ' '),
    warehouse: warehouse,
    status: 'Stock Reserved',
    items: [{
      sku: product.sku,
      name: product.name,
      qty: qty,
      price: product.unit_price,
      bin: `${product.zone} / ${product.aisle} / ${product.bin}`
    }],
    total: total,
    picker: 'Pending Assignment',
    trackingNo: null
  };

  ERP_STATE.orders.unshift(newOrder);
  logAudit('Stock Reserved', `Order ${newOrderId} created for ${customer}. Reserved ${qty}x ${product.sku}. Available stock reduced to ${product.current_stock - product.reserved_stock}.`);
  
  closeModal('modal-create-order');
  showToast(`Order ${newOrderId} successfully created and stock reserved!`);
  renderAllViews();
}

// 2. FULFILLMENT PIPELINE STEPPING (Pick -> Pack -> Dispatch -> Deliver)
let activeFulfillmentOrder = null;

function openOrderFulfillmentModal(orderId) {
  const order = ERP_STATE.orders.find(o => o.id === orderId);
  if (!order) return;
  activeFulfillmentOrder = order;

  document.getElementById('f-order-id').textContent = order.id;
  document.getElementById('f-customer-name').textContent = order.customer;
  document.getElementById('f-status-badge').textContent = order.status;
  document.getElementById('f-warehouse').textContent = order.warehouse;
  document.getElementById('f-total-val').textContent = fmtCurrency(order.total);

  // Pick list details
  const pickListContainer = document.getElementById('f-pick-list');
  pickListContainer.innerHTML = order.items.map(it => `
    <div style="background:var(--bg-main);padding:12px;border-radius:6px;border:1px solid var(--border-color);display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
      <div>
        <strong style="color:#fff">${it.name}</strong><br/>
        <span class="mono" style="font-size:12px;color:var(--primary)">Location: ${it.bin}</span>
      </div>
      <div class="mono" style="font-size:16px;font-weight:700;color:var(--warning)">
        Qty: ${it.qty}
      </div>
    </div>
  `).join('');

  // Action button states based on status
  const actionBtn = document.getElementById('f-action-btn');
  if (order.status === 'Stock Reserved') {
    actionBtn.textContent = 'Generate Pick List & Start Picking';
    actionBtn.onclick = () => advanceOrderStatus(order, 'Picking');
  } else if (order.status === 'Picking') {
    actionBtn.textContent = 'Complete Picking & Print Packing Slip';
    actionBtn.onclick = () => advanceOrderStatus(order, 'Packing');
  } else if (order.status === 'Packing') {
    actionBtn.textContent = 'Dispatch Package & Create Shipping Manifest';
    actionBtn.onclick = () => advanceOrderStatus(order, 'Dispatched');
  } else if (order.status === 'Dispatched') {
    actionBtn.textContent = 'Mark Delivered & Close Order';
    actionBtn.onclick = () => advanceOrderStatus(order, 'Delivered');
  } else {
    actionBtn.textContent = 'Order Completed';
    actionBtn.onclick = () => closeModal('modal-fulfillment');
  }

  document.getElementById('modal-fulfillment').classList.add('active');
}

function advanceOrderStatus(order, newStatus) {
  const oldStatus = order.status;
  order.status = newStatus;

  if (newStatus === 'Dispatched') {
    order.trackingNo = 'TRK-' + Math.floor(100000 + Math.random() * 900000);
    // Physically deduct from inventory and release reserved stock
    order.items.forEach(it => {
      const prod = ERP_STATE.products.find(p => p.sku === it.sku);
      if (prod) {
        prod.current_stock -= it.qty;
        prod.reserved_stock = Math.max(0, prod.reserved_stock - it.qty);
      }
    });
    logAudit('Order Dispatched', `Physical stock deducted for ${order.id}. Tracking ID ${order.trackingNo} issued.`);
  } else {
    logAudit(`Fulfillment Step: ${newStatus}`, `Order ${order.id} moved from ${oldStatus} to ${newStatus} by ${ERP_STATE.currentUser.name}.`);
  }

  showToast(`Order ${order.id} status updated to: ${newStatus}`);
  closeModal('modal-fulfillment');
  renderAllViews();
}

// 3. PURCHASE ORDER GOODS RECEIPT (GRN)
function openReorderModal(productId) {
  const prod = ERP_STATE.products.find(p => p.id === productId);
  if (!prod) return;

  const select = document.getElementById('po-supplier-select');
  select.innerHTML = ERP_STATE.suppliers.map(s => `<option value="${s.id}">${s.name} (${s.lead_days} days lead)</option>`).join('');

  document.getElementById('po-product-name').textContent = `${prod.name} (${prod.sku})`;
  document.getElementById('po-product-id').value = prod.id;
  document.getElementById('po-qty-input').value = Math.max(10, prod.safety_stock * 2);

  document.getElementById('modal-raise-po').classList.add('active');
}

function submitPurchaseOrder(e) {
  e.preventDefault();
  const prodId = parseInt(document.getElementById('po-product-id').value, 10);
  const supplierId = document.getElementById('po-supplier-select').value;
  const qty = parseInt(document.getElementById('po-qty-input').value, 10);
  const wh = document.getElementById('po-warehouse-select').value;

  const prod = ERP_STATE.products.find(p => p.id === prodId);
  const supplier = ERP_STATE.suppliers.find(s => s.id === supplierId);
  if (!prod || !supplier) return;

  const newPoId = `PO-2026-${100 + ERP_STATE.purchaseOrders.length + 1}`;
  const total = qty * prod.cost_price;

  ERP_STATE.purchaseOrders.unshift({
    id: newPoId,
    supplierId: supplier.id,
    supplierName: supplier.name,
    date: new Date().toISOString().slice(0, 10),
    expectedDate: '2026-11-22',
    warehouse: wh,
    status: 'In Transit',
    items: [{ sku: prod.sku, name: prod.name, qty: qty, unitCost: prod.cost_price }],
    total: total,
    grnNumber: null
  });

  logAudit('Purchase Order Issued', `Raised ${newPoId} to ${supplier.name} for ${qty}x ${prod.sku}. Total: ${fmtCurrency(total)}.`);
  closeModal('modal-raise-po');
  showToast(`Purchase order ${newPoId} transmitted to supplier.`);
  renderAllViews();
}

function receiveGoodsGRN(poId) {
  const po = ERP_STATE.purchaseOrders.find(p => p.id === poId);
  if (!po || po.status === 'Received') return;

  po.status = 'Received';
  const grnNum = `GRN-2026-00${Math.floor(50 + Math.random() * 40)}`;
  po.grnNumber = grnNum;

  // Add stock to warehouse inventory
  po.items.forEach(it => {
    const prod = ERP_STATE.products.find(p => p.sku === it.sku);
    if (prod) {
      prod.current_stock += it.qty;
    }
  });

  logAudit('Goods Received Note (GRN)', `${grnNum} generated. Received and verified ${po.items[0].qty}x ${po.items[0].sku} into ${po.warehouse}. Inventory increased.`);
  showToast(`Goods received! Inventory stock credited and ${grnNum} posted.`);
  renderAllViews();
}

// 4. SYNOPSIS & ACADEMIC MODAL
function openSynopsisModal() {
  document.getElementById('modal-synopsis').classList.add('active');
}

function closeModal(modalId) {
  const m = document.getElementById(modalId);
  if (m) m.classList.remove('active');
}

// ================= INITIALIZATION =================
document.addEventListener('DOMContentLoaded', () => {
  renderAllViews();

  // Attach outside click listener for modals
  document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) {
        overlay.classList.remove('active');
      }
    });
  });

  console.log("Smart Warehouse & Order Fulfillment ERP initialized successfully.");
});
