import os
import random
from flask import Blueprint, render_template, g, flash, request, redirect, url_for, current_app, session
from flask_login import login_required
from flask_dropzone import random_filename
from sqlalchemy import or_, and_
from forms import AddReplyForm, CommentTowardsForm, AddReplyPopForm, ReportForm, NewPostForm
from extensions import db
from models import Category, Photo, Post, User, Comment, Notification
from utils import *
from abstract_factory import AbstractAction
from actiontype import *
from datetime import datetime


bp = Blueprint("posts", __name__)
basedir = os.path.abspath(os.path.dirname(__file__))


@bp.route("/", defaults={"page": 1})
@bp.route("/index", defaults={"page": 1})
@bp.route("/page/<int:page>")
@login_required
def index(page):
    user_id = int(session.get("user_id"))
    user = User.query.get(user_id)
    per_page = current_app.config["POST_PER_PAGE"]
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page=page, per_page=per_page)
    posts = pagination.items
    # cat_record = dict()
    # CF_get_recommendation_users()
    # compute_user_similar()
    # for p in user.posts.all():
    #     cat_record[p.category_id] = cat_record.get(p.category_id, 0) + 1

    # recommend_category = sorted(list(cat_record.keys()), key=lambda x: cat_record[x], reverse=True)[:2]
    # print(recommend_category)
    # if len(recommend_category) >= 2:
    #     recommend_posts = Post.query.filter(
    #         or_(Post.category_id == recommend_category[0], Post.category_id == recommend_category[1])
    #     ).all()
    #     recommend_posts = recommend_posts[:10]
    # else:
    #     recommend_posts = []
    # random.shuffle(recommend_posts)
    recommend_posts_id = CF_get_recommendation_posts(user_id)
    recommend_posts = [Post.query.get(post_id) for post_id in recommend_posts_id]

    recommend_users_id = CF_get_recommendation_users(user_id)
    recommend_users = [User.query.get(user_id) for user_id in recommend_users_id]

    return render_template(
        "posts/index-tmp-extend.html",
        pagination=pagination,
        index_posts=posts,
        current_user=user,
        recommend_posts=recommend_posts,
        recommend_users=recommend_users,
    )


@bp.route("/detail/<int:post_id>")
def detail(post_id):
    related1 = {"title": "Guide for beginner", "num_comments": 20}
    related2 = {"title": "Online Help", "num_comments": 30}
    related_topics = [related1, related2]
    add_reply_form = AddReplyForm()
    comment_towards_form = CommentTowardsForm()
    add_reply_pop_form = AddReplyPopForm()
    report_form = ReportForm()
    post = Post.query.get(post_id)
    post_user = post.user
    user_id = session["user_id"]
    current_user = User.query.get(user_id)
    if post.valid == 0:
        return render_template("errors/404.html")

    list_like_of_user = get_list_of_like(post_id, user_id)
    recommendation_post = get_recommendation_posts(user_id)
    body_list = post.body.split("\n\r\n")
    # print(repr(post.body))
    if current_user.is_admin:

        return render_template(
            # "posts/detail-tmp-extend.html",
            "posts/admin-detail.html",
            User=User,
            current_user=current_user,
            post_user=post_user,
            topic=post,
            body_list=body_list,
            post=post,
            add_reply_form=add_reply_form,
            comment_towards_form=comment_towards_form,
            add_reply_pop_form=add_reply_pop_form,
            report_form=report_form,
            related_topics=related_topics,
            recommend_posts=recommendation_post,
            likes=list_like_of_user,
        )
    else:
        return render_template(
            # "posts/detail-tmp-extend.html",
            "posts/detail-tmp-extend.html",
            User=User,
            current_user=current_user,
            post_user=post_user,
            topic=post,
            body_list=body_list,
            post=post,
            add_reply_form=add_reply_form,
            comment_towards_form=comment_towards_form,
            add_reply_pop_form=add_reply_pop_form,
            report_form=report_form,
            related_topics=related_topics,
            recommend_posts=recommendation_post,
            likes=list_like_of_user,
        )


from app import csrf


@csrf.exempt
@bp.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == "POST" and "file" in request.files:
        current_user = User.query.get(session["user_id"])
        f = request.files.get("file")
        session["photo_nums"] = session.get("photo_nums", 0) + 1
        photo_num = session["photo_nums"]
        filename = f.filename
        upload_path = current_app.config["FILE_UPLOAD_PATH"]
        print(upload_path)
        # print("filename:", filename)
        filename = random_filename(filename)
        photo_path = url_for("static", filename="uploads/" + filename)
        print("当前上传的文件数为：", photo_num)
        session[f"photo_{photo_num}"] = photo_path
        f.save(os.path.join(upload_path, filename))
        photo = Photo(filename=filename, user=current_user, photo_path=photo_path)
        db.session.add(photo)
        db.session.commit()

        # redirect(url_for("posts.newpost", photo_path=os.path.join(upload_path, filename)))
    return "202"


