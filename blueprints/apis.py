import json
import random
import string
import time

from flask import Blueprint, jsonify, g, request
from sqlalchemy import and_, or_

from data import orderConbinition, turn_userid_to_name, order_overdate
from exts import db
from models import TagModel, UserModel, FoodModel, OrderModel, FollowModel, CommentModel, SubcommentModel, MessageModel

bp = Blueprint('apis', __name__, url_prefix='/elebu/api/v1/')


@bp.route('/tag/', methods=['GET', 'POST', 'DELETE'])
def tag():
    if request.method == 'GET':
        tags = TagModel.query.filter(TagModel.user_id == g.user.id).all()
        data = []
        for t in tags:
            t = {'tag': t.t}
            data.append(t)
        return jsonify(data)
    elif request.method == 'POST':
        gettag = request.form.get('tag')
        t = TagModel(user_id=g.user.id, t=gettag)
        db.session.add(t)
        db.session.commit()
        return jsonify({'status': 200, 'message': 'success'})
    elif request.method == 'DELETE':
        deltag = request.form.get('tag')
        t = TagModel.query.filter(and_(TagModel.t == deltag, TagModel.user_id == g.user.id)).first()
        db.session.delete(t)
        db.session.commit()
        return jsonify({'status': 200, 'message': 'success'})


@bp.route('/selfinfo/', methods=['GET', 'PUT', 'DELETE'])
def selfInfo():
    if request.method == 'GET':
        if request.args.get('num') == 'self':
            user = db.session.query(UserModel.username, UserModel.role, UserModel.avatar,
                                    UserModel.join_time, UserModel.selfintroduce, UserModel.avatar) \
                .filter(UserModel.id == g.user.id).first()
            return jsonify({'user_id': g.user.id,
                            'username': user.username,
                            'role': user.role,
                            'join_time': user.join_time,
                            'avatar': user.avatar,
                            'selfintroduce': user.selfintroduce})
        elif request.args.get('num') == 'one' and request.args.get('merchant_id'):
            user = UserModel.query.filter(UserModel.id == request.args.get('merchant_id')).first()
            return jsonify({'avatar': user.avatar, 'username': user.username})
        elif request.args.get('num') == 'merchant':
            keyword = request.args.get('keyword')
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
            else:
                total_info = UserModel.query.filter(UserModel.role == 2).count()
                total_page = total_info // 4
                if total_info % 4:
                    total_page += 1
                merchants = UserModel.query.filter(and_(UserModel.role == 2)). \
                    offset(per_page * (int(page) - 1)).limit(per_page).all()
            for m in merchants:
                merchant = {'merchant_id': m.id, 'username': m.username, 'avatar': m.avatar,
                            'introduce': m.selfintroduce}
                merchantlist.append(merchant)
            return jsonify({'page': page, 'total_page': total_page, 'merchants': merchantlist})
    elif request.method == 'PUT':
        try:
            selfintroduce = request.form.get('selfintroduce')
            user = UserModel.query.filter(UserModel.id == g.user.id).first()
            user.selfintroduce = selfintroduce.replace('<', '&lt;').replace('>', '&gt;').replace(' ', '&nbsp;').replace(
                '\n', '<br>')
            db.session.commit()
            return jsonify({'status': 200, 'message': 'success'})
        except Exception as e:
            print(e)
            return jsonify({'status': 400, 'message': 'fail'})


