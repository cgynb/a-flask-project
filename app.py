from flask import Flask, session, g
from flask_migrate import Migrate

import config
from exts import db, mail, avatars, dropzone

from blueprints import user_bp, food_bp, admin_bp

from models import UserModel, MerchantsModel

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)
mail.init_app(app)
avatars.init_app(app)
dropzone.init_app(app)

app.register_blueprint(food_bp)
app.register_blueprint(user_bp)
app.register_blueprint(admin_bp)

migrate = Migrate(app, db)


@app.before_request
def before_request():
    user_id = session.get('user_id')
    if user_id:
        try:
            user = UserModel.query.get(user_id)
            # 给g绑定一个叫做user的变量，他的值是user这个变量
            # setattr(g, 'user', user)  可以这样写
            g.user = user
            if user.role_id == 1:
                g.role = '顾客'
            elif user.role_id == 2:
                g.role = '商家'
            elif user.role_id == 3:
                g.role = '骑手'
            elif user.role_id == 4:
                g.role = '管理员'
            else:
                g.role = None
        except:
            g.user = None


@app.context_processor
def context_processor():
    if hasattr(g, 'user'):
        if g.role == '商家':
            merchant = MerchantsModel.query.filter(MerchantsModel.email == g.user.email).first()
            label = merchant.label
            return {'user': g.user, 'role': g.role, 'label': label}
        else:
            return {'user': g.user, 'role': g.role}
    else:
        return {}


if __name__ == '__main__':
    app.run(debug=True)
