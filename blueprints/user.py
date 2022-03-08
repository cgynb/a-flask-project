from datetime import datetime
from flask import (Blueprint,
                   redirect,
                   render_template,
                   request,
                   url_for,
                   jsonify,
                   session,
                   flash,
                   g)
from flask_mail import Message
from sqlalchemy import and_
from werkzeug.security import generate_password_hash, check_password_hash
from exts import mail, db
from models import EmailCaptchaModel, UserModel, MerchantsModel, FoodModel, OrderModel, CollectModel, FollowModel
import string
import random
from forms import RegisterForm, LoginForm, ChangePassForm
from decorators import login_required, merchant_required, rider_required
import os

bp = Blueprint('user', __name__, url_prefix='/user')


# ————————————————————————————————————————————通用——————————————————————————————————————————————————————————————————————
# 登录
@bp.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            #                               数据库里的加密密码 和 登录密码 进行比对
            if user and check_password_hash(user.password, password):
                session['username'] = user.username
                session['user_id'] = user.id
                session['role_id'] = user.role_id
                return redirect('/')
            else:
                flash('邮箱和密码不匹配')
                return redirect(url_for('user.login'))
        else:
            flash('邮箱或密码格式错误')
            return redirect(url_for('user.login'))


# 退出登录：删除session即可
@bp.route("/logout/")
def logout():
    # 清除session中所有数据
    session.clear()
    return redirect(url_for("user.login"))


# 注册
@bp.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            role_id = form.role_id.data
            # 这里密码加密
            hash_password = generate_password_hash(password)
            user = UserModel(email=email, username=username, password=hash_password, role_id=role_id)
            db.session.add(user)
            db.session.commit()
            if role_id == '2':
                merchant = MerchantsModel(email=email, label='早餐')
                db.session.add(merchant)
                db.session.commit()
            return redirect(url_for('user.login'))
        else:
            return redirect(url_for('user.register'))
    else:
        return render_template('register.html')


# 邮箱验证码
@bp.route('/captcha/', methods=['POST'])
def get_catpcha():
    email = request.form.get('email')
    try:
        if email:
            s = string.ascii_letters + string.digits
            captcha = ''.join(random.sample(s, 4))
            message = Message(
                subject='验证码',
                recipients=[email],
                body=f'验证码是：{captcha}',
            )
            mail.send(message)
            captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
            if captcha_model:
                captcha_model.captcha = captcha
                captcha_model.create_time = datetime.now()
                db.session.commit()
            else:
                captcha_model = EmailCaptchaModel(email=email, captcha=captcha)
                db.session.add(captcha_model)
                db.session.commit()
            return jsonify({'code': 200, 'message': 'success'})
        else:
            return jsonify({'code': 400, 'message': '请传递邮箱'})
    except:
        return jsonify({'code': 400, 'message': '邮箱格式错误'})


@bp.route('/homepage/')
@login_required
def homepage():
    if g.role == '商家':
        foods = db.session.query(FoodModel.food_name, FoodModel.food_price, FoodModel.id). \
            filter(FoodModel.merchant_id == g.user.id).all()
        orders = OrderModel.query.filter(OrderModel.merchant_id == g.user.id).all()
        total_earn = 0
        total_consumn = 0
        total_number = len(orders)
        for order in orders:
            total_earn += order.food_price - order.rider_salary
            total_consumn += order.food_price
        return render_template('homepage.html', foods=foods, merchant_name=g.user.username,
                               total_number=total_number, total_earn=total_earn, total_consumn=total_consumn)
    elif g.role == '顾客':
        total_consumn = 0
        orders = OrderModel.query.filter(OrderModel.customer_id == g.user.id).all()
        for order in orders:
            total_consumn += order.food_price
        return render_template('homepage.html', total_consumn=total_consumn)
    else:
        total_earn = 0
        total_consumn = 0
        orders = OrderModel.query.filter(OrderModel.customer_id == g.user.id).all()
        for order in orders:
            total_consumn += order.food_price
        orders = OrderModel.query.filter(OrderModel.rider_id == g.user.id).all()
        total_order = len(orders)
        for order in orders:
            total_earn += order.rider_salary
        return render_template('homepage.html', total_order=total_order, total_earn=total_earn,
                               total_consumn=total_consumn)


@bp.route('/change_username/', methods=['POST'])
@login_required
def change_username():
    username = request.form.get('username')
    user = UserModel.query.filter(UserModel.username == g.user.username).first()
    try:
        user.username = username
        db.session.commit()
    except:
        # 这里用js弹出alert("已有此用户名，请换一个")
        pass
    return redirect(url_for('user.homepage'))


@bp.route('/change_password/', methods=['GET', 'POST'])
def change_password():
    if request.method == 'GET':
        return render_template('change_password.html')
    else:
        form = ChangePassForm(request.form)
        if form.validate():
            new_password = form.new_password.data
            new_password = generate_password_hash(new_password)
            user = UserModel.query.filter(UserModel.id == g.user.id).first()
            user.password = new_password
            db.session.commit()
        return redirect(url_for('user.homepage'))


@bp.route('/bill/')
@login_required
def bill():
    bills = OrderModel.query. \
        filter(and_(g.user.id == OrderModel.customer_id, OrderModel.arrive == True)). \
        order_by(OrderModel.order_date.desc()).all()
    return render_template('bill.html', bills=bills)


