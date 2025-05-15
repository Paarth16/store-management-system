from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import pymysql
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='1029384756',
        database='shop'
    )

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    mobile = request.form.get('mobile')
    dob = request.form.get('dob')

    if not mobile or not dob:
        flash("Please fill in all fields.")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT Emp_ID, Name, Post FROM employee WHERE Mobile_no=%s AND DOB=%s", (mobile, dob))
        result = cursor.fetchone()
    finally:
        conn.close() 

    if result:
        emp_id, name, role = result
        session['username'] = name
        session['role'] = role.lower()
        session['employee_id'] = emp_id

        if session['role'] == 'manager':
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('billing'))
    else:
        flash("Invalid mobile number or date of birth.")
        return redirect(url_for('login'))

    
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.")
    return redirect(url_for('login'))


@app.route('/employee', methods=['GET', 'POST'])
def manage_employee():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    search_query = "SELECT * FROM employee"
    values = []

    if request.method == 'POST':
        field = request.form.get('field')
        keyword = request.form.get('keyword')

        if field and keyword:
            search_query += f" WHERE {field} LIKE %s"
            values.append(f"%{keyword}%")

    cursor.execute(search_query, values)
    employees = cursor.fetchall()
    conn.close()

    return render_template('employee.html', employees=employees)

@app.route('/employee/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form.get('name')
        mobile = request.form.get('mobile')
        dob = request.form.get('dob')
        email = request.form.get('email')
        address = request.form.get('address')
        post = request.form.get('post')
        salary = request.form.get('salary')

        if not all([name, mobile, dob, email, address, post]):
            flash("Please fill in all required fields.", "danger")
            return redirect(url_for('add_employee'))

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO employee (Name, Mobile_no, DOB, Email, Address, Post, Salary)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (name, mobile, dob, email, address, post, salary or None))
            conn.commit()
            flash("Employee added successfully!", "success")
            return redirect(url_for('manage_employee'))
        except pymysql.MySQLError as e:
            flash(f"Error: {e}", "danger")
            return redirect(url_for('add_employee'))
        finally:
            conn.close()

    return render_template('add_employee.html')

@app.route('/employee/delete', methods=['GET', 'POST'])
def delete_employee():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        emp_id = request.form.get('emp_id')
        cursor.execute("DELETE FROM employee WHERE Emp_ID=%s", (emp_id,))
        conn.commit()
        flash("Employee deleted successfully!")
        return redirect(url_for('delete_employee'))

    field = request.args.get('field')
    query = request.args.get('query')
    
    if field and query:
        cursor.execute(f"SELECT * FROM employee WHERE {field} LIKE %s", (f"%{query}%",))
    else:
        cursor.execute("SELECT * FROM employee")

    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('delete_employee.html', employees=records)

@app.route('/employee/edit', methods=['GET', 'POST'])
def edit_employee():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST':
        emp_id = request.form['Emp_ID']
        name = request.form['Name']
        mobile = request.form['Mobile_no']
        dob = request.form['DOB']
        email = request.form['Email']
        address = request.form['Address']
        post = request.form['Post']
        salary = request.form['Salary']

        cursor.execute("""
            UPDATE employee 
            SET Name=%s, Mobile_no=%s, DOB=%s, Email=%s, Address=%s, Post=%s, Salary=%s 
            WHERE Emp_ID=%s
        """, (name, mobile, dob, email, address, post, salary, emp_id))
        conn.commit()
        flash("Employee details updated successfully!", "success")
        return redirect(url_for('edit_employee'))

    edit_id = request.args.get('edit_id')
    edit_employee = None
    if edit_id:
        cursor.execute("SELECT * FROM employee WHERE Emp_ID=%s", (edit_id,))
        edit_employee = cursor.fetchone()

    field = request.args.get('field')
    query = request.args.get('query')
    if field and query:
        cursor.execute(f"SELECT * FROM employee WHERE {field} LIKE %s", (f"%{query}%",))
    else:
        cursor.execute("SELECT * FROM employee")

    employees = cursor.fetchall()
    conn.close()
    return render_template('edit_employee.html', employees=employees, edit_employee=edit_employee)

