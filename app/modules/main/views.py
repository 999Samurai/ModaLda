from flask import render_template, redirect, flash, request, url_for, abort, jsonify
from flask_login import login_required, current_user
from sqlalchemy import text

from .forms import AddUserForm, AddProductForm, AddWarehouseForm

from . import bp
from ..login.models import User
from .models import Product, Warehouse, Product_Warehouse, Movements, Product_Movements
from database import db

ROLES = {
    'admin': 'Admin',
    'gerente': 'Gerente',
    'funcionario': 'Funcionário'
}

CATEGORIES = {
    'calças': 'Calças',
    'blusas|blusões': 'Blusas|Blusões',
    'camisolas|casacos': 'Camisolas|Casacos',
    'camisas': 'Camisas'
}

BRANDS = {
    'zara': 'Zara',
    'bershka': 'Bershka',
    'pull n bear': 'Pull n Bear',
    'springfield': 'Springfield'
}


@bp.route('/home')
@login_required
def home():
    return render_template('home.html', user=current_user, tab="home")


@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user, tab="dashboard")


@bp.route('/users')
@login_required
def users():
    users_query = User.query.with_entities(User.id, User.username, User.role, User.last_login).all()
    all_users = []
    for user in users_query:
        all_users.append(
            {
                "id": user.id,
                "username": user.username,
                "role": ROLES[user.role],
                "last_login": user.last_login.strftime("%d/%m/%Y, %H:%M:%S")
            }
        )
    if current_user.role == 'admin' or current_user.role == 'gerente':
        return render_template('users/users_table.html', user=current_user, tab="users", all_users=all_users)
    else:
        return redirect(request.referrer or 'home')


@bp.route('/users/add')
@login_required
def add_user_get():
    form = AddUserForm()
    if current_user.role == 'admin' or current_user.role == 'gerente':
        return render_template('users/users_add.html', user=current_user, tab="users", form=form)
    else:
        return redirect(request.referrer or 'home')


@bp.route('/users/add', methods=['POST'])
@login_required
def add_user_post():
    form = AddUserForm()
    if form.validate_on_submit():
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get("role")

        record = User(username, password, role)
        db.session.add(record)
        db.session.commit()

        flash('Utilizador criado com sucesso')
        return redirect('/users')
    if current_user.role == 'admin' or current_user.role == 'gerente':
        return render_template('users/users_add.html', user=current_user, tab="users", form=form)
    else:
        return redirect(request.referrer or 'home')


@bp.route('/users/<int:id>')
@login_required
def view_user(id):
    user_view = User.query.filter_by(id=id).first_or_404()

    user = {
        "id": user_view.id,
        "username": user_view.username,
        "role": ROLES[user_view.role],
        "last_login": user_view.last_login.strftime("%d/%m/%Y, %H:%M:%S")
    }

    prev = User.query.order_by(User.id.desc()).filter(User.id < user_view.id).first()
    next = User.query.order_by(User.id.asc()).filter(User.id > user_view.id).first()

    if prev is not None:
        prev = prev.id

    if next is not None:
        next = next.id

    # Testing purposes
    # if prev is None and next is None:
    #     prev = 0
    #     next = 2
    if current_user.role == 'admin' or current_user.role == 'gerente':
        return render_template('users/users_view.html', user=current_user, tab="users",
                               user_view=user, next=next, prev=prev)
    else:
        return redirect(request.referrer or 'home')


@bp.route('/warehouses')
@login_required
def warehouses():
    warehouses_query = Warehouse.query.all()
    if current_user.role == 'admin' or current_user.role == 'gerente':
        return render_template('warehouses/warehouses_table.html', user=current_user, tab="warehouses",
                               all_warehouses=warehouses_query)
    else:
        return redirect(request.referrer or 'home')


@bp.route('/warehouses/add')
@login_required
def add_warehouses_get():
    form = AddWarehouseForm()
    if current_user.role == 'admin' or current_user.role == 'gerente':
        return render_template('warehouses/warehouses_add.html', user=current_user, tab="warehouses", form=form)
    else:
        return redirect(request.referrer or 'home')


