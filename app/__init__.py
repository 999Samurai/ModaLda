from flask import Flask, redirect
from modules.login import bp as bp_login
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/modalda"
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

app.register_blueprint(bp_login)


@app.route('/')
def login():
    return redirect("/login")


if __name__ == '__main__':
    app.run(port=8000, debug=True)
