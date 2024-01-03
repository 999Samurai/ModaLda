from database import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from modules.login.models import User



class Warehouse(db.Model):
    __tablename__ = 'warehouses'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    address = db.Column(db.String())
    phone = db.Column(db.String())

    def __init__(self, name, address, phone):
        self.name = name
        self.address = address
        self.phone = phone


class Product(db.Model):
    __tablename__ = 'products'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    category = db.Column(db.String())
    color = db.Column(db.String())
    brand = db.Column(db.String())
    min_stock = db.Column(db.Integer())
    max_stock = db.Column(db.Integer())
    last_buy_price = db.Column(db.Float())
    avg_buy_price = db.Column(db.Float())
    sell_price = db.Column(db.Float())
    desc = db.Column(db.String())

    def __init__(
        self, name, category, 
        color, brand, min_stock, 
        max_stock, current_stock, 
        last_buy_price, avg_buy_price, sell_price, desc):
        
        self.name = name
        self.category = category
        self.color = color
        self.brand = brand
        self.min_stock = min_stock
        self.max_stock = max_stock
        self.last_buy_price = last_buy_price
        self.avg_buy_price = avg_buy_price
        self.sell_price = sell_price
        self.desc = desc

    #def __repr__(self):
    #   return f"<User {self.id}>"
    
    
class Product_Warehouse(db.Model):
    __tablename__ = 'products_warehouses'
    __table_args__ = {'extend_existing': True}

    product_id = db.Column(db.Integer, ForeignKey(Product.id), primary_key=True)
    warehouse_id = db.Column(db.Integer, ForeignKey(Warehouse.id), primary_key=True)
    quantity = db.Column(db.Integer)

    product = relationship('Product', foreign_keys='Product_Warehouse.product_id')
    warehouse = relationship('Warehouse', foreign_keys='Product_Warehouse.warehouse_id')

    def __init__(
            self, product_id, warehouse_id, quantity):
        self.product_id = product_id
        self.warehouse_id = warehouse_id
        self.quantity = quantity


class Movements(db.Model):
    __tablename__ = 'movements'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey(User.id), unique=True)
    from_warehouse_id = db.Column(db.Integer, ForeignKey(Warehouse.id), unique=True) #FromWarehouse
    to_warehouse_id = db.Column(db.Integer, ForeignKey(Warehouse.id), unique=True) #ToWarehouse
    typ = db.Column(db.String()) #Type of movement {transfer, devolution, break}
    date = db.Column(db.Date)
    
    def __init__(self, user_id, from_warehouse_id, to_warehouse_id, date):
        self.user_id = user_id
        self.from_warehouse_id = from_warehouse_id
        self.to_warehouse_id = to_warehouse_id
        self.date = date
        
    from_warehouse = relationship('Warehouse', foreign_keys='Movements.from_warehouse_id')
    to_warehouse = relationship('Warehouse', foreign_keys='Movements.to_warehouse_id')
    user = relationship('User', foreign_keys='Movements.user_id')
    
    
class Product_Movements(db.Model):
    __tablename__ = 'product_movements'
    __table_args__ = {'extend_existing': True}
    
    movement_id = db.Column(db.Integer, ForeignKey(Movements.id), primary_key=True)
    product_id = db.Column(db.Integer, ForeignKey(Product.id), primary_key=True)
    quantity = db.Column(db.Integer)
    
    product = relationship('Product', foreign_keys='Product_Movements.product_id')
    movement = relationship('Movements', foreign_keys='Product_Movements.movement_id')
