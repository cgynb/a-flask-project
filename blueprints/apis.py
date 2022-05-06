import json
import os
import random
import string
import time
import datetime

from flask import Blueprint, jsonify, g, request
from sqlalchemy import and_, or_

from require import login_required
from data import orderConbinition, turn_userid_to_name
from exts import db
from models import TagModel, UserModel, FoodModel, OrderModel, FollowModel, CommentModel,\
    SubcommentModel, MessageModel, NoticeModel

bp = Blueprint('apis', __name__, url_prefix='/elebu/api/v1/')


@bp.route('/tag/', methods=['GET', 'POST', 'DELETE'])
@login_required
def tag():
    if request.method == 'GET':
        try:
            tags = TagModel.query.filter(TagModel.user_id == g.user.id).all()
            data = []
            for t in tags:
                t = {'tag': t.t}
                data.append(t)
            return jsonify({'status': 200, 'message': 'success', 'data': data})
        except:
            return jsonify({'status': 400, 'message': 'database error'})
    elif request.method == 'POST':
        try:
            gettag = request.form.get('tag')
            if gettag:
                t = TagModel(user_id=g.user.id, t=gettag)
                user = UserModel.query.filter(UserModel.id == g.user.id).first()
                user.audit = False
                db.session.add(t)
                db.session.commit()
                return jsonify({'status': 200, 'message': 'success'})
            else:
                return jsonify({'status': 400, 'message': 'please enter a tag'})
        except:
            return jsonify({'status': 400, 'message': 'database error'})
    elif request.method == 'DELETE':
        try:
            deltag = request.form.get('tag')
            t = TagModel.query.filter(and_(TagModel.t == deltag, TagModel.user_id == g.user.id)).first()
            if t:
                db.session.delete(t)
                db.session.commit()
                return jsonify({'status': 200, 'message': 'success'})
            else:
                return jsonify({'status': 400, 'message': 'there is no such tag'})
        except:
            return jsonify({'status': 400, 'message': 'database error'})


