from flask import render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user, login_user, logout_user

from .models import User
from . import bp


@bp.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    return render_template('login.html')


# POST /login
# @param username
# @param password
@bp.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username, password=password).first()
    if user is None:
        flash('Verifique o seu login e tente novamente.')
        return redirect(url_for("auth.login"))

    login_user(user)
    return redirect(url_for("main.dashboard"))


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
