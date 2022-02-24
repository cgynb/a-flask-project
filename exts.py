from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_avatars import Avatars
from flask_dropzone import Dropzone

db = SQLAlchemy()
mail = Mail()
avatars = Avatars()
dropzone = Dropzone()