@bp.route('/arrive/', methods=['GET'])
@login_required
def arrive():
    order_id = request.args.get('id')
    order = OrderModel.query.filter(OrderModel.id == order_id).first()
    order.arrive = True
    db.session.commit()
    return redirect(url_for('user.view_order'))


@bp.route('/order/')
@login_required
def view_order():
    orders = db.session. \
        query(OrderModel.food_name, OrderModel.id, OrderModel.merchant_take_order, OrderModel.order_date,
              OrderModel.rider_id, OrderModel.arrive). \
        filter(and_(OrderModel.customer_id == g.user.id, OrderModel.arrive == False)).all()
    return render_template('view_order.html', orders=orders, order_num=len(orders))


@bp.route('/collection/')
def collection():
    collections = db.session. \
        query(CollectModel.user_id, CollectModel.food_id, FoodModel.food_name, FoodModel.food_price). \
        filter(and_(CollectModel.user_id == g.user.id, FoodModel.id == CollectModel.food_id)).all()
    return render_template('colletion.html', collections=collections)


@bp.route('/follow/', methods=['POST'])
@login_required
def follow():
    follower_id = g.user.id
    followed_id = request.form.get('followed_id')
    f = FollowModel.query. \
        filter(and_(FollowModel.follower_id == follower_id, FollowModel.followed_id == followed_id)).first()
    if f:
        db.session.delete(f)
        db.session.commit()
    else:
        f = FollowModel(follower_id=follower_id, followed_id=followed_id)
        db.session.add(f)
        db.session.commit()
    return redirect(url_for('food.index'))


@bp.route('/follow_list/')
@login_required
def follow_list():
    merchants = db.session.query(FollowModel.followed_id, UserModel.username). \
        filter(and_(FollowModel.follower_id == g.user.id, UserModel.id == FollowModel.followed_id)).all()
    return render_template('follow_list.html', merchants=merchants)


@bp.route('/upload_avatar/', methods=['GET', 'POST'])
def upload_avatar():
    if request.method == 'GET':
        return render_template('upload_avatar.html')
    else:
        f = request.files.get('file')
        if not os.path.isdir(f"static/images/avatar/"):
            os.mkdir(f"static/images/avatar/")
        f.save(os.path.join(f"static/images/avatar/", f'{g.user.id}.png'))  # 保存文件
        return ''


# ————————————————————————————————————————————商家特有——————————————————————————————————————————————————————————————————
@bp.route('/update_label', methods=['POST'])
@login_required
@merchant_required
def update_label():
    label = request.form.get('label')
    merchant = MerchantsModel.query.filter(g.user.email == MerchantsModel.email).first()
    merchant.label = label
    db.session.commit()
    return redirect(url_for('user.homepage'))


@bp.route('/merchant_take_order/', methods=['GET'])
@login_required
@merchant_required
def merchant_take_order():
    order_id = request.args.get('id')
    if order_id:
        order = OrderModel.query.filter(OrderModel.id == order_id).first()
        order.merchant_take_order = True
        db.session.commit()

    orders = OrderModel.query. \
        filter(and_(g.user.id == OrderModel.merchant_id, OrderModel.merchant_take_order == False)).all()
    return render_template('merchant/merchant_take_order.html', orders=orders)


@bp.route('/upload_food_photo/', methods=['GET', 'POST'])
def upload_food_photo():
    if request.method == 'GET':
        food_id = request.args.get('id')
        if not os.path.isdir(f"static/images/food/{food_id}"):
            os.mkdir(f"static/images/food/{food_id}")
        if len(os.listdir(f'static/images/food/{food_id}')) == 1:
            # 这里弹出不能在放图片啦
            return redirect(url_for('user.homepage'))
        food = FoodModel.query.filter(FoodModel.id == food_id).first()
        if food:
            session['food_upload_photo_id'] = food_id
            return render_template('merchant/upload_food_photo.html')
        else:
            # 这里js弹出没有这个食物
            return redirect(url_for('user.homepage'))
    else:
        food_id = session.get('food_upload_photo_id')
        session['food_upload_photo_id'] = False
        if len(os.listdir(f'static/images/food/{food_id}')) == 1:
            # 这里弹出不能在放图片啦
            return redirect(url_for('user.homepage'))
        f = request.files.get('file')
        f.save(os.path.join(f"static/images/food/{food_id}", f"{food_id}.png"))  # 保存文件
        return ''


# ————————————————————————————————————————————骑手特有——————————————————————————————————————————————————————————————————
@bp.route('/take_order/')
@login_required
@rider_required
def take_order():
    if request.args.get('id') is None:
        #                                   注意这里筛选的是用  is_(None)
        orders = OrderModel.query.filter(and_(OrderModel.rider_id.is_(None), OrderModel.merchant_take_order == True)). \
            order_by(OrderModel.rider_salary.desc()).all()
        return render_template('rider/take_order.html', orders=orders)
    else:
        _id = request.args.get('id')
        order = OrderModel.query.filter(OrderModel.id == _id).first()
        order.rider_id = g.user.id
        db.session.commit()
        orders = OrderModel.query.filter(OrderModel.rider_id.is_(None)).order_by(OrderModel.rider_salary.desc()).all()
        return render_template('rider/take_order.html', orders=orders)


@bp.route('/history_order/')
@login_required
@rider_required
def history_order():
    orders = OrderModel.query.filter(OrderModel.rider_id == g.user.id).order_by(OrderModel.order_date.desc()).all()
    return render_template('rider/history_order.html', orders=orders)
