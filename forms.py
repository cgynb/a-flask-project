from flask import g
import wtforms
from wtforms.validators import length, email, EqualTo

from models import EmailCaptchaModel, UserModel
from werkzeug.security import check_password_hash


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[length(min=6, max=20)])


class RegisterForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=3, max=20)])
    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[length(min=6, max=20)])
    password_confirm = wtforms.StringField(validators=[EqualTo("password")])
    role_id = wtforms.StringField(validators=[length(min=1, max=1)])

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if (not captcha_model) or (captcha_model.captcha.lower() != captcha.lower()):
            raise wtforms.ValidationError('邮箱验证错误！')

    def validate_email(self, field):
        email = field.data
        user_model = UserModel.query.filter_by(email=email).first()
        if user_model:
            raise wtforms.ValidationError('邮箱已经存在！')

    def validate_role_id(self, field):
        role_id = field.data
        if role_id not in ('1', '2', '3'):
            raise wtforms.ValidationError('职业选择错误')


class FoodForm(wtforms.Form):
    food_name = wtforms.StringField(validators=[length(min=1, max=200)])
    food_price = wtforms.StringField(validators=[length(min=1, max=6)])
    food_desc = wtforms.TextAreaField(validators=[length(min=5)])

    def validate_food_price(self, field):
        food_price = field.data
        if int(food_price) not in range(0, 100000):
            raise wtforms.ValidationError('价格不对')


class ChangePassForm(wtforms.Form):
    old_password = wtforms.StringField(validators=[length(min=6, max=20)])
    new_password = wtforms.StringField(validators=[length(min=6, max=20)])
    def validate_old_password(self, field):
        password = field.data
        if not check_password_hash(g.user.password, password):
            raise wtforms.ValidationError('原密码不对')