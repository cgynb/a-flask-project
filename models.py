from exts import db
from datetime import datetime


class EmailCaptchaModel(db.Model):
    __tablename__ = 'email_captcha'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    captcha = db.Column(db.String(100), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)


class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    # 1:顾客  2:商家  3:骑手
    role_id = db.Column(db.Integer)
    join_time = db.Column(db.DateTime, default=datetime.now)


class MerchantsModel(db.Model):
    __tablename__ = 'merchant'
    email = db.Column(db.String(100), db.ForeignKey("user.email"), primary_key=True)
    label = db.Column(db.String(30))


class FoodModel(db.Model):
    __tablename__ = 'food'
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    merchant_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    merchant_name = db.Column(db.String(100), db.ForeignKey('user.username'))
    food_price = db.Column(db.Integer)
    food_name = db.Column(db.String(50))
    food_desc = db.Column(db.Text)
    zans = db.Column(db.Integer, default=0)
    collects = db.Column(db.Integer, default=0)
    order_number = db.Column(db.Integer, default=0)


class OrderModel(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    arrive = db.Column(db.Boolean, default=False)
    merchant_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    merchant_take_order = db.Column(db.Boolean, default=False)
    rider_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    food_id = db.Column(db.Integer)
    food_price = db.Column(db.Integer, nullable=False)
    food_name = db.Column(db.String(50))
    rider_salary = db.Column(db.Integer, nullable=False)
    zan = db.Column(db.Boolean, default=False)
    order_date = db.Column(db.DateTime, default=datetime.now)


class CollectModel(db.Model):
    __tablename__ = 'collect'
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=False)


class FollowModel(db.Model):
    __tablename__ = 'follow'
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class CommentModel(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now)
