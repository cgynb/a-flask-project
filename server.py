import socketio
import eventlet.wsgi
import random
import socket
import logging
name_list = []

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
logging.basicConfig()
logging.warning('        服务器ip：     ' + ip)


def create_username(sid):
    with open('name.txt', 'r', encoding='utf-8') as f:
        names = f.readlines()
        names = list(map(lambda x: x.strip(), names))
        name = names[random.randint(0, len(names)-1)]
        while name in name_list:
            name = names[random.randint(0, len(names) - 1)]
        name_list.append((name, sid))
    return name


# create a Socket.IO server
sio = socketio.Server()

# wrap with a WSGI application
app = socketio.WSGIApp(sio)


@sio.event
def connect(sid, environ, auth):
    data = {'username': create_username(sid), 'action': 'login', 'name_list': name_list}
    sio.emit('msg', data)
    print('connect ', sid)


@sio.event
def disconnect(sid):
    for i, j in name_list:
        if j == sid:
            name_list.remove((i, j))
    sio.emit('msg', {'action': 'logout', 'name_list': name_list})
    print(name_list)
    print('disconnect ', sid)


@sio.on('msg')
def msg(sid, data):
    print(data)
    sio.emit('msg', data)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