@bp.route("/textform", methods=["POST"])
def textform():
    return "202 "


# @bp.route("/newpost/<string:photo_path>", methods=["POST", "GET"])
@bp.route("/newpost", methods=["POST", "GET"])
def newpost():
    user_id = int(session.get("user_id"))
    current_user = User.query.get(user_id)
    new_post_form = NewPostForm()
    if request.method == "GET":
        # session['']
        session["photo_nums"] = 0
    if request.method == "POST":
        # print("hello word")
        title = new_post_form.title.data
        cat_id = new_post_form.categories.data[0]  ### 这里允许多分类，但是目前数据库里面一篇post对应一个分类。
        body = new_post_form.post_text.data  ### ，没有去掉两边的标签
        # print(title,cat_id,body)
        new_post = Post(title=title, category_id=cat_id, body=body)
        # new_post.timestamp = datetime.strptime(new_post.timestamp, "%Y-%m-%d %H:%M")
        new_post.user_id = user_id
        new_post.user = current_user
        if session["photo_nums"] > 0:  ### 这里session的值是在upload视图里面改变的
            for i in range(1, session["photo_nums"] + 1):
                photo_path = session[f"photo_{i}"]
                print("上传的图片路径为", photo_path)
                photo = Photo.query.filter(Photo.photo_path == photo_path).first()
                # print()
                new_post.photos.append(photo)
        # print(photo_path)
        # if photo_path is not None:
        #     photo = Photo.query.filter(Photo.photo_path == photo_path).first()

        #     new_post.photos.append(photo)

        # photo=current_user.photos[-1]

        db.session.add(new_post)
        # new_post.timestamp = datetime.strptime(new_post.timestamp, "%Y-%m-%d %H:%M")

        db.session.commit()

        # new_post.timestamp = datetime.strptime(new_post.timestamp, "%Y-%m-%d %H:%M")
        # print(new_post.timestamp.strftime("%y-%m-%d %I:%M:%S %p"))
        # db.session.commit()

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
    # print(category)
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
    recommend_posts = get_recommendation_posts(user_id)

    return render_template(
        "posts/index-tmp-extend.html",
        pagination=pagination,
        index_posts=posts,
        current_user=user,
        recommend_posts=recommend_posts,
    )


def get_list_of_like(post_id, user_id):
    post = Post.query.get(post_id)
    commentsofpost = post.comments
    user = User.query.get(user_id)
    user_like_comments_id = set()
    for comment in user.like_comments:
        user_like_comments_id.add(comment.id)

    list_like_of_user = [0 for _ in range(len(commentsofpost) + 1)]

    if post in user.like_posts:
        list_like_of_user[0] = 1

    for i in range(1, len(commentsofpost) + 1):
        if commentsofpost[i - 1].id in user_like_comments_id:
            list_like_of_user[i] = 1

    return list_like_of_user


@csrf.exempt
@bp.route("/like", methods=["POST"])
def like():
    if request.method == "POST":
        form = request.form
        post_id = int(form["post_id"])
        comment_id = int(form["comment_id"])
        user_id = int(form["user_id"])
        floor = int(form["floor"])  # 被点赞的楼层，用于生成链接
        current_user = User.query.get(session["user_id"])
        post = Post.query.get(post_id)

        action_like = AbstractAction(
            post_id=post_id, cur_user_id=current_user.id, floor=floor, reply_id=comment_id
        ).set_action(OptionType.LIKE)

        if comment_id == -1:

            complete_action = action_like.to_a_post()
            print("添加点赞post通知")

        else:

            complete_action = action_like.to_a_reply()
            print("添加点赞comment通知")

    complete_action.update_likes()

    complete_action.send_notification()
    return "202"


@csrf.exempt
@bp.route("/unlike", methods=["POST"])
def unlike():
    if request.method == "POST":
        form = request.form
        post_id = int(form["post_id"])
        comment_id = int(form["comment_id"])
        user_id = int(form["user_id"])
        print(post_id, comment_id, user_id)
        current_user = User.query.get(session["user_id"])

        if comment_id == -1:
            # 取消赞的是post本身，更新数据库
            post = Post.query.get(post_id)
            current_user.like_posts.remove(post)
            post.num_likes -= 1
            db.session.commit()
            print("移除成功")
        else:
            # 取消赞的是post下的评论，评论id为comment_id，更新数据库
            # pass
            #
            comment = Comment.query.get(comment_id)
            current_user.like_comments.remove(comment)

            comment.num_likes -= 1

            db.session.commit()

    return "202"


