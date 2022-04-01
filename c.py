import socketio

sio = socketio.Client()


@sio.on('connect')
def connect():
    sio.emit('msg', "i'm back")
    print('connect')


@sio.on('disconnect')
def disconnect():
    print('disconnect')


@sio.on('msg')
def handle_msg(data):
    print(data)


sio.connect('http://localhost:5000')
sio.wait()

print('hhh')