from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room


app = Flask(__name__)
app.config['SECRET_KEY'] = 'jjj'

socketio = SocketIO()
socketio.init_app(app)


online_user = []
room_user = {}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        if 'username' in session:
            return redirect(url_for('chat'))
        return render_template('index.html')
    else:
        username = request.form.get('username')
        room = request.form.get('room')
        session['username'] = username
        session['room'] = room
        return redirect(url_for('chat'))


@app.route('/chat/')
def chat():
    if 'username' in session and 'room' in session:
        username = session['username']
        room = session['room']
        return render_template('chat.html', username=username, room=room)
    else:
        return redirect(url_for('index'))


@app.route('/logout/')
def logout():
    if 'username' in session:
        session.clear()
    return redirect(url_for('index'))


# # 连接
@socketio.on('connect')
def handle_connect():
    username = session.get('username')
    online_user.append(username)
    # print('connect info:  ' + f'{username}  connect')
    # print(online_user)
    # socketio.emit('connect info', f'{username}  connect')


# 断开连接
@socketio.on('disconnect')
def handle_disconnect():
    username = session.get('username')
    print('connect info:  ' + f'{username}  disconnect')
    # socketio.emit('connect info', f'{username}  disconnect')


# @socketio.on('connect info')
# def handle_connect_info(info):
#     print('connect info' + str(info))
#     room = session.get('room')
#     socketio.emit('connect info', info, to=room)


@socketio.on('send msg')
def handle_message(data):
    print('sendMsg' + str(data))
    room = session.get('room')
    data['message'] = data.get('message').replace('<', '&lt;').replace('>', '&gt;').replace(' ', '&nbsp;')
    socketio.emit('send msg', data, to=room)


@socketio.on('join')
def on_join(data):
    username = data.get('username')
    room = data.get('room')
    try:
        room_user[room].append(username)
    except:
        room_user[room] = []
        room_user[room].append(username)

    join_room(room)
    print('join room:  ' + str(data))
    print(room_user)
    socketio.emit('connect info', username + '加入房间', to=room)


@socketio.on('leave')
def on_leave(data):
    username = data.get('username')
    room = data.get('room')
    room_user[room].remove(username)
    leave_room(room)
    print('leave room   ' + str(data))
    print(room_user)
    socketio.emit('connect info', username + '离开房间', to=room)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
