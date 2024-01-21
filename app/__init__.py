from flask import Flask, redirect, url_for, render_template
from flask_login import current_user

from database import db
from login_manager import login_manager

from modules.login import bp as bp_login
from modules.main import bp as bp_main


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'm0zcHMigdfCvUcV'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"
    app.config['JSON_AS_ASCII'] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(bp_login)
    app.register_blueprint(bp_main)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Efetue o login para aceder a esta página."
    login_manager.init_app(app)
    
    @app.route('/')
    def home():
        if current_user.is_authenticated:
            return redirect(url_for("main.home"))
        return redirect(url_for("auth.login"))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=8000, debug=True)
