from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit


app = Flask(__name__)
app.config['SECRET_KEY'] = 'jjj'

socketio = SocketIO()
socketio.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        if 'username' in session:
            return redirect(url_for('chat'))
        return render_template('index.html')
    else:
        username = request.form.get('username')
        session['username'] = username
        return redirect(url_for('chat'))


@app.route('/chat/')
def chat():
    if 'username' in session:
        username = session['username']
        return render_template('chat.html', username=username)
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
    print('*' * 20, f'{username}  connect', '*' * 20)
    socketio.emit('connect info', f'{username}  connect')


# 断开连接
@socketio.on('disconnect')
def handle_disconnect():
    username = session.get('username')
    print('*' * 20, f'{username}  disconnect', '*' * 20)
    socketio.emit('connect info', f'{username}  disconnect')


@socketio.on('connect info')
def handle_connect_info(info):
    print('connect info' + str(info))
    socketio.emit('connect info', info)


@socketio.on('send msg')
def handle_message(data):
    print('sendMsg' + str(data))
    socketio.emit('send msg', data)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
