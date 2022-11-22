# from unicodedata import category
from flask import Blueprint, render_template, g, flash, request, redirect, url_for, current_app, session
from decorators import login_request
from forms import AddReplyForm, CommentTowardsForm, AddReplyPopForm, ReportForm, NewPostForm
from extensions import db
import os
from models import Category, Photo, Post, User
from sqlalchemy import or_, and_
import random
# from 
bp = Blueprint("posts", __name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# upload_path = os.path.join(basedir, "uploads")


@bp.route("/", defaults={"page": 1})
@bp.route("/index")
@bp.route("/page/<int:page>")
@login_request
def index(page):
    user_id = int(session.get("user_id"))
    user = User.query.get(user_id)
    # print(page)
    per_page = current_app.config["POST_PER_PAGE"]
    # print(per_page)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page=page, per_page=per_page)
    posts = pagination.items
    cat_record = dict()
    for p in user.posts:
        cat_record[p.category_id] = cat_record.get(p.category_id, 0) + 1

    recommend_category = sorted(list(cat_record.keys()), key=lambda x: cat_record[x], reverse=True)[:2]
    print(recommend_category)
    recommend_posts = Post.query.filter(
        or_(Post.category_id == recommend_category[0], Post.category_id == recommend_category[1])
    ).all()
    recommend_posts = recommend_posts[:10]
    random.shuffle(recommend_posts)

    # for po in Post.query.filter(
    #     or_(
    #     Post.category_id==recommend_category[0],
    #     Post.category_id==recommend_category[1]
    #     )).all():

    return render_template(
        "posts/index-tmp-extend.html",
        pagination=pagination,
        index_posts=posts,
        current_user=user,
        recommend_posts=recommend_posts,
    )


@bp.route("/detail/<int:post_id>")
def detail(post_id):
    related1 = {"title": "Guide for beginner", "num_comments": 20}
    related2 = {"title": "Online Help", "num_comments": 30}
    related_topics = [related1, related2]

    recom1 = {"title": "Guide for art", "num_comments": 210}
    recom2 = {"title": "Guide for music", "num_comments": 230}
    recommendations = [recom1, recom2]
    add_reply_form = AddReplyForm()
    comment_towards_form = CommentTowardsForm()
    add_reply_pop_form = AddReplyPopForm()
    report_form = ReportForm()
    post = Post.query.get(post_id)
    user = post.user
    return render_template(
        "posts/detail-tmp-extend.html",
        User=User,
        current_user=User.query.get(session["user_id"]),
        post_user=user,
        topic=post,
        post=post,
        add_reply_form=add_reply_form,
        comment_towards_form=comment_towards_form,
        add_reply_pop_form=add_reply_pop_form,
        report_form=report_form,
        related_topics=related_topics,
        recommendations=recommendations,
    )


from app import  csrf
from flask_dropzone import random_filename
@csrf.exempt
@bp.route("/upload", methods=["POST","GET"])
def upload():  
    if request.method=='POST' and "file" in request.files:
        current_user= User.query.get(session['user_id'])
        f = request.files.get("file")
        filename = f.filename
        upload_path= current_app.config['FILE_UPLOAD_PATH']
        # print("filename:", filename)
        filename=random_filename(filename)
        f.save(os.path.join(upload_path, filename))
        photo=Photo(
            filename=filename,
            user=current_user   
        )
        db.session.add(photo)
        db.session.commit()
    return "202"


@bp.route("/textform", methods=["POST"])
def textform():
    return "202 "


@bp.route("/newpost", methods=["POST", "GET"])
def newpost():
    user_id = int(session.get("user_id"))
    current_user = User.query.get(user_id)
    new_post_form = NewPostForm()
    if request.method == "POST":
        print("hello word")
        title = new_post_form.title.data
        cat_id = new_post_form.categories.data[0]  ### 这里允许多分类，但是目前数据库里面一篇post对应一个分类。
        body = new_post_form.post_text.data[3:-6]  ### 去掉两边的标签
        # print(title,cat_id,body)
        new_post = Post(title=title, category_id=cat_id, body=body)
        new_post.user_id = user_id
        new_post.user = current_user
        db.session.add(new_post)
        db.session.commit()
        # return "已经成功提交"
        return redirect(url_for("posts.index"))

    return render_template("posts/newpost-tmp-extend.html", current_user=current_user, new_post_form=new_post_form)


@bp.route("/anime")
def anime():
    user_id = int(session.get("user_id"))
    user = User.query.get(user_id)
    per_page = current_app.config["POST_PER_PAGE"]
    pagination = (
        Post.query.filter(Post.category_id == 2).order_by(Post.timestamp.desc()).paginate(page=1, per_page=per_page)
    )
    posts = pagination.items
    return render_template("posts/index-tmp-extend.html", pagination=pagination, index_posts=posts, current_user=user)


@bp.route("/music")
def music():
    user_id = int(session.get("user_id"))
    user = User.query.get(user_id)
    per_page = current_app.config["POST_PER_PAGE"]
    pagination = (
        Post.query.filter(Post.category_id == 5).order_by(Post.timestamp.desc()).paginate(page=1, per_page=per_page)
    )
    posts = pagination.items
    return render_template("posts/index-tmp-extend.html", pagination=pagination, index_posts=posts, current_user=user)


@bp.route("/games")
def games():
    return "这是游戏分区"


@bp.route("/sport")
def sports():
    return "这是体育分区"


@bp.route("/local")
def local():
    from fakes import real_data_load

    real_data_load()

    return "从本地成功更新数据库"


# @bp.route("/search", methods=["GET", "POST"])
@bp.route("/search/")
def search():
    user_id = int(session.get("user_id"))
    user = User.query.get(user_id)
    srchterm = request.args.get("search_content", "")
    if srchterm == "":
        return redirect(request.referrer or url_for("posts.index"))
    # print(srchterm)
    category = request.args.get("search_category", "分区")
    print(category)
    page = request.args.get("page", 1, type=int)

    per_page = current_app.config["POST_PER_PAGE"]
    if category == "全局搜索":
        pagination = (
            Post.query.filter(
                or_(
                    Post.title.like("%" + srchterm + "%"),
                    Post.body.like("%" + srchterm + "%"),
                    User.username.like("%" + srchterm + "%"),
                )
            )
            .order_by(Post.timestamp.desc())
            .paginate(page=page, per_page=per_page)
        )
        posts = pagination.items
    elif category == "帖子内容":
        pagination = (
            Post.query.filter(Post.body.like("%" + srchterm + "%"))
            .order_by(Post.timestamp.desc())
            .paginate(page=page, per_page=per_page)
        )
        posts = pagination.items
    elif category == "分区":
        ### 分区还没写好
        post_category = Category.query.filter(Category.name == srchterm).first()
        pagination = (
            Post.query.with_parent(post_category).order_by(Post.timestamp.desc()).paginate(page=page, per_page=per_page)
        )
        # pagination = (
        #     # Category.query.filter(Category.name == srchterm)
        #     # .first()
        #     # .posts
        #     # .paginate(page=page, per_page=per_page)
        #     Post.query.filter( Category.query.get(Post.category_id).first().name == srchterm)

        #     .order_by(Post.timestamp.desc())
        #     .paginate(page=page, per_page=per_page)
        # )
        posts = pagination.items

    elif category == "帖子标题":
        pagination = (
            Post.query.filter(Post.title.like("%" + srchterm + "%"))
            .order_by(Post.timestamp.desc())
            .paginate(page=page, per_page=per_page)
        )
        posts = pagination.items

    # return url_for("search_result", search_content="")
    # return srchterm

    return render_template("posts/index-tmp-extend.html", pagination=pagination, index_posts=posts, current_user=user)
