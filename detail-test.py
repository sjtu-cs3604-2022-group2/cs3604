import click,os
from flask import Flask, render_template, request,g
# from flask_login import current_user
from flask_sqlalchemy import get_debug_queries
from flask_wtf.csrf import CSRFError

# from bluelog.blueprints.blog import blog_bp

from models import Post, Category, Comment
from extensions import bootstrap, db, csrf, ckeditor, mail, moment, toolbar, migrate
# from bluelog.settings import config
from blueprints.user import bp as userbp
from blueprints.posts import bp as postsbp
from setting import config
import models
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField,RadioField
from wtforms . validators import DataRequired,Length
from flask_ckeditor import CKEditorField

from flask_ckeditor import CKEditor


current_user=models.User()
current_user.image='static/image/imgs_icons/boyphoto.svg'
current_user.username="Bob"

user1=models.User()
user1.image='static/image/imgs_icons/girlphoto.svg'
user1.username="Alice"

user2=current_user #just define another user

user3=models.User()
user3.image='static/image/imgs_icons/girlphoto1.svg'
user3.username="Cathy"

app = Flask(__name__)
ckeditor = CKEditor(app)

@app.route('/base')
def base():
    return render_template('base.html',current_user=current_user)

@app.route('/search')
def search():
    return 1


class AddReplyForm(FlaskForm):
    #title= StringField('Title', validators=[DataRequired() ,Length(1, 50)])
    text_body1 = CKEditorField( label='text_body1', validators= [ DataRequired () ])
    submit1 = SubmitField (label='提交')

class CommentTowardsForm(FlaskForm):
    towards=StringField(label='towards')
    text_body2 = CKEditorField( label='text_body2', validators= [ DataRequired () ])
    submit2 = SubmitField (label='提交')

class AddReplyPopForm(FlaskForm):
    text_body3 = CKEditorField( label='text_body3', validators= [ DataRequired () ])
    submit3 = SubmitField (label='提交')

class ReportForm(FlaskForm):
    towards=StringField(label='towards')
    reason= RadioField(
        label='Report_reason',
        validators=[DataRequired('请选择理由')],
        render_kw={
            'style': 'list-style-type:none;margin-left:0px;text-align:left;padding-left:0px'
        },
        choices=[(1, '不实信息'), (2, '引战嫌疑'), (3, '不适当内容'),(4,'涉及抄袭'),(5,'其他')],
        
        coerce=int
    )
    other_reason=StringField(label="other_reason")
    submit4= SubmitField (label='提交')

cat=Category()
cat.id=0
cat.name="音乐"

class comment:
    responder=current_user
    text=['Even when our position and our character seem to remain precisely the same, they are changing, for the mere advance of time is a change.'
    ,'Even when our position and our character seem to remain precisely the same, they are changing, for the mere advance of time is a change.']
    num_likes=1
    time='2022.1.31 10:33'
    towards=1

class Topic:
    poster=user1
    title = 'HELLO THERE'
    text=['Wherever you are, and whoever you may be, there is one thing in which you and I are just alike at this moment, all in all the moments of our existence. We are not at rest; we are on a journey. Our life is a movement, a tendency, a steady, ceaseless progress towards an unseen goal. '
    ,'Wherever you are, and whoever you may be, there is one thing in which you and I are just alike at this moment, all in all the moments of our existence. We are not at rest; we are on a journey. Our life is a movement, a tendency, a steady, ceaseless progress towards an unseen goal. ']
    image='static/image/imgs_icons/guitar.jpg'
    category=cat


comment1=comment()
comment1.responder=user2
comment2=comment()
comment2.responder=user3
comment2.towards=2

class DetailPost:
    num_views=4
    num_likes=1
    num_comments=2
    post_time='2022 10.31'
    comments=[comment1,comment2]

topic=Topic()
post=DetailPost()

related1={'title':'Guide for beginner','num_comments':20}
related2={'title':'Online Help','num_comments':30}
related_topics=[related1,related2]

recom1={'title':'Guide for art','num_comments':210}
recom2={'title':'Guide for music','num_comments':230}
recommendations=[recom1,recom2]

app.config['SECRET_KEY']='AASDFASDF'

@app.route('/')
def detail():
    add_reply_form=AddReplyForm()
    comment_towards_form=CommentTowardsForm()
    add_reply_pop_form=AddReplyPopForm()
    report_form=ReportForm()
    return render_template('posts/detail-tmp-extend.html',
                            current_user=current_user,
                            topic=topic,
                            post=post,
                            add_reply_form=add_reply_form,
                            comment_towards_form=comment_towards_form,
                            add_reply_pop_form=add_reply_pop_form,
                            report_form=report_form,
                            related_topics=related_topics,
                            recommendations=recommendations
                            )

if __name__ == '__main__':
    app.run(debug = True)