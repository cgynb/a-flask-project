from flask import Flask, g, render_template, request
import click
from blueprints import food_bp, user_bp, apis_bp, chat_bp, admin_bp
from exts import db, mail, avatars, dropzone, socketio, scheduler, migrate
from token_operation import create_token, validate_token
import config
from models import UserModel
import eventlet
from eventlet import wsgi

# eventlet.monkey_patch()

app = Flask(__name__)

app.config.from_object(config)

app.register_blueprint(food_bp)
app.register_blueprint(user_bp)
app.register_blueprint(apis_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(admin_bp)

db.init_app(app)
mail.init_app(app)
avatars.init_app(app)
dropzone.init_app(app)
socketio.init_app(app, cors_allowed_origins='*', async_mode='eventlet')
scheduler.init_app(app)
migrate.init_app(app, db)


@app.before_request
def before_request():
    token, msg = validate_token(request.cookies.get('token'))
    if msg is None:
        try:
            user = UserModel.query.filter(UserModel.id == token.get('user_id')).first()
            g.user = user
            if user.role == 1:
                g.role = '顾客'
            elif user.role == 2:
                g.role = '商家'
            elif user.role == 3:
                g.role = '骑手'
            elif user.role == 4:
                g.role = '管理员'
        except Exception as e:

            print(e)


@app.context_processor
def context_processor():
    if hasattr(g, 'user'):
        return {'user': g.user}
    else:
        return {}


@app.after_request
def after_request(resp):
    if hasattr(resp, 'logout') and resp.logout is True:
        resp.delete_cookie('token')
    else:
        if hasattr(g, 'user'):
            token = create_token(g.user)
            resp.set_cookie('token', token, max_age=3600)
    return resp


@app.route('/try/')
def hello():
    return render_template('try.html')


@app.cli.command('start')
@click.argument("port")
def start(port):
    click.echo('start !!!')
    # wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)
    if isinstance(port, str) and port.isdigit():
        socketio.run(app, host='0.0.0.0', port=int(port), debug=True)


# if __name__ == '__main__':
#     socketio.run(app, host='0.0.0.0', port=5000, debug=True)
#     app.run(host='0.0.0.0', port=5000, threaded=True)
