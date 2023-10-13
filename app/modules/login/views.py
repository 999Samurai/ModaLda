from flask import render_template
from . import bp


@bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('index.html')
