from flask import Blueprint, render_template, g, flash, request, redirect, url_for,current_app,session
from decorators import login_request

from extensions import db

from models import Post,User

bp = Blueprint('posts', __name__)


@bp.route('/',defaults={'page':1})
@bp.route('/page/<int:page>')
@login_request
def index(page):
    user_id=int(session.get('user_id'))
    user=User.query.get(user_id)
    print(page)
    per_page = current_app.config['POST_PER_PAGE']
    print(per_page)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page=page, per_page=per_page)
    posts = pagination.items
    return render_template('posts/index-tmp.html', pagination=pagination, index_posts=posts,user=user)
    

@bp.route('/music')
def music():
    return "这是音乐分区"

@bp.route('/games')
def games():
    return "这是游戏分区"

@bp.route("/art")
def art():
    from fakes import real_post, real_categories, real_user
    real_categories()
    real_user()
    real_post()
    
    return "这是艺术分区"

@bp.route("/")
def sports():
    return "这是运动分区"



@bp.route('/search')
def search():
    pass
    









