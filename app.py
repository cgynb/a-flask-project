from flask import Flask, session, g
from blueprints import food_bp, user_bp, apis_bp, chat_bp
from exts import db, mail, avatars, dropzone, socketio
from flask_migrate import Migrate
import config
from models import UserModel

app = Flask(__name__)

app.config.from_object(config)

app.register_blueprint(food_bp)
app.register_blueprint(user_bp)
app.register_blueprint(apis_bp)
app.register_blueprint(chat_bp)

db.init_app(app)
mail.init_app(app)
avatars.init_app(app)
dropzone.init_app(app)
socketio.init_app(app)
migrate = Migrate(app, db)


@app.before_request
def before_request():
    user_id = session.get('user_id')
    if user_id:
        try:
            user = UserModel.query.get(user_id)
            g.user = user
            if user.role == 1:
                g.role = '顾客'
            elif user.role == 2:
                g.role = '商家'
            elif user.role == 3:
                g.role = '骑手'
            elif user.role == 4:
                g.role = '管理员'
            else:
                g.role = None
        except Exception as e:
            print(e)
            g.user = None


@app.context_processor
def context_processor():
    if hasattr(g, 'user'):
        return {'user': g.user}
    else:
        return {}


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
