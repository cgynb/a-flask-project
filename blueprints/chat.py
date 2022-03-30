from flask import Blueprint, render_template, session, g, request, redirect, url_for, flash
from flask_socketio import join_room, leave_room
import datetime
import time
from exts import socketio, db
from models import OrderModel, MessageModel, UserModel
from require import login_required
from data import turn_userid_to_name, order_overdate

bp = Blueprint('chat', __name__, url_prefix='/chat/')


rooms = []
# rooms = [{'roomid': 1234, 'people': ['iid', 'hhh', 'kkk']}]


@bp.route('/', methods=['GET'])
@login_required
def chatRoom():
    order_id = request.args.get('orderid')
    order = OrderModel.query.filter(OrderModel.order_id == order_id).first()
    if not order:
        return redirect(url_for('food.index'))
    idlist = [order.customer_id, order.merchant_id, order.rider_id]
    if not order_overdate(order):
        flash('订单过期啦')
        return redirect(url_for('food.index'))
    if g.user.id in idlist:
        return render_template('chatroom.html', username=g.user.username, user_id=g.user.id)
    else:
        return redirect(url_for('food.index'))


@socketio.on('connect')
def handle_connect():
    username = session.get('username')
    print(f'{username} connect')


@socketio.on('disconnect')
def handle_disconnect():
    username = session.get('username')
    print(f'{username} disconnect')


@socketio.on('send msg')
def handle_message(data):
    print('sendMsg:' + str(data))
    room = data.get('room')
    data['message'] = data.get('message').\
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
            except AttributeError as e:
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
            r['people'].append(username)
            break
    else:
        rooms.append({'roomid': room, 'people': [username]})
    print(rooms)
    socketio.emit('connect info', username + '加入房间', to=room)


@socketio.on('leave')
def on_leave(data):
    username = data.get('username')
    room = data.get('room')
    leave_room(room)
    for r in rooms:
        if r['roomid'] == room:
            r['people'].remove(username)
            break
    print(rooms)
    print('leave room   ' + str(data))
    socketio.emit('connect info', username + '离开房间', to=room)
