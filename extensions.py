from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from flask_socketio import SocketIO

from flask_ckeditor import CKEditor
from flask_dropzone import Dropzone

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
ckeditor = CKEditor()
mail = Mail()
moment = Moment()
toolbar = DebugToolbarExtension()
migrate = Migrate()
socketio = SocketIO()
ckeditor= CKEditor()
dropzone=Dropzone()

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

login_manager.login_view = 'user.login'