@bp.route('/food/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def foodInfo():
    if request.method == 'GET':
        if request.args.get('num') == 'self':
            foods = FoodModel.query. \
                filter(and_(FoodModel.merchant_id == g.user.id, FoodModel.merchant_name == g.user.username)).all()
            info = []
            for food in foods:
                f = {'food_id': food.id, 'food_price': food.food_price, 'food_name': food.food_name,
                     'food_desc': food.food_desc, 'zans': food.zans, 'address': food.address}
                info.append(f)
        elif request.args.get('merchant_id'):
            info = []
            foods = FoodModel.query. \
                filter(FoodModel.merchant_id == request.args.get('merchant_id')).all()
            for food in foods:
                f = {'food_price': food.food_price, 'food_name': food.food_name, 'address': food.address,
                     'food_id': food.id, 'food_desc': food.food_desc, 'zans': food.zans}
                info.append(f)
        return jsonify({'status': 200, 'message': 'success', 'info': info})
    elif request.method == 'POST':
        pass
    elif request.method == 'DELETE':
        food_id = request.form.get('food_id')
        try:
            food = FoodModel.query.filter(and_(FoodModel.merchant_id == g.user.id, FoodModel.id == food_id)).first()
            db.session.delete(food)
            db.session.commit()
            return jsonify({'status': 200, 'message': 'success'})
        except Exception as e:
            print(e)
            return jsonify({'status': 400, 'message': 'fail'})


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
        return jsonify({'status': 200, 'message': 'success'})
    elif request.method == 'PUT':
        order_id = request.form.get('order_id')
        rider_salary = request.form.get('rider_salary')
        if rider_salary:  # 商家接单
            orders = OrderModel.query.filter(OrderModel.order_id == order_id).all()
            for order in orders:
                order.merchant_take_order = True
                order.rider_salary = float(rider_salary)
            db.session.commit()
        elif request.form.get('arrive') == 'arrive':  # 确认送达
            orders = OrderModel.query.filter(OrderModel.order_id == order_id).all()
            for order in orders:
                order.arrive = True
            db.session.commit()
        else:  # 骑手接单
            orders = OrderModel.query.filter(OrderModel.order_id == order_id).all()
            for order in orders:
                order.rider_id = g.user.id
            db.session.commit()
        return jsonify({'status': 200, 'message': 'success'})


@bp.route('/zan/', methods=['PUT'])
def Zan():
    order_id = request.form.get('order_id')
    zan = request.form.get('zan')
    food_id = request.form.get('food_id')
    food = FoodModel.query.filter(FoodModel.id == food_id).first()
    order = OrderModel.query.filter(and_(OrderModel.order_id == order_id, OrderModel.food_id == food_id)).first()
    if zan == 'zaned':
        order.zan = False
        food.zans -= 1
    elif zan == 'tozan':
        order.zan = True
        food.zans += 1
    db.session.commit()
    return jsonify({'status': 200, 'message': 'success'})


@bp.route('/follow/', methods=['GET', 'POST', 'DELETE'])
def follow():
    if request.method == 'GET':
        follow_list = request.args.get('follow_list')
        if follow_list:
            info = []
            fs = db.session. \
                query(FollowModel.followed_id, UserModel.username, UserModel.avatar, UserModel.selfintroduce) \
                .filter(and_(FollowModel.follower_id == g.user.id, UserModel.id == FollowModel.followed_id)).all()
            for f in fs:
                data = {'merchant_id': f.followed_id, 'merchant_name': f.username, 'merchant_avatar': f.avatar,
                        'merchant_introduce': f.selfintroduce}
                info.append(data)
            return jsonify({'status': 200, 'message': 'success', 'info': info})
        followed_id = request.args.get('followed_id')
        if followed_id:  # 查看自己是否关注
            follower_id = g.user.id
            f = FollowModel.query.filter(
                and_(FollowModel.followed_id == followed_id, FollowModel.follower_id == follower_id)).first()
            if f:
                return jsonify({'status': 200, 'message': 'success', 'info': 'followed'})
            else:
                return jsonify({'status': 200, 'message': 'success', 'info': 'tofollow'})
        else:  # 获取商家关注数
            merchant_id = request.args.get('merchant_id')
            f = FollowModel.query.filter(FollowModel.followed_id == merchant_id).count()
            return jsonify({'status': 200, 'message': 'success', 'follow-num': f})

    elif request.method == 'POST':
        followed_id = request.form.get('followed_id')
        follower_id = g.user.id
        f = FollowModel(follower_id=follower_id, followed_id=followed_id)
        db.session.add(f)
        db.session.commit()
    else:
        followed_id = request.form.get('followed_id')
        f = FollowModel.query.filter(
            and_(FollowModel.followed_id == followed_id, FollowModel.follower_id == g.user.id)).first()
        db.session.delete(f)
        db.session.commit()
    return jsonify({'status': 200, 'message': 'success'})


@bp.route('/comment/', methods=['GET', 'POST', 'DELETE'])
def comment():
    if request.method == 'GET':
        info = []
        if request.args.get('num') != 'all':
            merchant_id = request.args.get('merchant_id')
            comments = db.session. \
                query(UserModel.username, UserModel.avatar, CommentModel.comment, CommentModel.id). \
                filter(and_(CommentModel.merchant_id == merchant_id, UserModel.id == CommentModel.user_id)). \
                order_by(CommentModel.id.desc()).all()
            for c in comments:
                subcomments = db.session.query(SubcommentModel.comment, UserModel.username, UserModel.avatar). \
                    filter(and_(SubcommentModel.sub == c.id, UserModel.id == SubcommentModel.user_id)). \
                    order_by(SubcommentModel.id.desc()).all()
                subs = []
                for sub in subcomments:
                    subs.append({'username': sub.username, 'useravatar': sub.avatar, 'reply': sub.comment})
                info.append({'username': c.username, 'useravatar': c.avatar, 'commentid': c.id, 'comment': c.comment,
                             'replies': subs})
        else:
            pass
        return jsonify({'status': 200, 'message': 'success', 'info': info})
    elif request.method == 'POST':
        if request.form.get('sub'):
            # 子评论
            sub = request.form.get('sub')
            user_id = g.user.id
            c = request.form.get('rpy').replace('<', '&lt;').replace('>', '&gt;').replace(' ', '&nbsp;').replace('\n',
                                                                                                                 '<br>')
            cmt = SubcommentModel(sub=sub, user_id=user_id, comment=c)
            db.session.add(cmt)
            db.session.commit()
            return jsonify({'status': 200, 'message': 'success',
                            'data': {'reply': c, 'username': g.user.username, 'useravatar': g.user.avatar}})
        else:
            # 非子评论
            cmt = request.form.get('comment').replace('<', '&lt;').replace('>', '&gt;').replace(' ', '&nbsp;').replace(
                '\n', '<br>')
            user_id = g.user.id
            merchant_id = request.form.get('merchant_id')
            c = CommentModel(user_id=user_id, merchant_id=merchant_id, comment=cmt)
            db.session.add(c)
            db.session.commit()
            return jsonify({'status': 200, 'message': 'success',
                            'data': {'comment': cmt, 'username': g.user.username, 'useravatar': g.user.avatar}})
    else:
        pass


@bp.route('/message/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def msg():
    if request.method == 'GET':
        if request.args.get('room'):
            userid = request.args.get('userid')
            msglist = []
            userinfo = {}
            mlist = MessageModel.query.filter(MessageModel.room == request.args.get('room')).all()
            if mlist:
                for m in mlist:
                    if userid == str(m.user2) and m.user2_read is False:
                        m.user2_read = True
                    elif userid == str(m.user3) and m.user3_read is False:
                        m.user3_read = True
                    msgg = {'message': m.message, 'send_msg_user': m.send_msg_user, 'user2': m.user2,
                            'user3': m.user3, 'user2_read': m.user2_read, 'user3_read': m.user3_read}
                    msglist.append(msgg)
                db.session.commit()
                u1id = msglist[0]['send_msg_user']
                u2id = msglist[0]['user2']
                u3id = msglist[0]['user3']
                u1name = UserModel.query.filter(UserModel.id == u1id).first().username
                u2name = UserModel.query.filter(UserModel.id == u2id).first().username
                u3name = UserModel.query.filter(UserModel.id == u3id).first().username
                userinfo = {u1id: u1name, u2id: u2name, u3id: u3name}
            return jsonify({'status': 200, 'message': 'success', 'data': msglist, 'userinfo': userinfo})
        elif request.args.get('userid'):
            userid = request.args.get('userid')
            orders = OrderModel.query.filter(or_(OrderModel.customer_id == userid, OrderModel.merchant_id == userid,
                                                 OrderModel.rider_id == userid)).order_by(OrderModel.id.desc()).all()
            orderlist = [i.order_id for i in orders if order_overdate(i)]
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
            return jsonify({'status': 400, 'message': 'params is required'})
    elif request.method == 'POST':
        print(request.json)
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        pass
