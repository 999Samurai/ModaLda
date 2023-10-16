from flask import Flask, redirect, url_for
from flask_login import LoginManager, current_user

from database import db

from app.modules.login import bp as bp_login
from app.modules.main import bp as bp_main


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'm0zcHMigdfCvUcV'
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:diogo123123@localhost:5432/modalda"
    db.init_app(app)

    app.register_blueprint(bp_login)
    app.register_blueprint(bp_main)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Efetue o login para aceder a esta página."
    login_manager.init_app(app)

    from modules.login.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/')
    def home():
        if current_user.is_authenticated:
            return redirect(url_for("main.dashboard"))
        return redirect(url_for("auth.login"))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=8000, debug=True)
