from database import db


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
    current_stock = db.Column(db.Integer())
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
        self.current_stock = current_stock
        self.last_buy_price = last_buy_price
        self.avg_buy_price = avg_buy_price
        self.sell_price = sell_price
        self.desc = desc

    #def __repr__(self):
    #   return f"<User {self.id}>"
