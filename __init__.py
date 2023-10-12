from flask import Flask
from views.login import bp as bp_login

app = Flask(__name__)

app.register_blueprint(bp_login)

if __name__ == '__main__':
    app.run(debug=True)
