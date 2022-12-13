import os
import sys

#basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
basedir = os.path.abspath(os.path.dirname(__file__))

# SQLite URI compatible
WIN = sys.platform.startswith("win")
if WIN:
    prefix = "sqlite:///"
else:
    prefix = "sqlite:////"


class BaseConfig(object):
    SECRET_KEY = os.getenv("SECRET_KEY", "dev key")

    DEBUG_TB_INTERCEPT_REDIRECTS = False
    
    ADMIN_NAME = ['test','管理员1']
    ADMIN_ID = [1]

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    CKEDITOR_ENABLE_CSRF = True
    CKEDITOR_FILE_UPLOADER = ""
    CKEDITOR_LANGUAGE = "zh-cn"

    # MAIL_SERVER = os.getenv('MAIL_SERVER')
    # MAIL_PORT = 465
    # MAIL_USE_SSL = True
    # MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    # MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    # MAIL_DEFAULT_SENDER = ('Bluelog Admin', MAIL_USERNAME)
    MAIL_SERVER = "smtp.qq.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = True
    MAIL_USERNAME = "1007736246@qq.com"
    MAIL_PASSWORD = "mbjqvvtlaaxubebh"
    MAIL_DEFAULT_SENDER = "1007736246@qq.com"

    ### dropzone 的配置
    FILE_UPLOAD_PATH = os.path.join(basedir, "static/uploads")
    DROPZONE_ENABLE_CSRF = False
    # BLUELOG_EMAIL = os.getenv('BLUELOG_EMAIL')
    POST_PER_PAGE = 10
    BLUELOG_MANAGE_POST_PER_PAGE = 15
    BLUELOG_COMMENT_PER_PAGE = 15
    # ('theme name', 'display name')
    BLUELOG_THEMES = {"perfect_blue": "Perfect Blue", "black_swan": "Black Swan"}
    BLUELOG_SLOW_QUERY_THRESHOLD = 1

    BLUELOG_UPLOAD_PATH = os.path.join(basedir, "uploads")
    BLUELOG_ALLOWED_IMAGE_EXTENSIONS = ["png", "jpg", "jpeg", "gif"]

    # chat config
    CHAT_MESSAGE_PER_PAGE = 30

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, "data-dev.db")


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # in-memory database


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", prefix + os.path.join(basedir, "data.db"))


config = {"development": DevelopmentConfig, "testing": TestingConfig, "production": ProductionConfig}
