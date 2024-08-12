from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from .crud import (get_users, add_user, update_user, delete_user, get_products, add_product, update_product, delete_product, 
                    get_product_by_id, get_orders, get_order_by_id, get_orders_filtered_by_status, get_orders_by_period, add_order, update_order, delete_order, 
                    get_order_items, get_order_item_by_id, add_order_item, update_order_item, delete_order_item)
import pandas as pd
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    period = request.args.get('period', 'week')
    orders = pd.DataFrame(get_orders_by_period(period))
    users = pd.DataFrame([user for user in get_users()])
    products = pd.DataFrame([product for product in get_products()])

    # Sales Overview
    sales_overview = {
        'labels': orders['date_of_order'].tolist() if not orders.empty else [],
        'data': orders['total_amount'].tolist() if not orders.empty else []
    }

    # User Demographics - example with 'town'
    user_demographics = {
        'labels': users['town'].value_counts().index.tolist() if not users.empty else [],
        'data': users['town'].value_counts().tolist() if not users.empty else []
    }

    # Product Performance
    product_performance = {
        'labels': products['name'].tolist() if not products.empty else [],
        'data': products['stock'].tolist() if not products.empty else []
    }

    return render_template('index.html', sales_overview=sales_overview, user_demographics=user_demographics, product_performance=product_performance, period=period)

@main_bp.route('/users')
def users():
    users = get_users()
    return render_template('users.html', users=users)

@main_bp.route('/products')
def products():
    products = get_products()
    return render_template('products.html', products=products)

@main_bp.route('/orders')
def orders():
    status = request.args.get('status', 'all')
    orders = get_orders_filtered_by_status(status)
    return render_template('orders.html', orders=orders)


@main_bp.route('/order_items')
def order_items():
    order_items = get_order_items()
    return render_template('order_items.html', order_items=order_items)

@main_bp.route('/add_user', methods=['GET', 'POST'])
def add_user_route():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        address_line_1 = request.form['address_line_1']
        address_line_2 = request.form['address_line_2']
        town = request.form['town']
        county = request.form['county']
        country = request.form['country']
        eircode = request.form['eircode']
        add_user(name, email, password, address_line_1, address_line_2, town, county, country, eircode)
        return redirect(url_for('main.users'))
    return render_template('add_user.html')

@main_bp.route('/update_user/<int:user_id>', methods=['GET', 'POST'])
def update_user_route(user_id):
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            address_line1 = request.form['address_line1']
            address_line2 = request.form['address_line2']
            town = request.form['town']
            county = request.form['county']
            country = request.form['country']
            eircode = request.form['eircode']
            
            update_user(user_id, name, email, password, address_line1, address_line2, town, county, country, eircode)
            return redirect(url_for('main.users'))
        except KeyError as e:
            return f"Missing form field: {e}", 400

    # Handling the GET request
    user = next((u for u in get_users() if u['id'] == user_id), None)
    if user:
        return render_template('update_user.html', user=user)
    else:
        return "User not found", 404



@main_bp.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user_route(user_id):
    delete_user(user_id)
    return redirect(url_for('main.users'))

@main_bp.route('/add_product', methods=['GET', 'POST'])
def add_product_route():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        stock = request.form['stock']
        add_product(name, description, price, stock)
        return redirect(url_for('main.products'))
    return render_template('add_product.html')

@main_bp.route('/update_product/<int:product_id>', methods=['GET', 'POST'])
def update_product_route(product_id):
    product = get_product_by_id(product_id)
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        stock = request.form['stock']
        update_product(product_id, name, description, price, stock)
        return redirect(url_for('main.products'))
    return render_template('update_product.html', product=product)

@main_bp.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product_route(product_id):
    delete_product(product_id)
    return redirect(url_for('main.products'))

@main_bp.route('/add_order', methods=['GET', 'POST'])
def add_order_route():
    if request.method == 'POST':
        user_id = request.form['user_id']
        total_amount = request.form['total_amount']
        date_of_order = request.form['date_of_order']
        status = request.form['status']
        add_order(user_id, total_amount, date_of_order, status)
        return redirect(url_for('main.orders'))
    return render_template('add_order.html')

@main_bp.route('/update_order/<int:order_id>', methods=['GET', 'POST'])
def update_order_route(order_id):
    order = get_order_by_id(order_id)
    if request.method == 'POST':
        user_id = request.form['user_id']
        total_amount = request.form['total_amount']
        date_of_order = request.form['date_of_order']
        status = request.form['status']
        update_order(order_id, user_id, total_amount, date_of_order, status)
        return redirect(url_for('main.orders'))
    return render_template('update_order.html', order=order)

@main_bp.route('/delete_order/<int:order_id>', methods=['POST'])
def delete_order_route(order_id):
    delete_order(order_id)
    return redirect(url_for('main.orders'))

@main_bp.route('/add_order_item', methods=['GET', 'POST'])
def add_order_item_route():
    if request.method == 'POST':
        order_id = request.form['order_id']
        product_id = request.form['product_id']
        quantity = request.form['quantity']
        price = request.form['price']
        add_order_item(order_id, product_id, quantity, price)
        return redirect(url_for('main.order_items'))
    return render_template('add_order_item.html')

@main_bp.route('/update_order_item/<int:order_item_id>', methods=['GET', 'POST'])
def update_order_item_route(order_item_id):
    order_item = get_order_item_by_id(order_item_id)
    if request.method == 'POST':
        order_id = request.form['order_id']
        product_id = request.form['product_id']
        quantity = request.form['quantity']
        price = request.form['price']
        update_order_item(order_item_id, order_id, product_id, quantity, price)
        return redirect(url_for('main.order_items'))
    return render_template('update_order_item.html', order_item=order_item)

@main_bp.route('/delete_order_item/<int:order_item_id>', methods=['POST'])
def delete_order_item_route(order_item_id):
    delete_order_item(order_item_id)
    return redirect(url_for('main.order_items'))

def register_routes(app):
    app.register_blueprint(main_bp)