# num: self, one, merchant, all
# num=self: 这是获取自己的信息
# num=one: 获取一个商家的头像，店名，介绍
# num=merchant: 获取大量商家信息, 可以通过keyword, tag_进行筛选，否则面向全部商家
# num=all: 这是管理员进行操作时获取所有没有通过审核的商家
@bp.route('/selfinfo/', methods=['GET', 'PUT', 'DELETE'])
def selfInfo():
    if request.method == 'GET':
        if request.args.get('num') == 'self':
            user = db.session.query(UserModel.username, UserModel.role, UserModel.avatar,
                                    UserModel.join_time, UserModel.selfintroduce, UserModel.avatar) \
                .filter(UserModel.id == g.user.id).first()
            return jsonify({'status': 200,
                            'message': 'success',
                            'user_id': g.user.id,
                            'username': user.username,
                            'role': user.role,
                            'join_time': user.join_time,
                            'avatar': user.avatar,
                            'selfintroduce': user.selfintroduce})
        elif request.args.get('num') == 'one' and request.args.get('merchant_id'):
            user = UserModel.query.filter(UserModel.id == request.args.get('merchant_id')).first()
            return jsonify({'status': 200, 'message': 'success', 'avatar': user.avatar, 'username': user.username, 'selfintroduce': user.selfintroduce})
        elif request.args.get('num') == 'merchant':
            keyword = request.args.get('keyword')
            tag_ = request.args.get('tag')
            # print(keyword)
            merchantlist = []
            per_page = 4
            page = int(request.args.get('page', default=1))
            if keyword:
                merchants = UserModel.query.filter(and_(UserModel.role == 2, UserModel.username.contains(keyword))). \
                    offset(per_page * (int(page) - 1)).limit(per_page).all()
                total_info = UserModel.query.filter(
                    and_(UserModel.role == 2, UserModel.username.contains(keyword))).count()
                total_page = total_info // 4
                if total_info % 4:
                    total_page += 1
            elif tag_ != 'null':
                merchants = db.session.query(UserModel.id, UserModel.username, UserModel.email, UserModel.selfintroduce,
                                             UserModel.avatar, TagModel.t). \
                    filter(and_(UserModel.role == 2, TagModel.user_id == UserModel.id, TagModel.t.contains(tag_))). \
                    offset(per_page * (int(page) - 1)).limit(per_page).all()
                total_info = db.session.query(UserModel.id, UserModel.username, UserModel.email,
                                              UserModel.selfintroduce, UserModel.avatar, TagModel.t). \
                    filter(and_(UserModel.role == 2, TagModel.user_id == UserModel.id, TagModel.t.contains(tag_))). \
                    count()
                total_page = total_info // 4
                if total_info % 4:
                    total_page += 1
            else:
                total_info = UserModel.query.filter(UserModel.role == 2).count()
                total_page = total_info // 4
                if total_info % 4:
                    total_page += 1
                merchants = UserModel.query.filter(and_(UserModel.role == 2)). \
                    offset(per_page * (int(page) - 1)).limit(per_page).all()

            for m in merchants:
                tags = [t.t for t in TagModel.query.filter(TagModel.user_id == m.id).all()]
                merchant = {'merchant_id': m.id, 'username': m.username, 'avatar': m.avatar,
                            'introduce': m.selfintroduce, 'tags': tags}
                merchantlist.append(merchant)
            return jsonify({'status': 200, 'message': 'success', 'page': page, 'total_page': total_page, 'merchants': merchantlist})
        elif request.args.get('num') == 'all':
            if g.user.role == 4:
                info = []
                users = UserModel.query.filter(UserModel.audit == False).all()
                for user in users:
                    tags = [t.t for t in TagModel.query.filter(TagModel.user_id == user.id).all()]
                    info.append({'username': user.username, 'email': user.email, 'selfintroduce': user.selfintroduce,
                                 'userid': user.id, 'avatar': user.avatar, 'tags': tags})
                return jsonify({'status': 200, 'message': 'success', 'info': info})
            else:
                return jsonify({'status': 403, 'message': 'forbid'})
        else:
            return jsonify({'status': 400, 'message': 'parameters error'})
    elif request.method == 'PUT':
        user_id = request.form.get('user_id')
        selfintroduce = request.form.get('selfintroduce')
        if request.form.get('pass') == 'pass' and user_id:
            user = UserModel.query.filter(UserModel.id == user_id).first()
            user.audit = True
            db.session.commit()
            return jsonify({'status': 200, 'message': 'success'})
        elif selfintroduce:
            try:
                user = UserModel.query.filter(UserModel.id == g.user.id).first()
                user.selfintroduce = selfintroduce.replace('<', '&lt;').replace('>', '&gt;').replace(' ', '&nbsp;').\
                    replace('\n', '<br>')
                user.audit = False
                db.session.commit()
                return jsonify({'status': 200, 'message': 'success'})
            except Exception as e:
                print(e)
                return jsonify({'status': 400, 'message': 'database error'})
        else:
            return jsonify({'status': 400, 'message': 'parameters error'})
    elif request.method == 'DELETE':
        del_thing = request.form.get('del_thing')
        del_thing_detail = request.form.get('del_thing_detail')  # 如果是图片需要得到图片文件名，标签需要确切定位那个标签
        user_id = request.form.get('user_id')
        print(del_thing_detail)
        if del_thing in ('avatar', 'selfintroduce', 'tag', 'username') and str(user_id).isdigit():
            try:
                if del_thing == 'avatar':
                    user = UserModel.query.filter(UserModel.id == user_id).first()
                    if del_thing_detail == '/static/images/1.jpg':
                        return jsonify({'status': 404, 'message': 'no avatar'})
                    else:
                        os.remove(f'{del_thing_detail[1:]}')
                        user.avatar = None
                elif del_thing == 'selfintroduce':
                    user = UserModel.query.filter(UserModel.id == user_id).first()
                    user.selfintroduce = None
                elif del_thing == 'tag':
                    t = TagModel.query.filter(and_(TagModel.user_id == user_id, TagModel.t == del_thing_detail)).first()
                    db.session.delete(t)
                elif del_thing == 'username':
                    user = UserModel.query.filter(UserModel.id == user_id).first()
                    user.username = 'sb赶快改名' + str(time.time())
                db.session.commit()
                return jsonify({'status': 200, 'message': 'success'})
            except:
                return jsonify({'status': 400, 'message': 'database error'})
        else:
            return jsonify({'status': 400, 'message': 'parameters error'})


