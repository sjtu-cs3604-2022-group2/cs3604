import click,os
from flask import Flask, render_template, request,g
# from flask_login import current_user
from flask_sqlalchemy import get_debug_queries
from flask_wtf.csrf import CSRFError

# from bluelog.blueprints.blog import blog_bp

from models import Post, Category, Comment
# from extensions import bootstrap, db, csrf, ckeditor, mail, moment, toolbar, migrate
# from bluelog.settings import config
# from blueprints.user import bp as userbp
# from blueprints.posts import bp as postsbp
from setting import config
import models
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField,RadioField,SelectMultipleField
from wtforms . validators import DataRequired,Length
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField

from flask_ckeditor import CKEditorField

from flask_ckeditor import CKEditor

from blueprints import posts

from flask_dropzone import Dropzone,random_filename
from flask_wtf.file import FileField,FileAllowed,FileRequired
from blueprints import posts

current_user=models.User()
current_user.image='static/image/imgs_icons/boyphoto.svg'
current_user.username="Bob"

app = Flask(__name__)

@app.route('/search',methods=['GET'])
def search():
    args=request.args
    content=args.get('search-content')
    category=args.get('search-category')
    return '202'




mypost=Post(id=1,title='Title of the post')
othercomment=Comment(id=3,body='comment from other user (not current user)')

user1=models.User()
user1.image='static/image/imgs_icons/girlphoto.svg'
user1.username="Alice"

user2=current_user #just define another user

user3=models.User()
user3.image='static/image/imgs_icons/girlphoto1.svg'
user3.username="Cathy"

actions=['like','comment_to']
objects=['post','comment']

class notice:
    state=0 #0 或 1，未读 或 已读
    from_user=user1 #发起者
    action=0 #0 或 1，点赞/评论
    object=0 #0 或 1，被评论/点赞的是帖子还是回帖。
    object_detail=mypost # 第四列，可以是Post对象或者Comment对象
    link='#' #链接
    timestamp='2022.10.21 10:31' #时间

notice1=notice()
notice2=notice()
notice2.action=1
notice2.object=1
notice2.object_detail=othercomment
notice2.state=1

notices=[notice1,notice2]*5

@app.route('/')
def notification():
    return render_template('user/notification.html',current_user=current_user,
    notices=notices
    )

if __name__ == '__main__':
    app.run(debug = True)