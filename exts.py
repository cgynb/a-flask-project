from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_avatars import Avatars
from flask_dropzone import Dropzone
from flask_socketio import SocketIO
from flask_apscheduler import APScheduler
from flask_migrate import Migrate

db = SQLAlchemy()
mail = Mail()
avatars = Avatars()
dropzone = Dropzone()
socketio = SocketIO()
scheduler = APScheduler()
migrate = Migrate()