@bp.route("/comment_towards", methods=["POST"])
def comment_towards():
    if request.method == "POST":
        form = request.form
        post_id = int(form["post_id2"])  # 被回复的comment所属的帖子id，用于生成链接
        towards = int(form["towards"])  # 被回复的楼层，用于渲染页面
        body = form["text_body2"]  # 回复内容
        action_id = int(form["user_id2"])  # 动作发起者的id
        comment_id = int(form["comment_id"])  # 被回复的comment的id，用于寻找该comment的作者，并向其发送通知
        new_floor = int(form["new_floor2"])

        user_id = Comment.query.get(comment_id).user_id

        if action_id == user_id:
            from_author = True
        else:
            from_author = False

        comment = Comment(body=body, from_author=from_author, user_id=action_id, towards=towards, post_id=post_id)

        # comment.timestamp = datetime.strptime(comment.timestamp, "%Y-%m-%d %H:%M")

        action_comment = AbstractAction(
            post_id=post_id, cur_user_id=user_id, floor=new_floor, reply_id=comment_id, comment_body=body
        ).set_action(OptionType.COMMENT)

        complete_action = action_comment.to_a_reply()

        complete_action.update_comments(comment)
        complete_action.send_notification()

    return redirect(url_for("posts.detail", post_id=post_id))


@bp.route("/add_reply/<int:type_of_form>", methods=["POST"])
def add_reply(type_of_form):
    if request.method == "POST":
        form = request.form
        type_of_form = str(type_of_form)
        post_id = int(form["post_id" + type_of_form])  # 被回复的帖子id，用于生成链接,寻找该post的作者，并向其发送通知
        body = form["text_body" + type_of_form]  # 回复内容
        action_id = int(form["user_id" + type_of_form])  # 动作发起者的id
        new_floor = int(form["new_floor" + type_of_form])  # 新增楼层，用于生成链接

        user_id = Post.query.get(post_id).user_id
        if action_id == user_id:
            from_author = True
        else:
            from_author = False

        comment = Comment(body=body, from_author=from_author, post_id=post_id, towards=-1, user_id=action_id)

        action_comment = AbstractAction(
            post_id=post_id, cur_user_id=user_id, floor=new_floor, reply_id=-1, comment_body=body
        ).set_action(OptionType.COMMENT)

        complete_action = action_comment.to_a_post()
        complete_action.update_comments(comment)
        complete_action.send_notification()

    return redirect(url_for("posts.detail", post_id=post_id))


@bp.route("/notifications")
def notifications():
    current_user = User.query.get(session["user_id"])
    notices = current_user.notifications
    return render_template("user/notification.html", current_user=current_user, notices=notices, User=User)


@bp.route("/report", methods=["POST"])
def report():
    if request.method == "POST":
        form = request.form
        post_id = form["report_post_id"]
        floor = form["report_floor"]  # -1 if post is reported
        comment_id = form["report_comment_id"]  # -1 if post is reported
        user_id = form["report_user_id"]
        reason = form["reason"]
        other_reason = form["other_reason"]  # empty if '其他' is not selected
        print(post_id, floor, comment_id, user_id, reason, other_reason)

    return redirect(url_for("posts.detail", post_id=post_id))


@csrf.exempt
@bp.route("/admin_delete", methods=["POST"])
def admin_delete():
    if request.method == "POST":
        form = request.form
        post_id = int(form["delete_post_id"])
        floor = int(form["delete_floor"])  # -1 if post is deleted
        comment_id = int(form["delete_comment_id"])  # -1 if post is deleted
        admin_id = int(form["delete_admin_id"])
        reason = form["delete_reason"]

        print(post_id, floor, comment_id, admin_id, reason)
        # if floor.isdigit():
        #     floor = int(floor)
        if comment_id == -1:
            post = Post.query.get(post_id)
            post.valid = 0
            for c in post.comments:
                c.valid = 0
        elif comment_id != -1:

            comment_1 = Comment.query.get(comment_id)
            association_comments = Comment.query.filter(
                and_(
                    Comment.post_id == post_id,
                    Comment.towards == floor,
                )
            ).all()
            comment_1.valid = 0
            for comment in association_comments:
                comment.valid = 0

        db.session.commit()

    return redirect(url_for("posts.detail", post_id=post_id))
