from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_avatars import Avatars
from flask_dropzone import Dropzone
from flask_socketio import SocketIO
from flask_apscheduler import APScheduler
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
db = SQLAlchemy()
mail = Mail()
avatars = Avatars()
dropzone = Dropzone()
socketio = SocketIO()
scheduler = APScheduler()
migrate = Migrate()
limiter = Limiter(key_func=get_remote_address, default_limits=["2000 per day", "500 per hour"])
