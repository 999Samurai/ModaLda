from flask import Flask
from .views.login import bp as login_bp

app = Flask(__name__)

app.register_blueprint(login_bp)
