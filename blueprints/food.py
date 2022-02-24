from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from sqlalchemy import and_, or_
from decorators import login_required, merchant_required
from forms import FoodForm
from exts import db
from models import (FoodModel,
                    UserModel,
                    MerchantsModel,
                    OrderModel,
                    CollectModel,
                    FollowModel,
                    CommentModel,)

bp = Blueprint('food', __name__, url_prefix='/')


@bp.route('/', methods=['GET'])
def index():
    keyword = request.args.get('keyword')
    page = int(request.args.get('page', default=1))
    if not keyword:
        per_page = 9
        # 总食物数量
        total_info = FoodModel.query.count()
        # 一面六个，总页面数
        total_page = total_info // per_page + 1
        if total_info % per_page == 0 and total_info != 0:
            total_page -= 1
        if page > total_page or page < 1:
            page = 1
            # 获取到：食物价格，食物名称，食物订单数，商家名
        foods = db.session.query(FoodModel.id, FoodModel.food_price, FoodModel.food_name,
                                 FoodModel.order_number, FoodModel.zans, UserModel.username). \
            filter(and_(UserModel.id == FoodModel.merchant_id, UserModel.role_id == 2)). \
            order_by(FoodModel.order_number.desc()).offset(per_page * (int(page) - 1)).limit(per_page).all()
        return render_template('index.html', foods=foods, total_page=total_page, current_page=page, info_num=len(foods))
    else:
        per_page = 9
        if page < 1:
            page = 1
        total_page = int(request.args.get('total_page'))
        if total_page:
            if page > total_page:
                page = 1
        foods = db.session.query(FoodModel.id, FoodModel.food_price, FoodModel.food_name,
                                 FoodModel.order_number, UserModel.username). \
            filter(and_(UserModel.id == FoodModel.merchant_id, UserModel.role_id == 2,
                        or_(FoodModel.food_name.contains(keyword), FoodModel.food_desc.contains(keyword)))).\
            order_by(FoodModel.order_number.desc()). \
            offset(per_page * (int(page) - 1)).limit(per_page).all()
        total_info = len(foods)
        total_page = total_info // per_page + 1
        if total_info % per_page == 0 and total_info != 0:
            total_page -= 1
        return render_template('index.html', foods=foods,keyword=keyword, total_page=total_page, current_page=page,
                               info_num=len(foods))


@bp.route('/food_details/')
@login_required
def food_details():
    food_id = request.args.get('id')
    food = FoodModel.query.filter(FoodModel.id == food_id).first()
    col = CollectModel.query.filter(and_(CollectModel.user_id == g.user.id, CollectModel.food_id == food_id)).first()
    food_comments = db.session.\
        query(CommentModel.comment, CommentModel.create_time, CommentModel.author_id, UserModel.username).\
        filter(and_(CommentModel.food_id == food_id, UserModel.id == CommentModel.author_id)).all()
    if col is None:
        collect_status = False
    else:
        collect_status = True
    f = FollowModel.query.\
        filter(and_(FollowModel.follower_id == g.user.id, FollowModel.followed_id == food.merchant_id)).first()
    if f:
        follow_status = True
    else:
        follow_status = False
    return render_template('food_details.html', food=food, collect_status=collect_status, follow_status=follow_status,
                           food_comments=food_comments)


@bp.route('/comment/', methods=['POST'])
def comment():
    food_id = request.form.get('food_id')
    food_comment = request.form.get('comment')
    new_comment = CommentModel(food_id=food_id, author_id=g.user.id, comment=food_comment)
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for('food.food_details') + f'?id={food_id}')


@bp.route('/merchant_classify/')
def merchant_classify():
    return render_template('merchant_classify.html')


