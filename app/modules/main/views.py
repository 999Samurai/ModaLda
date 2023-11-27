from flask import render_template
from flask_login import login_required, current_user

from . import bp
from ..login.models import User

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
                "role": user.role,
                "last_login": user.last_login.strftime("%d/%m/%Y, %H:%M:%S")
            }
        )

    return render_template('users.html', user=current_user, tab="users", all_users=all_users)
