from flask import Blueprint, render_template, g, request, redirect, url_for, flash
from flask_socketio import join_room, leave_room
from token_operation import validate_token
from exts import socketio, db
from models import OrderModel, MessageModel
from require import login_required
from data import turn_userid_to_name

bp = Blueprint('chat', __name__, url_prefix='/chat/')

rooms = []
# rooms = [
#
#           {'people': [{'sid': 'sid1', 'username': 'u1'},
#                       {'sid': 'sid2', 'username': 'u2'}],
#            'roomid': 'roomid1'},
#
#           {'people': [{'sid': 'sid3', 'username': 'u3'},
#                       {'sid': 'sid4', 'username': 'u4'}],
#            'roomid': 'roomid2'}
#
#          ]


@bp.route('/', methods=['GET'])
@login_required
def chatRoom():
    order_id = request.args.get('orderid')
    order = OrderModel.query.filter(OrderModel.order_id == order_id).first()
    if not order:
        return redirect(url_for('food.index'))
    if order.merchant_take_order and order.rider_id is not None:
        idlist = [order.customer_id, order.merchant_id, order.rider_id]
        if g.user.id in idlist:
            return render_template('chatroom.html', username=g.user.username, user_id=g.user.id)
        else:
            return redirect(url_for('food.index'))
    else:
        flash('商家或骑手还没有接单')
        return redirect(url_for('user.homepage'))


@socketio.on('connect')
def handle_connect():
    username = validate_token(request.cookies.get('token'))[0].get('name')
    print(f'{username} connect, sid: {request.sid}')
    # socketio.emit('connect info', username + '加入房间', to=room)


@socketio.on('disconnect')
def handle_disconnect():
    username = validate_token(request.cookies.get('token'))[0].get('name')
    print(f'{username} disconnect, sid: {request.sid}')
    roomid = None
    # 根据reques.sid找到用户，从rooms列表中删去用户信息
    from pprint import pprint
    pprint(rooms)
    for room in rooms:
        for person in room['people']:
            if person.get('sid') == request.sid:
                room['people'].remove(person)
                roomid = room['roomid']
                break
    socketio.emit('connect info', username + '离开房间', to=roomid)


@socketio.on('send msg')
def handle_message(data):
    print('sendMsg:' + str(data))
    room = data.get('room')
    data['message'] = data.get('message'). \
        replace('<', '&lt;').replace('>', '&gt;').replace(' ', '&nbsp;').replace('\n', '')
    order = OrderModel.query.filter(OrderModel.order_id == room).first()
    idlist = [order.customer_id, order.merchant_id, order.rider_id]
    idlist.remove(int(data.get('userid')))
    user2id, user3id = idlist
    for r in rooms:
        if r['roomid'] == room:
            user2_read = True if turn_userid_to_name(user2id) in r['people'] else False
            try:
                user3_read = True if turn_userid_to_name(user3id) in r['people'] else False
            except AttributeError as _:
                user3_read = False
            msg = MessageModel(message=data['message'], send_msg_user=data.get('userid'), room=room,
                               user2=user2id, user3=user3id, user2_read=user2_read, user3_read=user3_read)
            db.session.add(msg)
            db.session.commit()
    socketio.emit('send msg', data, to=room)


@socketio.on('join')
def on_join(data):
    username = data.get('username')
    room = data.get('room')
    join_room(room)
    # print('join room:  ' + str(data))
    for r in rooms:
        if r['roomid'] == room:
            r['people'].append({'username': username, 'sid': request.sid})
            break
    else:
        rooms.append({'roomid': room, 'people': [{'username': username, 'sid': request.sid}]})
    print(rooms)
    socketio.emit('connect info', username + '加入房间', to=room)

# @socketio.on('leave')
# def on_leave(data):
#     username = data.get('username')
#     room = data.get('room')
#     leave_room(room)
#     for r in rooms:
#         if r['roomid'] == room:
#             r['people'].remove(username)
#             break
#     print(rooms)
#     print('leave room   ' + str(data))
#     socketio.emit('connect info', username + '离开房间', to=room)
