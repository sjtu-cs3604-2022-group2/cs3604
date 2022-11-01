#### 数据库的配置信息
HOSTNAME='127.0.0.1'
PORT='3306'
DATABASE='hobbitat'
USERNAME='root'
PASSWORD='10077zkn555666'

### Debug模式
FLASK_DEBUG=True

# DB_URI='mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
### 现在先不使用mysql数据库，使用SqLite 
# 
SQLALCHEMY_TRACK_MODIFICATIONS=False
SECRET_KEY='zknzknzkn123456'
# 
### 邮箱配置
MAIL_SERVER ='smtp.qq.com'
MAIL_PORT =465
MAIL_USE_TLS =False
MAIL_USE_SSL = True
MAIL_DEBUG = True
MAIL_USERNAME ='1007736246@qq.com'
MAIL_PASSWORD ='mbjqvvtlaaxubebh'
MAIL_DEFAULT_SENDER ='1007736246@qq.com'






