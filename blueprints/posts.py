import os
import io
import random
import json
from PIL import Image
from flask import Blueprint, render_template, g, flash, request, redirect, url_for, current_app, session
from flask_login import login_required
from flask_dropzone import random_filename
from sqlalchemy import or_, and_
from flask_ckeditor import upload_success, upload_fail
import base64
from forms import AddReplyForm, CommentTowardsForm, AddReplyPopForm, ReportForm, NewPostForm
from extensions import db
from models import *
from utils import *
from abstraction import *
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
    pagination = (
        Post.query.filter(Post.valid == 1).order_by(Post.timestamp.desc()).paginate(page=page, per_page=per_page)
    )
    posts = pagination.items

    recommend_posts = CF_get_recommendation_posts(user_id)
    # recommend_posts = [Post.query.get(post_id) for post_id in recommend_posts_id]

    recommend_users = CF_get_recommendation_users(user_id)
    # recommend_users = [User.query.get(user_id) for user_id in recommend_users_id]

    return render_template(
        "posts/index-tmp-extend.html",
        pagination=pagination,
        index_posts=posts,
        current_user=user,
        recommend_posts=recommend_posts,
        recommend_users=recommend_users,
    )

@bp.route("/follow_posts", defaults={"page": 1})
@bp.route("/follow_posts/<int:page>")
def follow_posts(page):
    user_id = int(session.get("user_id"))
    user = User.query.get(user_id)
    per_page = current_app.config["POST_PER_PAGE"]
    followed_list = list()
    for relation in user.followed.all():
        followed_list.append(relation.followed.id)
    # print(followed_id)

    pagination = (
        Post.query.filter(and_(Post.valid == 1, Post.user_id.in_(followed_list)))
        .order_by(Post.timestamp.desc())
        .paginate(page=page, per_page=per_page)
    )

    posts = pagination.items

    recommend_posts = CF_get_recommendation_posts(user_id)
    # recommend_posts = [Post.query.get(post_id) for post_id in recommend_posts_id]

    recommend_users = CF_get_recommendation_users(user_id)
    # recommend_users = [User.query.get(user_id) for user_id in recommend_users_id]

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
    if not post or post.valid == 0:
        return render_template("errors/404.html")
    post_user = post.user
    user_id = session["user_id"]
    current_user = User.query.get(user_id)

    list_like_of_user = get_list_of_like(post_id, user_id)
    recommendation_users = CF_get_recommendation_users(user_id)
    recommendation_posts = CF_get_recommendation_posts(user_id)
    body_list = post.body.split("\n\r\n")
    # print(repr(post.body))
    post.num_views += 1
    db.session.commit()

    if current_user.is_admin:
        return render_template(
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
            recommend_posts=recommendation_posts,
            recommend_users=recommendation_users,
            likes=list_like_of_user,
            collections= current_user.favorites.all()
        )
    else:
        return render_template(
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
            recommend_posts=recommendation_posts,
            recommend_users=recommendation_users,
            likes=list_like_of_user,
            collections= current_user.favorites.all()
        )


from app import csrf
@csrf.exempt
@bp.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == "POST" and "file" in request.files:
        print("调用1次")
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
        return photo_path

        # redirect(url_for("posts.newpost", photo_path=os.path.join(upload_path, filename)))
    return "202"