@app.route('/inventory', methods=['GET', 'POST'])
def manage_inventory():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    query = "SELECT * FROM inventory"
    values = []
    
    if request.method == 'POST':
        field = request.form.get('field')
        keyword = request.form.get('keyword')
        if field and keyword:
            query += f" WHERE {field} LIKE %s"
            values.append(f"%{keyword}%")
    
    cursor.execute(query, values)
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('inventory.html', products=products)

@app.route('/inventory/add', methods=['GET', 'POST'])
def add_inventory():
    if request.method == 'POST':
        product_id = request.form['Product_ID']
        name = request.form['Name']
        brand = request.form['Brand']
        category = request.form['Category']
        price = request.form['Price']
        quantity = request.form['Quantity']
    
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM inventory WHERE Product_ID = %s", (product_id,))
        existing = cursor.fetchone()
    
        if existing:
            flash('Error: Product ID already exists.', 'danger')
            cursor.close()
            conn.close()
            return redirect(url_for('add_inventory'))

        query = """
            INSERT INTO inventory (Product_ID, Name, Brand, Category, Price, Quantity)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (product_id, name, brand, category, price, quantity))
        conn.commit()
    
        cursor.close()
        conn.close()
    
        flash('Product added successfully!', 'success')
        return redirect(url_for('manage_inventory'))
    
    return render_template('add_inventory.html')

@app.route('/inventory/delete', methods=['GET', 'POST'])
def delete_inventory():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        prod_id = request.form.get('Product_ID')
        cursor.execute("DELETE FROM inventory WHERE Product_ID=%s", (prod_id,))
        conn.commit()
        flash("Product deleted successfully!", "success")
        return redirect(url_for('delete_inventory'))
    
    field = request.args.get('field')
    query = request.args.get('query')
    if field and query:
        cursor.execute(f"SELECT * FROM inventory WHERE {field} LIKE %s", (f"%{query}%",))
    else:
        cursor.execute("SELECT * FROM inventory")
    
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('delete_inventory.html', products=products)

@app.route('/inventory/edit', methods=['GET', 'POST'])
def edit_inventory():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    edit_id = request.args.get('edit_id') 

    if request.method == 'POST':
        original_product_id = request.form.get('original_Product_ID') 
        new_product_id = request.form.get('Product_ID')
        name = request.form.get('Name')
        brand = request.form.get('Brand')
        category = request.form.get('Category')
        price = request.form.get('Price')
        quantity = request.form.get('Quantity')

        query = """
            UPDATE inventory
            SET Product_ID = %s, Name = %s, Brand = %s, Category = %s, Price = %s, Quantity = %s
            WHERE Product_ID = %s
        """
        values = (new_product_id, name, brand, category, price, quantity, original_product_id)

        try:
            cursor.execute(query, values)
            conn.commit()
            flash('Product updated successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error updating product: {e}', 'danger')
        return redirect(url_for('edit_inventory'))

    products = []
    edit_product = None

    search_field = request.args.get('field')
    search_query = request.args.get('query')

    try:
        base_query = "SELECT * FROM inventory"
        if search_field and search_query:
            query = f"{base_query} WHERE {search_field} LIKE %s"
            cursor.execute(query, (f"%{search_query}%",))
        else:
            cursor.execute(base_query)
        products = cursor.fetchall()

        if edit_id:
            cursor.execute("SELECT * FROM inventory WHERE Product_ID = %s", (edit_id,))
            edit_product = cursor.fetchone()
    except Exception as e:
        flash(f'Error fetching products: {e}', 'danger')

    return render_template('edit_inventory.html', products=products, edit_product=edit_product)

@app.route('/billing', methods=['GET', 'POST'])
def billing():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
   
    if request.method == 'POST':
        items = request.get_json()['items']
        Cart_no = session.get('Cart_no')

        if not Cart_no:
            cursor.execute("SELECT IFNULL(MAX(Cart_no), 0) + 1 AS new_id FROM cart")
            Cart_no = cursor.fetchone()['new_id']
            session['Cart_no'] = Cart_no
            
            cursor.execute("DELETE FROM cart WHERE Cart_no = %s", (Cart_no,))
            conn.commit()

        for item in items:
            cursor.execute("""
                INSERT INTO cart (Cart_no, Product_ID, Name, Brand, Price, Category, Quantity)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                Cart_no,
                item['Product_ID'],
                item['Name'],
                item['Brand'],
                item['Price'],
                item['Category'],
                item['Quantity']
            ))

        conn.commit()
        return jsonify({'status': 'success', 'cart_id': Cart_no})  # updated to return 'cart_id'
    
    cursor.execute("SELECT * FROM inventory")
    products = cursor.fetchall()
    return render_template('billing.html', products=products)
    
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    Cart_no = session.get('Cart_no')

    if not Cart_no:
        flash('No active cart. Please start billing first.')
        return redirect(url_for('billing'))

    cursor.execute("""
        SELECT p.Product_ID, p.Name, p.Brand, p.Price, c.Quantity
        FROM cart c
        JOIN inventory p ON c.Product_ID = p.Product_ID
        WHERE c.Cart_no = %s
    """, (Cart_no,))
    cart_items = cursor.fetchall()
    total_amount = float(sum(item['Price'] * item['Quantity'] for item in cart_items))

    existing = False
    checked_mobile = None
    customer = None
    Cname = None

    if request.method == 'POST':
        mobile = request.form['mobile']

        if 'check_mobile' in request.form:
            checked_mobile = mobile
            cursor.execute("SELECT * FROM customer WHERE Mobile_no = %s", (mobile,))
            customer = cursor.fetchone()
            existing = bool(customer)
            if existing:
                Cname = customer['Name']

        elif 'proceed' in request.form:
            if request.form.get('name'): 
                name = request.form['name']
                dob = request.form['dob']
                gender = request.form['gender']
                cursor.execute("""
                    INSERT INTO customer (Mobile_no, Name, Dob, Gender)
                    VALUES (%s, %s, %s, %s)
                """, (mobile, name, dob, gender))
                Cname = name
            else:
                cursor.execute("SELECT Name FROM customer WHERE Mobile_no = %s", (mobile,))
                result = cursor.fetchone()
                if result:
                    Cname = result['Name']
        
            cursor.execute("""
                INSERT INTO receipt (Cart_no, Emp_ID, Date_Time, CMobile_no, Cname, Total)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (Cart_no, session['employee_id'], datetime.now(), mobile, Cname, total_amount))

            for item in cart_items:
                cursor.execute("""
                    UPDATE inventory
                    SET Quantity = Quantity - %s
                    WHERE Product_ID = %s
                """, (item['Quantity'], item['Product_ID']))

            conn.commit()
    
            session['last_cart'] = Cart_no
            session.pop('Cart_no', None)
            return redirect(url_for('receipt'))


    return render_template('checkout.html',
                           cart_items=cart_items,
                           total_amount=total_amount,
                           checked_mobile=checked_mobile,
                           customer=customer,
                           existing=existing)

@app.route('/receipt')
def receipt():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    Cart_no = session.get('last_cart')

    if not Cart_no:
        flash("No active cart found.")
        return redirect(url_for('billing'))

    cursor.execute("""
        SELECT r.Receipt_no AS Receipt_ID, r.Emp_ID AS Employee_ID, e.Name AS EmployeeName, 
               r.Date_Time, r.cMobile_no AS Mobile_no, cu.Name AS CustomerName
        FROM receipt r
        JOIN employee e ON r.Emp_ID = e.Emp_ID
        JOIN customer cu ON r.cMobile_no = cu.Mobile_no
        WHERE r.Cart_no = %s
        ORDER BY r.Receipt_no DESC LIMIT 1
    """, (Cart_no,))
    receipt_info = cursor.fetchone()

    if not receipt_info:
        flash("Receipt not found.")
        return redirect(url_for('billing'))

    cursor.execute("""
        SELECT i.Product_ID, i.Name, i.Brand, i.Price, c.Quantity
        FROM cart c
        JOIN inventory i ON c.Product_ID = i.Product_ID
        WHERE c.Cart_no = %s
    """, (Cart_no,))
    items = cursor.fetchall()

    total_amount = sum(item['Price'] * item['Quantity'] for item in items)

    session.pop('last_cart', None)

    cursor.close()
    conn.close()

    return render_template('receipt.html', receipt=receipt_info, items=items, total_amount=total_amount)


@app.route('/back_to_billing')
def back_to_billing():
    Cart_no = session.pop('Cart_no', None)
    if Cart_no is not None:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cart WHERE Cart_no = %s", (Cart_no,))
        conn.commit()
        conn.close()
    return redirect(url_for('billing'))

if __name__ == '__main__':
    app.run(debug=True)