@bp.route('/warehouses/add', methods=['POST'])
@login_required
def add_warehouses_post():
    form = AddWarehouseForm()
    if form.validate_on_submit():
        name = request.form.get('name')
        address = request.form.get('address')
        phone = request.form.get("phone")

        record = Warehouse(name, address, phone)
        db.session.add(record)
        db.session.commit()

        flash('Armazém criado com sucesso')
        return redirect('/warehouses')
    if current_user.role == 'admin' or current_user.role == 'gerente':
        return render_template('warehouses/warehouses_add.html', user=current_user, tab="warehouses", form=form)
    else:
        return redirect(request.referrer or 'home')


@bp.route('/warehouses/<int:id>')
@login_required
def view_warehouses(id):
    warehouse = Warehouse.query.filter_by(id=id).first_or_404()

    prev = Warehouse.query.order_by(Warehouse.id.desc()).filter(Warehouse.id < warehouse.id).first()
    next = Warehouse.query.order_by(Warehouse.id.asc()).filter(Warehouse.id > warehouse.id).first()

    if prev is not None:
        prev = prev.id

    if next is not None:
        next = next.id

    # Testing purposes
    # if prev is None and next is None:
    #     prev = 0
    #     next = 2
    if current_user.role == 'admin' or current_user.role == 'gerente':
        return render_template('warehouses/warehouses_view.html', user=current_user, tab="warehouses",
                               warehouse_view=warehouse, next=next, prev=prev)
    else:
        return redirect(request.referrer or 'home')


@bp.route('/products')
@login_required
def products():
    products_query = Product.query.all()

    all_products = []
    for product in products_query:
        all_products.append(
            {
                "id": product.id,
                "name": product.name,
                "category": CATEGORIES[product.category],
                "color": product.color,
                "brand": BRANDS[product.brand],
                "min_stock": product.min_stock,
                "max_stock": product.max_stock,
                "last_buy_price": product.last_buy_price,
                "avg_buy_price": product.avg_buy_price,
                "sell_price": product.sell_price,
                "desc": product.desc,
            }
        )

    return render_template('products/products_table.html', user=current_user, tab="products", all_products=all_products)


@bp.route('/products/add')
@login_required
def add_product_get():
    form = AddProductForm()

    return render_template('products/products_add.html', user=current_user, tab="products", form=form)


@bp.route('/products/add', methods=['POST'])
@login_required
def add_product_post():
    form = AddProductForm()
    if form.validate_on_submit():
        name = request.form.get('name')
        category = request.form.get('category')
        color = request.form.get("color")
        brand = request.form.get('brand')
        min_stock = request.form.get('min_stock')
        max_stock = request.form.get('max_stock')
        last_buy_price = request.form.get('last_buy_price')
        avg_buy_price = request.form.get('avg_buy_price')
        sell_price = request.form.get('sell_price')
        desc = request.form.get('desc')

        record = Product(name, category, color, brand, min_stock, max_stock, last_buy_price,
                         avg_buy_price, sell_price, desc)
        db.session.add(record)
        db.session.commit()

        flash('Produto criado com sucesso')
        return redirect('/products')

    return render_template('products/products_add.html', user=current_user, tab="products", form=form)


@bp.route('/stock')
@login_required
def stock():
    warehouses_query = Warehouse.query.all()

    return render_template('stock/select_warehouse.html', user=current_user, tab="stock",
                           warehouses=warehouses_query)


@bp.route('/stock/all/products')
@login_required
def view_stock():
    query = text('''
        SELECT DISTINCT
            products.id as id,
            products.name AS name,
            SUM(products_warehouses.quantity) AS quantity
        FROM
            products
        LEFT JOIN
            products_warehouses ON products.id = products_warehouses.product_id
        GROUP BY
            products.id
    ''')

    result = db.session.execute(query)
    return render_template('stock/stock_table.html', user=current_user, tab="stock", warehouse=None, products=result)


