import ttkbootstrap
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap.dialogs.dialogs import Messagebox
import threading
import socketio
import time

sio = socketio.Client()


@sio.on('connect')
def connect():
    w.window.deiconify()


@sio.on('disconnect')
def disconnect():
    # print('disconnect')
    pass


def flash_msg(title, message):
    toast = ToastNotification(
        title=title,
        message=message,
        duration=4000,
    )
    toast.show_toast()


@sio.on('msg')
def handle_msg(data):
    print(data)
    if data['action'] == 'login':
        if not w.username:
            w.username = data['username']
            w.label_var.set(w.label_var.get() + f" ({w.username})")
            for name, sid in data['name_list']:
                w.add_user(name)
        else:
            flash_msg("有新用户加入了聊天", '欢迎' + data['username'])
            w.add_user(data['username'])
    elif data['action'] == 'logout':
        print(data['name_list'])
        w.user_list.delete('1.0', 'end')
        w.user_list.insert('end', '在线用户：')
        for name, sid in data['name_list']:
            w.add_user(name)
    else:
        if data['username'] != w.username:
            flash_msg("有新消息", data['username'] + ':' + data['msg'])
        w.show_msg(data['username'], data['msg'])


class ChatWindow:
    def __init__(self):
        self.sysclose = False
        self.username = None
        self.ip = ''
        # 窗口设置
        self.window = ttkbootstrap.Style(theme='lumen').master
        self.window.title('聊天室')
        ws = self.window.winfo_screenwidth()
        hs = self.window.winfo_screenheight()
        # 计算 x, y 位置
        x = (ws / 2) - (1000 / 2)
        y = (hs / 2) - (600 / 2) - 100
        self.window.geometry(f'1000x600+{int(x)}+{int(y)}')
        # 标题设置
        self.label_var = ttkbootstrap.StringVar()
        self.title = ttkbootstrap.Label(self.window, textvariable=self.label_var,
                                        font=('Arial', 17), background='#f4f4f4')
        self.title.place(width=800, height=60, x=0, y=0)
        self.label_var.set(' ' * 50 + '匿名聊天室')

        # 输入框
        self.e = ttkbootstrap.Text(self.window, width=100, height=6)
        self.e.place(height=90, width=630, x=30, y=470)
        self.e.bind('<Return>', self.post_msg)

        # 发送消息按钮
        self.b = ttkbootstrap.Button(self.window, text='发送', command=self.post_msg)
        self.b.place(height=90, width=90, x=670, y=470)

        # 会话框
        self.msg_box = ttkbootstrap.ScrolledText(self.window, width=100, height=22)
        self.msg_box.place(x=30, y=60)

        # 用户列表
        self.user_list = ttkbootstrap.ScrolledText(self.window, width=24, height=33)
        self.user_list.place(x=780, y=0)
        self.user_list.insert('end', '在线用户：')

        # 输入ip
        self.ipwin = ttkbootstrap.Toplevel(self.window)
        self.ipwin.title('连接服务器')
        self.ipwin.geometry('400x80')
        self.inp_var = ttkbootstrap.StringVar()
        self.ininp = ttkbootstrap.Entry(self.ipwin, textvariable=self.inp_var)
        self.ipconfirm = ttkbootstrap.Button(self.ipwin, text='确认', command=self.get_ip)
        self.ininp.pack()
        self.ipconfirm.pack()
        self.inp_var.set('请输入要连接服务器的ip')
        self.ininp.bind('<Button-1>', lambda e: self.inp_var.set(''))

        # 设置关闭窗口事件
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.ipwin.protocol("WM_DELETE_WINDOW", self.force_close)

    def get_ip(self):
        self.ip = self.ininp.get()
        self.ipwin.destroy()

    def post_msg(self, event=None):
        m = self.get_msg()
        sio.emit('msg', {'action': 'send msg', 'username': self.username, 'msg': m})

    def get_msg(self):
        return self.e.get('0.0', 'end').strip()

    def show_msg(self, username, message):
        if message:
            self.msg_box.insert('end', '\n' + username + ':' + '\n' + message)
            self.e.delete('0.0', 'end')

    def add_user(self, username):
        # print(username)
        if username:
            self.user_list.insert('end', '\n' + ' ' * 5 + username)

    def run(self):
        self.ipwin.place_window_center()
        self.window.withdraw()
        self.window.mainloop()

    def force_close(self):
        try:
            self.window.destroy()
            self.sysclose = True
            sio.disconnect()
        finally:
            self.window.destroy()

    # 关闭窗口的同时，断开连接
    def on_closing(self):
        ret = Messagebox.okcancel('关咯', title='提示')
        if ret == '确定':
            self.window.destroy()
            sio.disconnect()
        elif ret == '取消':
            return


def start():
    global w
    w = ChatWindow()
    w.run()


if __name__ == '__main__':
    ip = ''
    w = None
    t1 = threading.Thread(target=start)
    t1.start()
    while w is None or not w.ip:
        time.sleep(0.01)
        if w is not None and not w.ip:
            if w.sysclose:
                break

    if not w.sysclose:
        try:
            sio.connect(f'http://{w.ip}:5000')
            sio.wait()
        except Exception as exception:
            flash_msg(title='连接问题', message='未能连接到服务器')
            time.sleep(3)
            print('没有连接上')
            print(exception)
            w.force_close()
