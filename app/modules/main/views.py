from flask import render_template
from flask_login import login_required, current_user

from . import bp


@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user, tab="dashboard")


@bp.route('/users')
@login_required
def users():
    return render_template('users.html', user=current_user, tab="users")