@bp.route('/stock/<int:id>/products')
@login_required
def view_stock_warehouses(id):
    warehouse = Warehouse.query.filter_by(id=id).first_or_404()

    query = text('''
         SELECT
            products.id as id,
            products.name AS name,
            products_warehouses.quantity AS quantity
        FROM
            products
        LEFT JOIN
            products_warehouses ON products_warehouses.product_id = products.id AND products_warehouses.warehouse_id = :warehouse_id
        LEFT JOIN
            warehouses ON warehouses.id = products_warehouses.warehouse_id
    ''')

    result = db.session.execute(query, {'warehouse_id': id})
    return render_template('stock/stock_table.html', user=current_user, tab="stock", warehouse=warehouse,
                           products=result)


@bp.route('/stock/<int:warehouse_id>/products/<int:product_id>', methods=['GET'])
@login_required
def view_stock_warehouse_product(warehouse_id, product_id):
    warehouse = Warehouse.query.filter_by(id=warehouse_id).first_or_404()
    Product.query.filter_by(id=product_id).first_or_404()

    query = text('''
         SELECT
            products.id as id,
            products.name AS name,
            products_warehouses.quantity AS quantity
        FROM
            products
        LEFT JOIN
            products_warehouses ON products_warehouses.product_id = products.id AND products_warehouses.warehouse_id = :warehouse_id
        LEFT JOIN
            warehouses ON warehouses.id = products_warehouses.warehouse_id
        WHERE products.id = :product_id
    ''')

    result = db.session.execute(query, {'warehouse_id': warehouse_id, 'product_id': product_id}).one()

    return render_template('stock/stock_edit.html', user=current_user, tab="stock",
                           warehouse=warehouse, product=result)


@bp.route('/stock/<int:warehouse_id>/products/<int:product_id>', methods=['POST'])
@login_required
def post_stock_warehouse_product(warehouse_id, product_id):
    Warehouse.query.filter_by(id=warehouse_id).first_or_404()
    Product.query.filter_by(id=product_id).first_or_404()

    product_warehouse = Product_Warehouse.query.filter_by(product_id=product_id, warehouse_id=warehouse_id).first()

    if product_warehouse is None:
        record = Product_Warehouse(product_id=product_id, warehouse_id=warehouse_id, quantity=request.form.get("stock"))
        db.session.add(record)
        db.session.commit()
    else:
        product_warehouse.quantity = request.form.get("stock")
        db.session.flush()
        db.session.commit()

    flash('Stock do produto editado com sucesso')
    return redirect(url_for(f"main.view_stock_warehouses", id=warehouse_id))


@bp.route('/movements')
@login_required
def movements():
    movements_query = Movements.query.all()

    all_movements = []
    for movement in movements_query:
        all_movements.append(
            {
                "id": movement.id,
                "from": movement.from_warehouse_id,
                "to": movement.to_warehouse_id,
                "user": movement.user_id,
                "type": movement.typ,
                "date": movement.date,
            }
        )

    return render_template('movements/movements_table.html', user=current_user, tab="movements",
                           all_movements=all_movements)


@bp.route('/movements/add')
@login_required
def add_movements_get():
    warehouses = Warehouse.query.all()

    return render_template("movements/movements_add.html", user=current_user, tab="movements", warehouses=warehouses)


@bp.route('/api/warehouses/<int:warehouse_id>/products')
@login_required
def api_warehouse_products(warehouse_id):
    Warehouse.query.filter_by(id=warehouse_id).first_or_404()

    query = text('''
         SELECT
            products.id as id,
            products.name AS name,
            products_warehouses.quantity AS quantity
        FROM
            products
        LEFT JOIN
            products_warehouses ON products_warehouses.product_id = products.id AND products_warehouses.warehouse_id = :warehouse_id
        LEFT JOIN
            warehouses ON warehouses.id = products_warehouses.warehouse_id
    ''')

    results = db.session.execute(query, {'warehouse_id': warehouse_id})
    products = []

    for result in results:
        products.append({
            'id': result.id,
            'name': result.name,
            'quantity': result.quantity
        })

    return jsonify(products)
