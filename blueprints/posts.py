# from unicodedata import category
from flask import Blueprint, render_template, g, flash, request, redirect, url_for, current_app, session
from decorators import login_request
from forms import AddReplyForm, CommentTowardsForm, AddReplyPopForm, ReportForm, NewPostForm
from extensions import db
import os
from models import Post, User
from sqlalchemy import or_,and_
bp = Blueprint("posts", __name__)
basedir = os.path.abspath(os.path.dirname(__file__))
upload_path = os.path.join(basedir, "upload")


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
    return render_template("posts/index-tmp-extend.html", pagination=pagination, index_posts=posts, current_user=user)


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


@bp.route("/upload", methods=["POST"])
def upload():
    if "file" in request.files:
        f = request.files.get("file")
        filename = f.filename
        f.save(os.path.join(upload_path, filename))
    return "202"


@bp.route("/textform", methods=["POST"])
def textform():
    return "202 "


@bp.route("/newpost")
def newpost():
    user_id = int(session.get("user_id"))
    current_user = User.query.get(user_id)
    new_post_form = NewPostForm()
    return render_template("posts/newpost-tmp-extend.html", current_user=current_user, new_post_form=new_post_form)


@bp.route("/music")
def music():
    return "这是音乐分区"


@bp.route("/games")
def games():
    return "这是游戏分区"


@bp.route("/art")
def art():
    from fakes import real_data_load

    real_data_load()

    return "这是艺术分区"


@bp.route("/sport")
def sports():
    return "这是运动分区"


@bp.route("/search", methods=["GET", "POST"])
@bp.route("/search_result")
def search():
    user_id = int(session.get("user_id"))
    user = User.query.get(user_id)
    srchterm = request.args.get("srch-term", "")
    if srchterm == "":
        return redirect(request.referrer or url_for("posts.index"))
    print(srchterm)
    category = "全局搜索"
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
