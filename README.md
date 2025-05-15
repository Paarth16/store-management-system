# 🛒 Store Management System

A web-based store management system built with **Flask**, **MySQL**, and **Bootstrap**. It handles employee and inventory management, billing operations, customer receipts, and tracks sales efficiently with a clear and intuitive interface.

---

## 🚀 Features

- 🔐 **Employee Login** (with role-based redirection: manager or staff)
- 👨‍💼 **Employee Management** (Add, Edit, Delete, Search)
- 📦 **Inventory Management** (Add, Edit, Delete, Search)
- 🧾 **Billing System** with:
  - Live product search
  - Quantity selection
  - Automated price calculation
- 📱 **Customer Details Capture** with mobile verification
- 🧾 **Receipt Generation**
- 📉 **Stock Update** after purchase
- 🧭 **Session-based Cart** tracking
- 🔙 Smart **Back to Billing** to edit cart before checkout

---

## 🗂️ Project Structure
```plaintext
.
├── app.py                  # Main Flask application
├── Create tables.py        # Script to create database tables
├── Store_Structure.sql     # SQL dump of the database schema
└── templates/
    ├── login.html
    ├── dashboard.html
    ├── add_inventory.html
    ├── delete_inventory.html
    ├── edit_inventory.html
    ├── employee.html
    ├── add_employee.html
    ├── delete_employee.html
    ├── edit_employee.html
    ├── billing.html
    ├── checkout.html
    └── receipt.html
```
---

## 🛠️ Technologies Used

- Backend: Python, Flask
- Frontend: HTML5, Bootstrap 5
- Database: MySQL (via PyMySQL)
- Tools: MySQL Workbench, VS Code

---

## 💽 Database Structure

Tables
- employee: Employee details and login credentials
- inventory: Product stock data
- cart: Temporarily holds items during billing
- customer: Stores customer info
- receipt: Records finalized transactions


For schema:
- Use Store_Structure.sql to import the full schema
- Or run Create tables.py to create tables programmatically

---

## ⚙️ Setup Instructions
1. Clone the repo
  git clone https://github.com/Paarth16/store-management-system.git
  cd store-management-system

2. Install dependencies
  pip install flask pymysql

3. Setup MySQL:
- Open MySQL Workbench
  - Run Store_Structure.sql 
  OR
- Run Create tables.py

4. Run the Flask app
  python app.py

5. Access the app
  Navigate to http://localhost:5000 in your browser.

## 🧪 Default Login for Testing
Use any employee record from your database.
  - Username: Mobile Number
  - Password: Date of Birth (YYYY-MM-DD)

## 📌 Author
Developed by Paarth Sharma
GitHub: @Paarth16