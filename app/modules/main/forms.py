from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, validators, DecimalField, IntegerField
from wtforms.validators import InputRequired


class AddUserForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), validators.length(max=32)])
    password = PasswordField('Password', validators=[InputRequired(), validators.length(min=6, max=32)])
    role = SelectField('Cargo',
        choices=[('admin', 'Admin'), ('gerente', 'Gerente'), ('funcionario', 'Funcionário')],
        default="funcionario",
        validators=[InputRequired()]
    )


class AddWarehouseForm(FlaskForm):
    name = StringField('Nome', validators=[InputRequired(), validators.length(max=32)])
    address = StringField('Morada', validators=[InputRequired(), validators.length(max=45)])
    phone = StringField('Número de Telemóvel', validators=[InputRequired(), validators.length(min=9, max=15)])


class AddProductForm(FlaskForm):
    name = StringField('Nome', validators=[InputRequired(), validators.length(max=32)])
    category = SelectField('Categoria',
        choices=[('calças', 'Calças'), ('blusas|blusões', 'Blusas|Blusões'), ('camisolas|casacos', 'Camisolas|Casacos'), ('camisas', 'Camisas')],
        validators=[InputRequired()])
    color = StringField('Cor', validators=[InputRequired(), validators.length(max=16)])
    brand = SelectField('Marcas',
        choices=[('zara', 'Zara'), ('bershka', 'Bershka'), ('pull n bear', 'Pull n Bear'), ('springfield', 'Springfield')],
        validators=[InputRequired()])
    min_stock = IntegerField('Stock Min', validators=[InputRequired(), validators.NumberRange(min=1)])
    max_stock = IntegerField('Stock Max', validators=[InputRequired(), validators.NumberRange(min=1)])
    last_buy_price = DecimalField('Último Preço', validators=[InputRequired(), validators.NumberRange(min=0.01)])
    avg_buy_price = DecimalField('Preço Médio', validators=[InputRequired(), validators.NumberRange(min=0.01)])
    sell_price = DecimalField('Preço', validators=[InputRequired(), validators.NumberRange(min=0.01)])
    desc = StringField('Descrição', validators=[validators.optional(), validators.length(min=0, max=32)])