from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, validators, FloatField, IntegerField
from wtforms.validators import InputRequired


class AddUserForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), validators.length(max=32)])
    password = PasswordField('Password', validators=[InputRequired(), validators.length(min=6, max=32)])
    role = SelectField('Cargo',
        choices=[('admin', 'Admin'), ('gerente', 'Gerente'), ('funcionario', 'Funcionário')],
        default="funcionario",
        validators=[InputRequired()]
    )
    
class AddProductForm(FlaskForm):
    name = StringField('Nome', validators=[InputRequired(), validators.length(max=32)])
    category = SelectField('Categoria',
        choices=[('calças', 'Calças'), ('blusas|blusões', 'Blusas|Blusões'), ('camisolas|casacos', 'Camisolas|Casacos'), ('camisas', 'Camisas')],
        default="escolha uma categoria",
        validators=[InputRequired()])
    color = StringField('Cor', validators=[InputRequired(), validators.length(max=16)])
    brand = SelectField('Marcas',
        choices=[('zara', 'Zara'), ('bershka', 'Bershka'), ('pull n bear', 'Pull n Bear'), ('springfield', 'Springfield')],
        default="escolha uma categoria",
        validators=[InputRequired()])
    min_stock = IntegerField('Stock Min', validators=[InputRequired(), validators.length(min=1)])
    max_stock = IntegerField('Stock Max', validators=[InputRequired(), validators.length(min=1, max=100)])
    current_stock = IntegerField('Stock', validators=[InputRequired(), validators.length(min=1, max=100)])
    last_buy_price = FloatField('Último Preço', validators=[InputRequired(), validators.length(min=4, max=6)])
    avg_buy_price = FloatField('Preço Médio', validators=[InputRequired(), validators.length(min=4, max=6)])
    sell_price = FloatField('Preço', validators=[InputRequired(), validators.length(min=4, max=6)])
    desc = StringField('Descrição', validators=[InputRequired(), validators.length(min=6, max=32)])
