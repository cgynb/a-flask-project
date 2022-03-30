import wtforms
from wtforms.validators import length, email, EqualTo
from models import EmailCaptchaModel, UserModel
from werkzeug.security import check_password_hash
from flask import g


class RegisterForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=3, max=20)])
    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[length(min=6, max=20)])
    confirm = wtforms.StringField(validators=[EqualTo("password")])
    captcha = wtforms.StringField(validators=[length(min=4, max=4)])
    role = wtforms.StringField(validators=[length(min=1, max=1)])

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        print(captcha_model.email, captcha, captcha_model.captcha)
        if (not captcha_model) or (captcha_model.captcha.lower() != captcha.lower()):
            raise wtforms.ValidationError('邮箱验证错误！')

    def validate_email(self, field):
        email = field.data
        user_model = UserModel.query.filter_by(email=email).first()
        if user_model:
            raise wtforms.ValidationError('邮箱已经存在！')

    def validate_role_id(self, field):
        role = field.data
        if role not in ('1', '2', '3'):
            raise wtforms.ValidationError('职业选择错误')


class LoginForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=3, max=20)])
    password = wtforms.StringField(validators=[length(min=6, max=20)])

    def validate_password(self, field):
        password = field.data
        user = UserModel.query.filter(UserModel.username == self.username.data).first()
        if user:
            right_password = user.password
        else:
            raise wtforms.ValidationError('无此用户')
        if not check_password_hash(right_password, password):
            raise wtforms.ValidationError('密码不对')


class NewUserNameForm(wtforms.Form):
    newusername = wtforms.StringField(validators=[length(min=3, max=20)])


class NewPasswordForm(wtforms.Form):
    password = wtforms.StringField(validators=[length(min=6, max=20)])
    newpassword = wtforms.StringField(validators=[length(min=6, max=20)])

    def validate_password(self, field):
        password = field.data
        if not check_password_hash(g.user.password, password):
            raise wtforms.ValidationError('原密码不对')
