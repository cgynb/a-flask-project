from flask import Blueprint, render_template, request, redirect, url_for, g, flash
from models import FoodModel
from exts import db
from require import login_required, merchant_required

bp = Blueprint('food', __name__, url_prefix='/')


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/food/', methods=['GET', 'POST'])
@login_required
@merchant_required
def upload_food():
    if request.method == 'GET':
        return render_template('merchant/upload_food.html')
    elif request.method == 'POST':
        form = request.form
        try:
            food = FoodModel(merchant_id=g.user.id, merchant_name=g.user.username, food_name=form.get('foodname')
                             , food_price=form.get('foodprice'), food_desc=form.get('fooddesc'))
            db.session.add(food)
            db.session.commit()
            flash('上传成功')
            return redirect(url_for('food.index'))
        except Exception as e:
            print(e)
            flash('上传失败')
            return redirect(url_for('food.upload_food'))


@bp.route('/shop/', methods=['GET'])
@login_required
def shop():
    return render_template('shop.html')
