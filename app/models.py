# models.py

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from .config import DATABASE_URL
from datetime import datetime


# Database setup
engine = create_engine(DATABASE_URL)
Base = declarative_base()
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# Define models
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    address_line1 = Column(String)
    address_line2 = Column(String)
    town = Column(String)
    county = Column(String)
    country = Column(String)
    eircode = Column(String)
    
    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'address_line1': self.address_line1,
            'address_line2': self.address_line2,
            'town': self.town,
            'county': self.county,
            'country': self.country,
            'eircode': self.eircode,
        }

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    stock = Column(Integer)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    total_amount = Column(Float)
    date_of_order = Column(DateTime, default=datetime.utcnow)
    status = Column(String)
    user = relationship("User", back_populates="orders")

    def as_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'total_amount': self.total_amount,
            'date_of_order': self.date_of_order,
            'status': self.status
        }


class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    price = Column(Float)
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

User.orders = relationship("Order", order_by=Order.id, back_populates="user")
Order.order_items = relationship("OrderItem", order_by=OrderItem.id, back_populates="order")
Product.order_items = relationship("OrderItem", order_by=OrderItem.id, back_populates="product")

# Create tables
Base.metadata.create_all(engine)
