from flask import render_template, redirect, flash, request
from flask_login import login_required, current_user
from .forms import AddUserForm, AddProductForm, AddWarehouseForm

from . import bp
from ..login.models import User
from .models import Product, Warehouse
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

    return render_template('users/users_table.html', user=current_user, tab="users", all_users=all_users)


@bp.route('/users/add')
@login_required
def add_user_get():
    form = AddUserForm()

    return render_template('users/users_add.html', user=current_user, tab="users", form=form)


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

    return render_template('users/users_add.html', user=current_user, tab="users", form=form)


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

    return render_template('users/users_view.html', user=current_user, tab="users",
                           user_view=user, next=next, prev=prev)


@bp.route('/warehouses')
@login_required
def warehouses():
    warehouses_query = Warehouse.query.all()

    return render_template('warehouses/warehouses_table.html', user=current_user, tab="warehouses",
                           all_warehouses=warehouses_query)


@bp.route('/warehouses/add')
@login_required
def add_warehouses_get():
    form = AddWarehouseForm()

    return render_template('warehouses/warehouses_add.html', user=current_user, tab="warehouses", form=form)


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

    return render_template('warehouses/warehouses_add.html', user=current_user, tab="warehouses", form=form)


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

    return render_template('warehouses/warehouses_view.html', user=current_user, tab="warehouses",
                           warehouse_view=warehouse, next=next, prev=prev)


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
        
        record = Product(name, category, color, brand, min_stock, max_stock, current_stock, last_buy_price, avg_buy_price, sell_price, desc)
        db.session.add(record)
        db.session.commit()

        flash('Produto criado com sucesso')
        return redirect('/products')

    return render_template('products/products_add.html', user=current_user, tab="products", form=form)
