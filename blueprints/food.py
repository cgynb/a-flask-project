from flask import Blueprint, render_template
from require import login_required, merchant_required

bp = Blueprint('food', __name__, url_prefix='/')


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/food/')
@login_required
@merchant_required
def upload_food():
    return render_template('merchant/upload_food.html')


@bp.route('/shop/', methods=['GET'])
@login_required
def shop():
    return render_template('shop.html')
