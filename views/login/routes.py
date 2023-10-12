from flask import render_template
from . import bp


@bp.route('/')
def hello_world():
    return render_template('login.html')
