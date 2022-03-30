from flask import Blueprint, jsonify, render_template, request, session, redirect, flash, url_for, g
from exts import mail, db
import string
import random
import datetime
import time
import os
from werkzeug.security import generate_password_hash
from flask_mail import Message
from models import EmailCaptchaModel, UserModel, FoodModel, OrderModel
from forms import RegisterForm, LoginForm, NewUserNameForm, NewPasswordForm
from require import login_required, merchant_required

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/')
def homepage():
    return render_template('homepage.html')


@bp.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        form = RegisterForm(request.form)
        print(request.form.to_dict())
        if form.validate():
            try:
                username = form.username.data
                password = generate_password_hash(form.password.data)
                email = form.email.data
                role = form.role.data
                user = UserModel(email=email, username=username, password=password, role=role)
                db.session.add(user)
                db.session.commit()
                flash('注册成功')
            except Exception as e:
                flash('注册失败')
            return redirect(url_for('food.index'))
        else:
            flash('注册失败')
            return render_template('register.html')


@bp.route('/captcha/', methods=['GET', 'POST'])
def get_captcha():
    email = request.form.get('email')
    try:
        if email:
            s = string.ascii_letters + string.digits
            captcha = ''.join(random.sample(s, 4))
            message = Message(
                subject='饿了不',
                recipients=[email],
                body=f'验证码是：{captcha}，请不要告诉他人',
            )
            mail.send(message)
            captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
            if captcha_model:
                captcha_model.captcha = captcha
                db.session.commit()
            else:
                captcha_model = EmailCaptchaModel(email=email, captcha=captcha)
                db.session.add(captcha_model)
                db.session.commit()
            return jsonify({'status': 200, 'message': '发送成功'})
        else:
            return jsonify({'status': 400, 'message': '请填写邮箱'})
    except:
        return jsonify({'status': 400, 'message': '未知错误'})


@bp.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            user = UserModel.query.filter(UserModel.username == form.username.data).first()
            flash('登录成功')
            session['username'] = user.username
            session['role'] = user.role
            session['user_id'] = user.id
            return redirect(url_for('food.index'))
        else:
            flash('登陆失败')
            return render_template('login.html')


@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for("food.index"))


@bp.route('/change_username/', methods=['POST'])
def change_username():
    form = NewUserNameForm(request.form)
    if form.validate():
        user = UserModel.query.filter(UserModel.id == g.user.id).first()
        user.username = form.newusername.data
        db.session.commit()
        flash('修改成功')
    else:
        flash('用户名应在3-20个字符之间')
    return redirect(url_for('user.homepage'))


@bp.route('/change_password/', methods=['POST'])
def change_password():
    form = NewPasswordForm(request.form)
    if form.validate():
        user = UserModel.query.filter(UserModel.id == g.user.id).first()
        user.password = generate_password_hash(form.newpassword.data)
        db.session.commit()
        flash('修改成功')
    else:
        flash('原密码不正确')
    return redirect(url_for('user.homepage'))


@bp.route('/upload_avatar/', methods=['POST'])
def upload_avatar():
    f = request.files.get('file')
    if not os.path.isdir(f"static/images/avatar/"):
        os.mkdir(f"static/images/avatar/")
    # 时间戳后5位，随机数六位，用户id，组成文件名
    t = int(time.time()) % 100000
    randomstring = ''.join(random.sample(string.ascii_letters + string.digits, 6))
    last = os.path.splitext(f.filename)[-1]
    fname = f'{t}{randomstring}{g.user.id}{last}'
    user = UserModel.query.filter(UserModel.id == g.user.id).first()
    # 如果原本有图像，先删除
    # 文件路径   static前不能加 /
    if user.avatar and os.path.exists(f'static/images/avatar/{user.avatar}'):

        os.remove(f'static/images/avatar/{user.avatar}')
    user.avatar = fname
    db.session.commit()
    f.save(os.path.join(f"static/images/avatar/", fname))
    return ''


@bp.route('/chatlist/', methods=['GET'])
def chatlist():
    return render_template('chatlist.html', userid=g.user.id)


# ——————————————————————————————————商家——————————————————————————————————

@bp.route('/food_photo/', methods=['GET', 'POST'])
def upload_food_photo():
    if request.method == 'GET':
        return render_template('merchant/upload_food_photo.html')
    elif request.method == 'POST':
        f = request.files.get('file')
        food_id = request.form.get('food_id')
        if not os.path.isdir(f"static/images/food/"):
            os.mkdir(f"static/images/food/")
        last = os.path.splitext(f.filename)[-1]
        fname = f'{food_id}{last}'
        food = FoodModel.query.filter(FoodModel.id == food_id).first()
        if food.address and os.path.exists(f'static/images/food/{fname}'):
            os.remove(f'static/images/food/{fname}')
        food.address = fname
        db.session.commit()
        f.save(os.path.join(f"static/images/food/", fname))
        return redirect(url_for('user.homepage'))
