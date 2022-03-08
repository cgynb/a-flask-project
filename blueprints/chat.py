from flask import Blueprint, render_template, session, g, request, redirect, url_for
from flask_socketio import join_room, leave_room
from decorators import login_required
from exts import socketio
from models import OrderModel

bp = Blueprint('chat', __name__, url_prefix='/chat/')


@bp.route('/', methods=['GET'])
@login_required
def chatRoom():
    order_id = request.args.get('order_id')
    order = OrderModel.query.filter(OrderModel.id == order_id).first()
    idList = [order.customer_id, order.merchant_id, order.rider_id]
    if not order.arrive and g.user.id in idList:
        return render_template('chatroom.html', room=order_id, username=g.user.username, role_id=g.user.role_id)
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
    print('sendMsg' + str(data))
    room = data.get('room')
    data['message'] = data.get('message').\
        replace('<', '&lt;').replace('>', '&gt;').replace(' ', '&nbsp;').replace('\n', '')
    socketio.emit('send msg', data, to=room)


@socketio.on('join')
def on_join(data):
    username = data.get('username')
    room = data.get('room')
    join_room(room)
    print('join room:  ' + str(data))
    socketio.emit('connect info', username + '加入房间', to=room)


@socketio.on('leave')
def on_leave(data):
    username = data.get('username')
    room = data.get('room')
    leave_room(room)
    print('leave room   ' + str(data))
    socketio.emit('connect info', username + '离开房间', to=room)
