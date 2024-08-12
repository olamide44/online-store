# crud.py

from .models import User, Product, Order, OrderItem, Session
from sqlalchemy import extract
from datetime import datetime, timedelta


def get_users():
    users = Session.query(User).all()
    return [user.as_dict() for user in users]


def add_user(name, email, password, address_line1, address_line2, town, county, country, eircode):
    new_user = User(name=name, email=email, password=password, 
                    address_line1=address_line1, address_line2=address_line2, 
                    town=town, county=county, country=country, eircode=eircode)
    Session.add(new_user)
    Session.commit()

def update_user(user_id, name, email, password, address_line1, address_line2, town, county, country, eircode):
    user = Session.query(User).filter(User.id == user_id).first()
    if user:
        user.name = name
        user.email = email
        user.password = password
        user.address_line1 = address_line1
        user.address_line2 = address_line2
        user.town = town
        user.county = county
        user.country = country
        user.eircode = eircode
        Session.commit()
    return user




def delete_user(user_id):
    user = Session.query(User).filter(User.id == user_id).one()
    Session.delete(user)
    Session.commit()

def add_product(name, description, price, stock):
    new_product = Product(name=name, description=description, price=price, stock=stock)
    Session.add(new_product)
    Session.commit()
    return new_product

def get_products():
    products = Session.query(Product).all()
    return [product.as_dict() for product in products]


def get_product_by_id(product_id):
    return Session.query(Product).filter(Product.id == product_id).first()

def update_product(product_id, name=None, description=None, price=None, stock=None):
    product = get_product_by_id(product_id)
    if product:
        if name:
            product.name = name
        if description:
            product.description = description
        if price:
            product.price = price
        if stock:
            product.stock = stock
        Session.commit()
    return product

def delete_product(product_id):
    product = get_product_by_id(product_id)
    if product:
        Session.delete(product)
        Session.commit()
    return product

def get_orders():
    session = Session()
    orders = session.query(Order).all()
    session.close()
    return [order.as_dict() for order in orders]

def get_order_by_id(order_id):
    return Session.query(Order).filter(Order.id == order_id).first()


def get_orders_filtered_by_status(status):
    if status == 'all':
        return Session.query(Order).all()
    else:
        return Session.query(Order).filter(Order.status == status).all()



def get_orders_by_period(period):
    session = Session()
    now = datetime.now()
    
    if period == 'day':
        start_date = now - timedelta(days=1)
    elif period == 'week':
        start_date = now - timedelta(weeks=1)
    elif period == 'month':
        start_date = now - timedelta(days=30)
    elif period == 'year':
        start_date = now - timedelta(days=365)
    else:
        # If no valid period is given, return all orders
        orders = session.query(Order).all()
        session.close()
        return [order.as_dict() for order in orders]
    
    orders = session.query(Order).filter(Order.date_of_order >= start_date).all()
    session.close()
    return [order.as_dict() for order in orders]


def add_order(user_id, total_amount, date_of_order, status):
    order = Order(user_id=user_id, total_amount=total_amount, date_of_order=date_of_order, status=status)
    Session.add(order)
    Session.commit()
    return order

def update_order(order_id, user_id=None, total_amount=None, date_of_order=None, status=None):
    order = get_order_by_id(order_id)
    if order:
        if user_id:
            order.user_id = user_id
        if total_amount:
            order.total_amount = total_amount
        if date_of_order:
            order.date_of_order = date_of_order
        if status:
            order.status = status
        Session.commit()
    return order

def delete_order(order_id):
    order = get_order_by_id(order_id)
    if order:
        Session.delete(order)
        Session.commit()
    return order

def get_orders_filtered(start_date, end_date):
    return Session.query(Order).filter(Order.date_of_order >= start_date, Order.date_of_order <= end_date).all()

def get_order_items():
    return Session.query(OrderItem).all()

def get_order_item_by_id(order_item_id):
    return Session.query(OrderItem).filter(OrderItem.id == order_item_id).first()

def add_order_item(order_id, product_id, quantity, price):
    order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=quantity, price=price)
    Session.add(order_item)
    Session.commit()
    return order_item

def update_order_item(order_item_id, order_id=None, product_id=None, quantity=None, price=None):
    order_item = get_order_item_by_id(order_item_id)
    if order_item:
        if order_id:
            order_item.order_id = order_id
        if product_id:
            order_item.product_id = product_id
        if quantity:
            order_item.quantity = quantity
        if price:
            order_item.price = price
        Session.commit()
    return order_item

def delete_order_item(order_item_id):
    order_item = get_order_item_by_id(order_item_id)
    if order_item:
        Session.delete(order_item)
        Session.commit()
    return order_item

# CRUD operations with date filtering for analytics
def get_orders_filtered(start_date, end_date):
    return Session.query(Order).filter(Order.date_of_order >= start_date, Order.date_of_order <= end_date).all()

def get_users_filtered(start_date, end_date):
    return Session.query(User).filter(User.date_of_order >= start_date, User.date_of_order <= end_date).all()

def get_products_filtered(start_date, end_date):
    return Session.query(Product).filter(Product.date_of_order >= start_date, Product.date_of_order <= end_date).all()