@bp.route('/ckeditor_upload', methods=['POST'])
def ckeditor_upload():
    f = request.files.get('upload')  # 获取上传图片文件对象，键必须为'upload'
    # Add more validations here
    extension = f.filename.split('.')[1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg','bmp']:  # 验证文件类型示例
        return upload_fail(message='Image only!')  # 返回upload_fail调用

    filename = random_filename(f.filename)
    bts=f.stream.read()
    img = io.BytesIO(bts)
    img = Image.open(img)
    width,height=img.size

    max_width=795 #px
    scale=1
    if width>max_width:
        scale=max_width/width

    width*=scale
    height*=scale

    img = img.resize((int(width), int(height)), Image.ANTIALIAS)
    

    current_user = User.query.get(session["user_id"])
    upload_path = current_app.config["FILE_UPLOAD_PATH"]
    
    photo_path = url_for("static", filename="uploads/" + filename)
    img.save(os.path.join(upload_path, filename))
    # f.save(os.path.join(upload_path, filename))
    session["photo_nums"] = session.get("photo_nums", 0) + 1
    photo_num = session["photo_nums"]
    session[f"photo_{photo_num}"] = photo_path
    photo = Photo(filename=filename, user=current_user, photo_path=photo_path)
    db.session.add(photo)
    db.session.commit()
    return upload_success(url=photo_path)


@bp.route("/contributers", methods=["GET"])
def contributers():
    return render_template("posts/contributers.html")


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
    category = request.args.get("search_category", "帖子标题")
    # print(category)
    page = request.args.get("page", 1, type=int)

    per_page = current_app.config["POST_PER_PAGE"]
    recommend_posts = CF_get_recommendation_posts(user_id)
    recommend_users = CF_get_recommendation_users(user_id)
    # if category == "全局搜索":
    #     pagination = (
    #         Post.query.filter(
    #             or_(
    #                 Post.title.like("%" + srchterm + "%"),
    #                 Post.body.like("%" + srchterm + "%"),
    #                 User.username.like("%" + srchterm + "%"),
    #             )
    #         )
    #         .order_by(Post.timestamp.desc())
    #         .paginate(page=page, per_page=per_page)
    #     )
    #     posts = pagination.items
    if category == "帖子内容":
        pagination = (
            Post.query.filter(Post.body.like("%" + srchterm + "%"))
            .order_by(Post.timestamp.desc())
            .paginate(page=page, per_page=per_page)
        )
        posts = pagination.items
    elif category == "分区":
        post_category = Category.query.filter(Category.name == srchterm).first()
        pagination = (
            Post.query.with_parent(post_category).order_by(Post.timestamp.desc()).paginate(page=page, per_page=per_page)
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

    elif category == "帖子作者":
        # search_user= User.query.filter(User.username==srchterm)
        search_user = User.query.filter(User.username == srchterm).first()

        pagination = (
            Post.query.filter(
                Post.user_id == search_user.id,
            )
            .order_by(Post.timestamp.desc())
            .paginate(page=page, per_page=per_page)
        )
        posts = pagination.items
    elif category == "搜索用户":
        search_users = User.query.filter(User.username.like("%" + srchterm + "%")).all()
        # search_users = search_res.items

        return render_template(
            "user/users_show.html",
            search_users=search_users,
            recommend_posts=recommend_posts,
            recommend_users=recommend_users,
        )
    return render_template(
        "posts/index-tmp-extend.html",
        pagination=pagination,
        index_posts=posts,
        current_user=user,
        recommend_posts=recommend_posts,
        recommend_users=recommend_users,
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

        if comment_id == -1:
            obj = ObjectPost(post)

        else:
            reply = Comment.query.get(comment_id)
            obj = ObjectComment(reply, floor)

        action_like = ActionLike(user_id)
        action_like.set_object(obj)

        action_like.update_database()

        action_like.send_notification()

    return "202"


@csrf.exempt
@bp.route("/unlike", methods=["POST"])
def unlike():
    if request.method == "POST":
        form = request.form
        post_id = int(form["post_id"])
        comment_id = int(form["comment_id"])
        user_id = int(form["user_id"])
        floor = int(form["floor"])
        current_user = User.query.get(session["user_id"])

        if comment_id == -1:
            # 取消赞的是post本身
            post = Post.query.get(post_id)
            obj = ObjectPost(post)

        else:
            # 取消赞的是post下的评论
            reply = Comment.query.get(comment_id)
            obj = ObjectComment(reply, floor)

        action_unlike = ActionUnlike(user_id)
        action_unlike.set_object(obj)
        action_unlike.update_database()

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

        new_comment = Comment(body=body, from_author=from_author, user_id=action_id, towards=towards, post_id=post_id)

        action_reply = ActionReply(action_id, new_comment, new_floor)

        target_comment = Comment.query.get(comment_id)
        obj = ObjectComment(target_comment)

        action_reply.set_object(obj)

        action_reply.update_database()

        action_reply.send_notification()

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

        action_reply = ActionReply(action_id, comment, new_floor)

        post = Post.query.get(post_id)
        obj = ObjectPost(post)
        action_reply.set_object(obj)

        action_reply.update_database()

        action_reply.send_notification()

    return redirect(url_for("posts.detail", post_id=post_id))


@bp.route("/notifications")
def notifications():
    current_user = User.query.get(session["user_id"])
    notices = current_user.notifications
    return render_template("user/notification.html", current_user=current_user, notices=notices, User=User)


report_reasons = ["不实信息", "引战嫌疑", "不适当内容", "涉及抄袭"]


@bp.route("/report", methods=["POST"])
def report():
    if request.method == "POST":
        form = request.form
        post_id = int(form["report_post_id"])
        floor = int(form["report_floor"])  # -1 if post is reported
        comment_id = int(form["report_comment_id"])  # -1 if post is reported
        user_id = int(form["report_user_id"])
        reason = int(form["reason"])
        other_reason = form["other_reason"]  # empty if '其他' is not selected
        print(post_id, floor, comment_id, user_id, reason, other_reason)

        if reason < 4:
            reason_text = report_reasons[reason]
        else:
            reason_text = other_reason

        if comment_id == -1:
            post = Post.query.get(post_id)
            obj = ObjectPost(post)
        else:
            reply = Comment.query.get(comment_id)
            obj = ObjectComment(reply, floor)

        action_report = ActionReport(user_id, reason_text)
        action_report.set_object(obj)
        action_report.send_report()

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

        action_delete=ActionDelete(admin_id,reason)

        if comment_id == -1: 
            post = Post.query.get(post_id)
            obj=ObjectPost(post)
            
            action_delete.set_object(obj)
            action_delete.delete_object()
            action_delete.send_notification()

            redirect_url=url_for("posts.index")
            
        elif comment_id != -1:

            comment_1 = Comment.query.get(comment_id)

            obj=ObjectComment(comment_1,floor)

            action_delete.set_object(obj)
            action_delete.delete_object()
            action_delete.send_notification()

            redirect_url=url_for("posts.detail", post_id=post_id)

            if(0):

                association_comments = Comment.query.filter(
                    and_(
                        Comment.post_id == post_id,
                        Comment.towards == floor,
                    )
                ).all()
                
                for comment in association_comments:
                    obj=ObjectComment(comment)

                    action_delete.set_object(obj)
                    action_delete.delete_object()
                    action_delete.send_notification()

    return redirect(redirect_url)

# @csrf.exempt
# @bp.route("/admin_delete", methods=["POST"])
# def admin_delete():
#     if request.method == "POST":
#         form = request.form
#         post_id = int(form["delete_post_id"])
#         floor = int(form["delete_floor"])  # -1 if post is deleted
#         comment_id = int(form["delete_comment_id"])  # -1 if post is deleted
#         admin_id = int(form["delete_admin_id"])
#         reason = form["delete_reason"]

#         print(post_id, floor, comment_id, admin_id, reason)
#         # if floor.isdigit():
#         #     floor = int(floor)
#         if comment_id == -1:
#             post = Post.query.get(post_id)
#             post.valid = 0
#             for c in post.comments:
#                 c.valid = 0
#             notification = Notification(
#                 body=filter_body_content(Post.query.get(post_id).title),
#                 action=2,
#                 object=0,
#                 action_id=admin_id,
#                 user_id=Post.query.get(post_id).user.id,
#                 post_id=post_id,
#             )
#             db.session.add(notification)
#             db.session.commit()
#             return redirect(url_for("posts.index"))
#         elif comment_id != -1:

#             comment_1 = Comment.query.get(comment_id)
#             association_comments = Comment.query.filter(
#                 and_(
#                     Comment.post_id == post_id,
#                     Comment.towards == floor,
#                 )
#             ).all()
#             comment_1.valid = 0
#             notification1 = Notification(
#                 body=filter_body_content(comment_1.body),
#                 action=2,
#                 object=1,
#                 action_id=admin_id,
#                 user_id=comment_1.user.id,
#                 comment_id=comment_1.id,
#             )
#             db.session.add(notification1)
#             for comment in association_comments:
#                 comment.valid = 0
#                 notification = Notification(
#                     body=filter_body_content(comment.body),
#                     action=2,
#                     object=1,
#                     action_id=admin_id,
#                     user_id=comment.user.id,
#                     comment_id=comment.id,
#                 )
#                 db.session.add(notification)
#             db.session.commit()

#             return redirect(url_for("posts.detail", post_id=post_id))


@csrf.exempt
@bp.route("/read_notification", methods=["POST"])
def read_notification():
    form = request.form
    notice_id = int(form["notice_id"])
    notice = Notification.query.get(notice_id)
    notice.state = StateType.READ.value
    db.session.commit()
    return "202"


@bp.route("/admin_notifications")
def admin_notifications():
    current_user = User.query.get(session["user_id"])
    notices = current_user.notifications
    admin_notices = AdminNotification.query.all()
    return render_template(
        "user/admin-notification.html",
        current_user=current_user,
        notices=notices,
        admin_notices=admin_notices,
        User=User,
    )


@csrf.exempt
@bp.route("/read_admin_notification", methods=["POST"])
def read_admin_notification():
    form = request.form
    notice_id = int(form["admin_notice_id"])
    notice = AdminNotification.query.get(notice_id)
    notice.state = StateType.READ.value
    db.session.commit()
    return "202"


@csrf.exempt
@bp.route("/author_delete", methods=["POST"])
def author_delete():
    if request.method == "POST":
        form = request.form
        post_id = int(form["post_id"])
        user_id = int(form['user_id'])
        post = Post.query.get(post_id)
        obj = ObjectPost(post)
        action_delete = ActionDelete(user_id)
        action_delete.set_object(obj)
        action_delete.delete_object()
    return json.dumps({'url': url_for('posts.index')})


@csrf.exempt
@bp.route("/add_collection", methods=["POST"])
def add_collection():
    if request.method == "POST":
        form = request.form
        user_id = int(form['user_id'])
        new_name = form["new_collection_name"]

        # 给user新建名为new_name的收藏
        #获得新的收藏夹的id (new_id)
        user = User.query.get(user_id)
        collection = FavoriteCollection(user=user, name=new_name)
        db.session.add(collection)
        db.session.commit()
        new_id = collection.id
        dic = {"new_id": new_id}
        return json.dumps(dic)


@csrf.exempt
@bp.route("/favorite", methods=["POST"])
def favorite():
    if request.method == "POST":
        form = request.form
        user_id = int(form['user_id'])
        post_id = int(form['post_id'])
        collection_id = int(form['collection_id'])

        # 把post加入相应收藏夹
        user = User.query.get(user_id)
        post = Post.query.get(post_id)
        collection = FavoriteCollection.query.get(collection_id)
        user.add_favorite(post, collection)
    return "202"


@csrf.exempt
@bp.route("/cancel_favorite", methods=["POST"])
def cancel_favorite():
    if request.method == "POST":
        form = request.form
        user_id = int(form['user_id'])
        post_id = int(form['post_id'])

        # 把post取消收藏
        # 注意：默认将post从该用户的全部收藏夹中取消收藏
        user = User.query.get(user_id)
        post = Post.query.get(post_id)
        user.remove_favorite(post)
    return "202"




@csrf.exempt
@bp.route("/get_delete_record", methods=["POST"])
def get_delete_record():
    if request.method == "POST":
        form = request.form
        delete_record_id = int(form['delete_record_id'])
        record=DeleteRecord.query.get(delete_record_id)
        reason=record.reason
        original_link=record.original_link
        comment_id = record.comment_id
        post_id=record.post_id
        post=Post.query.get(post_id)
        title=post.title
        if(comment_id==-1):
             content=post.body
             obj=ObjectType.OBJECT_POST.value
        else:
            comment=Comment.query.get(comment_id)
            content=comment.body
            obj=ObjectType.OBJECT_COMMENT.value

        dic={"reason":reason,"original_link":original_link,
                "object":obj,"title":title,"content":content}
        return json.dumps(dic)