@bp.route('/food/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def foodInfo():
    if request.method == 'GET':
        info = []
        num = request.args.get('num')
        merchant_id = request.args.get('merchant_id')
        try:
            if num == 'self':
                foods = FoodModel.query. \
                    filter(FoodModel.merchant_id == g.user.id).all()
                for food in foods:
                    f = {'food_id': food.id, 'food_name': food.food_name, 'food_price': food.food_price,
                         'food_desc': food.food_desc, 'zans': food.zans, 'address': food.address}
                    info.append(f)
            elif str(merchant_id).isdigit():
                foods = FoodModel.query. \
                    filter(FoodModel.merchant_id == merchant_id).all()
                for food in foods:
                    f = {'food_id': food.id, 'food_name': food.food_name, 'food_price': food.food_price,
                         'food_desc': food.food_desc, 'zans': food.zans, 'address': food.address}
                    info.append(f)
            elif num == 'all':
                foods = FoodModel.query.filter(FoodModel.audit == False).order_by(FoodModel.id.desc()).all()
                for food in foods:
                    f = {'foodid': food.id, 'foodprice': food.food_price, 'foodname': food.food_name,
                         'fooddesc': food.food_desc, 'zans': food.zans, 'ordernum': food.order_number,
                         'merchantid': food.merchant_id, 'merchantname': turn_userid_to_name(food.merchant_id),
                         'photo': food.address}
                    info.append(f)
            else:
                return jsonify({'status': 400, 'message': 'parameters error'})
            return jsonify({'status': 200, 'message': 'success', 'info': info})
        except:
            return jsonify({'status': 400, 'message': 'database error'})
    elif request.method == 'POST':
        foodname = request.form.get('foodname')
        foodprice = request.form.get('foodprice')
        fooddesc = request.form.get('fooddesc')
        try:
            if foodname and str(foodprice).isdigit() and fooddesc:
                food = FoodModel(merchant_id=g.user.id, food_name=foodname
                                 , food_price=foodprice, food_desc=fooddesc)
                db.session.add(food)
                db.session.commit()
            else:
                return jsonify({'status': 400, 'message': 'parameters error'})
        except Exception as e:
            print(e)
            return jsonify({'status': 400, 'message': 'database error'})
        return jsonify({'status': 200, 'message': 'success'})
    elif request.method == 'PUT':
        food_id = request.form.get('food_id')
        if request.form.get('pass') == 'pass' and str(food_id).isdigit() and g.user.role == 4:
            try:
                food = FoodModel.query.filter(FoodModel.id == food_id).first()
                food.audit = True
                db.session.commit()
                return jsonify({'status': 200, 'message': 'success'})
            except:
                return jsonify({'status': 400, 'message': 'database error'})
        return jsonify({'status': 400, 'message': 'parameters error'})
    elif request.method == 'DELETE':
        food_id = request.form.get('food_id')
        del_thing = request.form.get('del_thing')
        if food_id and g.user.role == 2:
            try:
                food = FoodModel.query.filter(and_(FoodModel.merchant_id == g.user.id, FoodModel.id == food_id)).first()
                if food:
                    OrderModel.query.filter(OrderModel.food_id == food_id).delete()
                    db.session.delete(food)
                    db.session.commit()
                else:
                    return jsonify({'status': 403, 'message': 'the food is not yours'})
                return jsonify({'status': 200, 'message': 'success'})
            except Exception as e:
                print(e)
                return jsonify({'status': 400, 'message': 'database error'})
        elif food_id and g.user.role == 4 and del_thing in ('photo', 'foodname', 'fooddesc'):
            food = FoodModel.query.filter(FoodModel.id == food_id).first()
            if del_thing == 'photo':
                if food.address is not None:
                    os.remove(f'static/images/food/{food.address}')
                food.address = None
            elif del_thing == 'foodname':
                food.food_name = str(time.time()) + 'sbbb商品赶紧改名！！！'
            elif del_thing == 'fooddesc':
                food.food_desc = str(time.time())[::-1] + 'sbb赶紧改商品名！！！'
            db.session.commit()
            return jsonify({'status': 200, 'message': 'success'})
        else:
            return jsonify({'status': 400, 'message': 'parameters error'})


@bp.route('/order/', methods=['GET', 'POST', 'PUT'])
def orderInfo():
    if request.method == 'GET':
        info = []
        if request.args.get('user') and request.args.get('arrive'):
            order_list = OrderModel.query.filter(
                and_(OrderModel.customer_id == g.user.id, OrderModel.arrive == True)).order_by(
                OrderModel.order_date.desc()).all()
            for order in order_list:
                o = {'order_date': order.order_date,
                     'food_price': order.food_price, 'food_name': order.food_name,
                     'food_count': order.food_count, 'food_id': order.food_id,
                     'zan': order.zan, 'order_id': order.order_id}
                info.append(o)
        else:
            user_id = request.args.get('user_id')
            if request.args.get('role') == 'customer':
                order_list = OrderModel.query.filter(OrderModel.customer_id == user_id).all()
            elif request.args.get('role') == 'merchant':
                order_list = OrderModel.query.filter(
                    and_(OrderModel.merchant_id == user_id, OrderModel.merchant_take_order == False)).all()
            elif request.args.get('role') == 'rider':
                order_list = OrderModel.query.filter(and_(OrderModel.merchant_take_order == True)).all()
            for order in order_list:
                o = {'customer_id': order.customer_id, 'arrive': order.arrive,
                     'merchant_id': order.merchant_id, 'merchant_take_order': order.merchant_take_order,
                     'rider_id': order.rider_id, 'rider_salary': order.rider_salary,
                     'food_id': order.food_id, 'food_price': order.food_price, 'food_name': order.food_name,
                     'food_count': order.food_count,
                     'zan': order.zan, 'order_id': order.order_id}
                info.append(o)
            info = orderConbinition(info)
        return jsonify({'status': 200, 'message': 'success', 'info': info})
    elif request.method == 'POST':
        # 由于一次订单，会有多个菜品，所以，一行是写不完全的，所以需要有多行数据储存一次的订单，
        # 于是自增的主键不能表示一次订单了，这里构建新的订单号，以识别一次订单
        # 取时间戳后7位乘3，然后6位随机字符串，然后用户id
        order_id = str(int(time.time()) % 10000000 * 3) + \
                   ''.join(random.sample(string.ascii_letters + string.digits, 6)) + str(g.user.id)
        datas = json.loads(request.form.get('data'))
        try:
            for data in datas:
                food_name = data['food_name']
                food_price = data['food_price']
                food_id = data['food_id']
                food_count = data['food_count']
                customer_id = g.user.id
                merchant_id = data['merchant_id']
                order = OrderModel(customer_id=customer_id, merchant_id=merchant_id, food_id=food_id, food_name=food_name,
                                   food_price=food_price, food_count=food_count, order_id=order_id)
                db.session.add(order)
            db.session.commit()
        except:
            return jsonify({'status': 400, 'message': 'database error'})
        return jsonify({'status': 200, 'message': 'success'})
    elif request.method == 'PUT':
        order_id = request.form.get('order_id')
        rider_salary = request.form.get('rider_salary')
        arrive = request.form.get('arrive')
        try:
            if order_id:
                if rider_salary:  # 商家接单
                    orders = OrderModel.query.filter(OrderModel.order_id == order_id).all()
                    for order in orders:
                        order.merchant_take_order = True
                        order.rider_salary = float(rider_salary)
                    db.session.commit()
                elif arrive == 'arrive':  # 确认送达
                    orders = OrderModel.query.filter(OrderModel.order_id == order_id).all()
                    for order in orders:
                        order.arrive = True
                    db.session.commit()
                else:  # 骑手接单
                    orders = OrderModel.query.filter(OrderModel.order_id == order_id).all()
                    for order in orders:
                        order.rider_id = g.user.id
                    db.session.commit()
            else:
                return jsonify({'status': 400, 'message': 'parameters error'})
        except:
            return jsonify({'status': 400, 'message': 'database error'})
        return jsonify({'status': 200, 'message': 'success'})


@bp.route('/zan/', methods=['PUT'])
def Zan():
    order_id = request.form.get('order_id')
    zan = request.form.get('zan')
    food_id = request.form.get('food_id')
    if food_id and zan and order_id:
        try:
            food = FoodModel.query.filter(FoodModel.id == food_id).first()
            order = OrderModel.query.filter(
                and_(OrderModel.order_id == order_id, OrderModel.food_id == food_id)).first()
            if food is None:
                return jsonify({'status': 404, 'message': 'food not found'})
            if order is None:
                return jsonify({'status': 404, 'message': 'order not found'})
            if zan == 'zaned':
                if order.zan is True:
                    food.zans -= 1
                order.zan = False
            elif zan == 'tozan':
                if order.zan is False:
                    food.zans += 1
                order.zan = True
            else:
                return jsonify({'status': 400, 'message': 'parameters error'})
            db.session.commit()
            return jsonify({'status': 200, 'message': 'success'})
        except:
            return jsonify({'status': 400, 'message': 'database error'})
    else:
        return jsonify({'status': 400, 'message': 'lose some parameters'})


@bp.route('/follow/', methods=['GET', 'POST', 'DELETE'])
def follow():
    if request.method == 'GET':
        follow_list = request.args.get('follow_list')
        followed_id = request.args.get('followed_id')
        merchant_id = request.args.get('merchant_id')
        if follow_list == 'follow_list':
            info = []
            fs = db.session. \
                query(FollowModel.followed_id, UserModel.username, UserModel.avatar, UserModel.selfintroduce) \
                .filter(and_(FollowModel.follower_id == g.user.id, UserModel.id == FollowModel.followed_id)).all()
            for f in fs:
                data = {'merchant_id': f.followed_id, 'merchant_name': f.username, 'merchant_avatar': f.avatar,
                        'merchant_introduce': f.selfintroduce}
                info.append(data)
            return jsonify({'status': 200, 'message': 'success', 'info': info})
        elif followed_id:  # 查看自己是否关注
            follower_id = g.user.id
            try:
                f = FollowModel.query.filter(
                    and_(FollowModel.followed_id == followed_id, FollowModel.follower_id == follower_id)).first()
                if f:
                    return jsonify({'status': 200, 'message': 'success', 'info': 'followed'})
                else:
                    return jsonify({'status': 200, 'message': 'success', 'info': 'tofollow'})
            except:
                return jsonify({'status': 400, 'message': 'database error'})
        elif merchant_id:  # 获取商家关注数
            cnt = FollowModel.query.filter(FollowModel.followed_id == merchant_id).count()
            return jsonify({'status': 200, 'message': 'success', 'follow-num': cnt})
        else:
            return jsonify({'status': 400, 'message': 'parameters error'})
    elif request.method == 'POST':
        followed_id = request.form.get('followed_id')
        follower_id = g.user.id
        try:
            f = FollowModel.query.filter(
                and_(FollowModel.followed_id == followed_id, FollowModel.follower_id == follower_id)).first()
            if f is None:
                f = FollowModel(follower_id=follower_id, followed_id=followed_id)
                db.session.add(f)
                db.session.commit()
                return jsonify({'status': 200, 'message': 'success'})
            else:
                return jsonify({'status': 403, 'message': 'you have followed'})
        except:
            return jsonify({'status': 400, 'message': 'database error'})
    elif request.method == 'DELETE':
        followed_id = request.form.get('followed_id')
        try:
            f = FollowModel.query.filter(
                and_(FollowModel.followed_id == followed_id, FollowModel.follower_id == g.user.id)).first()
            if f is not None:
                db.session.delete(f)
                db.session.commit()
                return jsonify({'status': 200, 'message': 'success'})
            else:
                return jsonify({'status': 403, 'message': "you haven't followed"})
        except:
            return jsonify({'status': 400, 'message': 'database error'})
    return jsonify({'status': 200, 'message': 'success'})


@bp.route('/comment/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def comment():
    if request.method == 'GET':
        info = []
        if request.args.get('num') != 'all' and str(request.args.get('merchant_id')).isdigit():
            merchant_id = request.args.get('merchant_id')
            comments = db.session. \
                query(UserModel.username, UserModel.avatar, CommentModel.comment, CommentModel.id). \
                filter(and_(CommentModel.merchant_id == merchant_id, UserModel.id == CommentModel.user_id)). \
                order_by(CommentModel.id.desc()).all()
            for c in comments:
                subcomments = db.session.query(SubcommentModel.id, SubcommentModel.comment, UserModel.username,
                                               UserModel.avatar). \
                    filter(and_(SubcommentModel.sub == c.id, UserModel.id == SubcommentModel.user_id)). \
                    order_by(SubcommentModel.id.desc()).all()
                subs = []
                for sub in subcomments:
                    subs.append(
                        {'subid': sub.id, 'username': sub.username, 'useravatar': sub.avatar, 'reply': sub.comment})
                info.append({'username': c.username, 'useravatar': c.avatar, 'commentid': c.id, 'comment': c.comment,
                             'replies': subs})
        elif request.args.get('num') == 'all':
            comments = db.session. \
                query(UserModel.username, UserModel.avatar, CommentModel.comment, CommentModel.id, CommentModel.audit). \
                filter(UserModel.id == CommentModel.user_id). \
                order_by(CommentModel.id.desc()).all()
            for c in comments:
                subcomments = db.session.query(SubcommentModel.id, SubcommentModel.comment, UserModel.username,
                                               UserModel.avatar). \
                    filter(and_(SubcommentModel.sub == c.id, UserModel.id == SubcommentModel.user_id,
                                SubcommentModel.audit == False)). \
                    order_by(SubcommentModel.id.desc()).all()
                subs = []
                for sub in subcomments:
                    subs.append(
                        {'subid': sub.id, 'username': sub.username, 'useravatar': sub.avatar, 'reply': sub.comment})
                # 主评论过审，而且没有未审核的子评论，则不显示
                if c.audit and subs == []:
                    continue
                info.append({'username': c.username, 'useravatar': c.avatar, 'commentid': c.id, 'comment': c.comment,
                             'replies': subs})
        else:
            return jsonify({'status': 400, 'message': 'parameters error'})
        return jsonify({'status': 200, 'message': 'success', 'info': info})
    elif request.method == 'POST':
        if request.form.get('sub') and request.form.get('rpy'):
            # 回复评论的id
            sub = request.form.get('sub')
            user_id = g.user.id
            # 回复内容
            rpy = request.form.get('rpy').replace('<', '&lt;').replace('>', '&gt;').replace(' ', '&nbsp;'). \
                replace('\n', '<br>')
            cmt = SubcommentModel(sub=sub, user_id=user_id, comment=rpy)
            try:
                db.session.add(cmt)
                db.session.commit()
                return jsonify({'status': 200, 'message': 'success',
                                'data': {'reply': rpy, 'username': g.user.username, 'useravatar': g.user.avatar}})
            except:
                return jsonify({'status': 400, 'message': 'database error'})
        elif request.form.get('comment') and request.form.get('merchant_id'):
            # 非子评论
            cmt = request.form.get('comment').replace('<', '&lt;').replace('>', '&gt;').replace(' ', '&nbsp;').replace(
                '\n', '<br>')
            user_id = g.user.id
            merchant_id = request.form.get('merchant_id')
            c = CommentModel(user_id=user_id, merchant_id=merchant_id, comment=cmt)
            try:
                db.session.add(c)
                db.session.flush()
                comment_id = c.id
                db.session.commit()
                return jsonify({'status': 200, 'message': 'success',
                                'data': {'comment': cmt, 'commentid': comment_id, 'username': g.user.username,
                                         'useravatar': g.user.avatar}})
            except:
                return jsonify({'status': 400, 'message': 'database error'})
        else:
            return jsonify({'status': 400, 'message': 'parameters error'})
    elif request.method == 'PUT':
        comment_type = request.form.get('comment_type')  # comment/subcomment
        comment_id = request.form.get('comment_id')  # 子评论或者评论的id
        if comment_type in ('comment', 'subcomment') and comment_id:
            try:
                if comment_type == 'comment':
                    cmt = CommentModel.query.filter(CommentModel.id == comment_id).first()
                    if cmt is None:
                        return jsonify({'status': 404, 'message': 'comment not found'})
                    cmt.audit = True
                elif comment_type == 'subcomment':
                    subcmt = SubcommentModel.query.filter(SubcommentModel.id == comment_id).first()
                    if subcmt is None:
                        return jsonify({'status': 404, 'message': 'subcomment not found'})
                    subcmt.audit = True
                db.session.commit()
                return jsonify({'status': 200, 'message': 'success'})
            except:
                return jsonify({'status': 400, 'message': 'database error'})
        else:
            return jsonify({'status': 400, 'message': 'parameters error'})
    elif request.method == 'DELETE':
        comment_type = request.form.get('comment_type')  # comment/subcomment
        comment_id = request.form.get('comment_id')  # 子评论或者评论的id
        if comment_type in ('comment', 'subcomment') and comment_id:
            try:
                if comment_type == 'comment':
                    cmt = CommentModel.query.filter(CommentModel.id == comment_id).first()
                    if cmt is None:
                        return jsonify({'status': 404, 'message': 'comment not found'})
                    subcmts = SubcommentModel.query.filter(SubcommentModel.sub == comment_id).all()
                    for subcmt in subcmts:
                        db.session.delete(subcmt)
                    db.session.commit()
                    db.session.delete(cmt)
                elif comment_type == 'subcomment':
                    subcmt = SubcommentModel.query.filter(SubcommentModel.id == comment_id).first()
                    if subcmt is None:
                        return jsonify({'status': 404, 'message': 'subcomment not found'})
                    db.session.delete(subcmt)
                db.session.commit()
                return jsonify({'status': 200, 'message': 'success'})
            except:
                return jsonify({'status': 400, 'message': 'database error'})
        else:
            return jsonify({'status': 400, 'message': 'parameters error'})


@bp.route('/message/', methods=['GET'])
def msg():
    if request.method == 'GET':
        # 如果传入的有room和userid，返回的是这个房间的信息
        # 如果传入userid，返回的是这个用户所有房间号，以及每个房间最后一条信息
        if request.args.get('room') and request.args.get('userid'):
            userid = request.args.get('userid')
            msglist = []
            userinfo = {}
            mlist = MessageModel.query.filter(MessageModel.room == request.args.get('room')).all()
            if mlist:
                # 这里是处理已读信息
                for m in mlist:
                    if userid == str(m.user2) and m.user2_read is False:
                        m.user2_read = True
                    elif userid == str(m.user3) and m.user3_read is False:
                        m.user3_read = True
                    elif userid not in (str(m.send_msg_user), str(m.user2), str(m.user3)):
                        return jsonify({'status': 404, 'message': 'user not found'})
                    msgg = {'message': m.message, 'send_msg_user': m.send_msg_user, 'user2': m.user2,
                            'user3': m.user3, 'user2_read': m.user2_read, 'user3_read': m.user3_read}
                    msglist.append(msgg)
                db.session.commit()

                # 这边获取用户id，对应的用户名
                u1id = msglist[0]['send_msg_user']
                u2id = msglist[0]['user2']
                u3id = msglist[0]['user3']
                # print(u1id, u2id, u3id)
                u1name = UserModel.query.filter(UserModel.id == u1id).first().username
                u2name = UserModel.query.filter(UserModel.id == u2id).first().username
                u3name = UserModel.query.filter(UserModel.id == u3id).first().username
                userinfo = {u1id: u1name, u2id: u2name, u3id: u3name}
            return jsonify({'status': 200, 'message': 'success', 'data': msglist, 'userinfo': userinfo})
        elif request.args.get('userid'):
            userid = request.args.get('userid')
            orders = OrderModel.query.filter(or_(OrderModel.customer_id == userid, OrderModel.merchant_id == userid,
                                                 OrderModel.rider_id == userid)).order_by(OrderModel.id.desc()).all()
            orderlist = [i.order_id for i in orders]
            newlist = list(set(orderlist))
            newlist.sort(key=orderlist.index)
            info = []
            for orderid in newlist:
                m = {'last_msg_sender': '', 'lastMsg': '', 'room': orderid, 'unread': 0}
                mg = MessageModel.query.filter(MessageModel.room == orderid).all()
                for i in mg:
                    if userid == str(i.user2) and (not i.user2_read):
                        m['unread'] += 1
                    elif userid == str(i.user3) and (not i.user3_read):
                        m['unread'] += 1
                if mg:
                    m['lastMsg'] = mg[len(mg) - 1].message
                    m['last_msg_sender'] = turn_userid_to_name(mg[len(mg) - 1].send_msg_user)
                info.append(m)
            return jsonify({'status': 200, 'message': 'success', 'data': info})
        else:
            return jsonify({'status': 400, 'message': 'parameters is required'})


@bp.route('/notice/', methods=['GET', 'POST'])
def notice():
    if request.method == 'GET':
        try:
            n = NoticeModel.query.all()
            for i in n:
                date = i.date.split('-')
                if int(date[0]) == datetime.datetime.now().year \
                        and int(date[1]) == datetime.datetime.now().month \
                        and int(date[2]) == datetime.datetime.now().day:
                    title = i.title
                    content = i.content
                    break
            else:
                return jsonify({'status': 404, 'message': 'not found'})
            return jsonify({'status': 200, 'message': 'success', 'notice': {'title': title, 'content': content}})
        except:
            return jsonify({'status': 400, 'message': 'database error'})
    elif request.method == 'POST':
        if g.user.role == 4:
            date = request.form.get('date')
            title = request.form.get('title')
            content = request.form.get('content')

            if date and title and content:
                n = NoticeModel(date=date, title=title, content=content)
                db.session.add(n)
                db.session.commit()
                return jsonify({'status': 200, 'message': 'success'})
            else:
                lack = ''
                if not date:
                    lack += ' ' + 'date'
                if not title:
                    lack += ' ' + 'title'
                if not content:
                    lack += ' ' + 'content'
                return jsonify({'status': 400, 'message': f'please input{lack}'})
        else:
            return jsonify({'status': 403, 'message': 'you are not admin'})
