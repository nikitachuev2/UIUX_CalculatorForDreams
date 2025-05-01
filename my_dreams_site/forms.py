import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError

def validate_custom_email(form, field):
    # Дополнительная защита — кастомное регулярное выражение
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_regex, field.data):
        raise ValidationError("Неверный формат email адреса.")

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message="Поле email обязательно для заполнения."),
        Email(message="Пожалуйста, введите корректный email."),
        validate_custom_email
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(message="Введите пароль.")
    ])
    submit = SubmitField('Зарегистрироваться')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message="Введите email."),
        Email(message="Неверный формат email."),
        validate_custom_email
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(message="Введите пароль.")
    ])
    submit = SubmitField('Войти')

class PurchaseForm(FlaskForm):
    category = StringField('Категория', validators=[DataRequired()])
    amount = FloatField('Сумма', validators=[DataRequired()])
    submit = SubmitField('Добавить покупку')

class GoalForm(FlaskForm):
    dream_name = StringField('Название мечты', validators=[DataRequired()])
    target_amount = FloatField('Целевая сумма', validators=[DataRequired()])
    submit = SubmitField('Установить цель')

class ContributionForm(FlaskForm):
    amount = FloatField('Сумма', validators=[DataRequired()])
    submit = SubmitField('Добавить взнос')
 