import socketio
import eventlet.wsgi
import random

name_list = []


def create_username():
    with open('name.txt', 'r', encoding='utf-8') as f:
        names = f.readlines()
        names = list(map(lambda x: x.strip(), names))
        name = names[random.randint(0, len(names)-1)]
        while name in name_list:
            name = names[random.randint(0, len(names) - 1)]
        name_list.append(name)
    return name


# create a Socket.IO server
sio = socketio.Server()

# wrap with a WSGI application
app = socketio.WSGIApp(sio)


@sio.event
def connect(sid, environ, auth):
    data = {'username': create_username(), 'action': 'login', 'name_list': name_list}
    sio.emit('msg', data)
    # print('connect ', sid)


@sio.event
def disconnect(sid):
    # print('disconnect ', sid)
    pass


@sio.on('msg')
def msg(sid, data):
    print(data)
    if data['action'] == 'logout':
        name_list.remove(data['username'])
        data['name_list'] = name_list
        sio.emit('msg', data)
    else:
        sio.emit('msg', data)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
