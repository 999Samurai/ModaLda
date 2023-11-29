from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, validators
from wtforms.validators import InputRequired


class AddUserForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), validators.length(max=32)])
    password = PasswordField('Password', validators=[InputRequired(), validators.length(min=6, max=32)])
    role = SelectField('Cargo',
        choices=[('admin', 'Admin'), ('gerente', 'Gerente'), ('funcionario', 'Funcionário')],
        default="funcionario",
        validators=[InputRequired()]
    )