@bp.route('/merchant_list/')
def merchant_list():
    per_page = 5
    page = int(request.args.get('page', default=1))
    keyword = request.args.get('keyword')
    if not keyword:
        # 总商家数量
        total_info = MerchantsModel.query.count()
        # 一面5个，总页面数
        total_page = total_info // per_page + 1
        if page > total_page or page < 1:
            page = 1
        label = request.args.get('label')
        merchants = db.session.query(UserModel.id, MerchantsModel.label, UserModel.username, UserModel.join_time). \
            filter(and_(MerchantsModel.label == label, MerchantsModel.email == UserModel.email)). \
            offset(per_page * (int(page) - 1)).limit(per_page).all()
    else:
        merchants = db.session.query(UserModel.id, MerchantsModel.label, UserModel.username, UserModel.join_time). \
            filter(and_(UserModel.username.contains(keyword), MerchantsModel.email == UserModel.email)). \
            offset(per_page * (int(page) - 1)).limit(per_page).all()
        label = ''
        total_page = len(merchants) // per_page + 1
        if page > total_page or page < 1:
            page = 1
    return render_template('merchant_list.html', label=label, merchants=merchants, total_page=total_page,
                           current_page=page, info_num=len(merchants))


@bp.route('/merchant_homepage/')
def merchant_homepage():
    _id = request.args.get('id')
    merchant = db.session.query(MerchantsModel.label, UserModel.username, UserModel.email, UserModel.id). \
        filter(UserModel.id == _id).first()
    merchant_name = merchant.username
    foods = db.session.query(FoodModel.food_name, FoodModel.food_price, FoodModel.id). \
        filter(FoodModel.merchant_name == merchant_name).all()
    f = FollowModel.query.filter(and_(FollowModel.follower_id == g.user.id, FollowModel.followed_id == _id)).first()
    if f:
        follow_status = True
    else:
        follow_status = False
    return render_template('merchant_homepage.html', merchant=merchant, foods=foods, follow_status=follow_status)


@bp.route('/get_food/', methods=['POST'])
@login_required
def get_food():
    merchant_id = request.form.get('merchant_id')
    food_price = request.form.get('food_price')
    food_id = request.form.get('food_id')
    food_name = request.form.get('food_name')
    customer_id = request.form.get('customer_id')
    rider_salary = request.form.get('rider_salary')
    order = OrderModel(food_price=food_price, food_id=food_id, customer_id=customer_id,
                       merchant_id=merchant_id, rider_salary=rider_salary, food_name=food_name)
    db.session.add(order)
    food = FoodModel.query.filter(FoodModel.id == food_id).first()
    food.order_number += 1
    db.session.commit()
    return redirect(url_for('user.view_order'))


@bp.route('/zan/')
def zan():
    order_id = request.args.get('order_id')
    order = OrderModel.query.filter(OrderModel.id == order_id).first()
    order.zan = not order.zan
    food = FoodModel.query.filter(FoodModel.id == order.food_id).first()
    food.zans += int(order.zan)
    db.session.commit()
    return redirect(url_for('user.bill'))


@bp.route('/collect/')
def collect():
    _id = request.args.get('id')
    user_id = g.user.id
    col = CollectModel.query.filter(and_(CollectModel.food_id == _id, CollectModel.user_id == user_id)).first()
    if col is None:
        col = CollectModel(food_id=_id, user_id=user_id)
        db.session.add(col)
        db.session.commit()
    else:
        db.session.delete(col)
        db.session.commit()
    return redirect(url_for('food.food_details') + f'?id={_id}')


# ————————————————————————————————————————————商家特有——————————————————————————————————————————————————————————————————
@bp.route('/upload_food/', methods=['GET', 'POST'])
@login_required
@merchant_required
def upload_food():
    if request.method == 'GET':
        return render_template('merchant/upload_food.html')
    else:
        form = FoodForm(request.form)
        if form.validate():
            food_price = form.food_price.data
            food_name = form.food_name.data
            food_desc = form.food_desc.data
            food = FoodModel(merchant_id=g.user.id, food_price=food_price, food_name=food_name,
                             food_desc=food_desc, merchant_name=g.user.username)
            db.session.add(food)
            db.session.commit()
            return redirect(url_for('food.index'))
        else:
            flash('食品描述多写一写哟[无语]')
            return redirect(url_for('food.upload_food'))


@bp.route('/delete_food/', methods=['POST'])
@login_required
@merchant_required
def delete_food():
    _id = request.form.get('id')
    food = FoodModel.query.filter(FoodModel.id == _id).first()
    if food is not None and g.user.email == food.merchants_email:
        db.session.delete(food)
        db.session.commit()
    else:
        flash('输入id错误')
    return redirect(url_for('user.homepage'))
