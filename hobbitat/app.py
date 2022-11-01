from datetime import timedelta
from flask import Flask, session, g
import config
import os
from extensions import db, mail
from blueprints.posts import bp as posts_bp
from blueprints.user import bp as user_bp
from flask_migrate import Migrate
from models import UserModel
# from extensions import manager
from flask_script import Manager
app = Flask(__name__)
### 注册配置
app.config.from_object(config)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///'+ os.path.join(app.root_path, 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

### 初始化数据库
db.init_app(app)

### 初始化命令工具
migrate = Migrate(app, db)
###初始化邮件
mail.init_app(app)
manager=Manager(app)

### 注册蓝图
app.register_blueprint(user_bp)
app.register_blueprint(posts_bp)


### 客户端发送请求 -> before_request -> 视图函数 -> 视图函数要返回模板之前 —> context_processoer -> 模板

###钩子函数

@app.before_request
def before_request():
    user_id = session.get('user_id')
    if user_id:
        try:
            record = UserModel.query.get(user_id)
            ### g是一个全局变量，给g一个叫做user的变量
            setattr(g, 'user', record)
            ## g.user=user
        except:
            pass


@app.context_processor  ###上下文处理器，渲染的所有模板都会执行这个代码
def context_processor():
    if hasattr(g, 'user'):
        return {'user': g.user}
    else:
        return {}


if __name__ == '__main__':
    app.run()
