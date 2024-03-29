import os
import string
import random
from datetime import datetime
from collections import namedtuple
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g, current_app
from flask_mail import Message
from flask_login import login_user, logout_user, login_required, current_user
from flask_dropzone import random_filename
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import mail, db
from models import User, Email, Comment, Photo
from forms import RegisterForm, LoginForm, ProfileForm
from utils import *

bp = Blueprint("user", __name__, url_prefix="/user")


def change_comments_num_likes():
    comments = Comment.query.all()
    for comment in comments:
        comment.num_likes = random.randint(20, 100)
    db.session.commit()


@bp.route("/login", methods=["GET", "POST"])
def login():
    # change_comments_num_likes()
    form = LoginForm()
    registerform = RegisterForm()
    if form.submit1.data and form.validate():
        username = form.username.data
        password = form.password.data
        # flash(f'{username,password}')
        record = User.query.filter_by(username=username, password=password).first()
        if record:
            # g.user = record
            session["user_id"] = record.id
            # session["user"] = record
            login_user(record, remember=False)
            return redirect(url_for("posts.index"))
        else:
            flash("用户名或密码错误")
            return redirect(url_for("user.login"))
    if registerform.submit2.data and registerform.validate():
        user = User(
            username=registerform.username.data, password=registerform.password.data, email=registerform.email.data
        )
        db.session.add(user)
        db.session.commit()
        flash("已经成功注册")
        return redirect(url_for("user.login"))

    return render_template("user/login.html", form=form, registerform=registerform)


# @bp.route("/notifications", methods=["GET"])
# def notifications():
#     return render_template("user/notifications.html")


# @bp.route("/follows", methods=["GET"])
# def follows():
#     try:
#         id = session["user_id"]
#         user = User.query.get(id)
#     except:
#         return redirect(url_for("user.login"))
#     return render_template("user/friends-tmp.html", main_user=user)


@bp.route("/profile/<int:uid>", methods=["GET", "POST"])
def profile(uid):
    # 必须使用封装以实现valid的筛选，否则前端逻辑会很麻烦
    attrs_direct = ['id', 'username', 'about', 'image']
    attrs_verify = ['posts', 'photos', 'comments', 'like_posts', 'like_comments']
    attrs_follow = ['followers', 'followed']+['favorites']
    # ["followed", "followers"]: List[User]
    ValidUser = namedtuple('ValidUser', attrs_verify+attrs_direct+attrs_follow)
    
    def encapsulate(user: User):
        info = dict()
        for a in attrs_direct:
            info[a] = getattr(user, a)
        for a in attrs_verify:
            invalid = getattr(user, a)
            valid = []
            for o in invalid:  
                if hasattr(o, 'valid') and getattr(o, 'valid'):
                    # 'posts', 'comments', 'like_posts', 'like_comments'
                    valid.append(o)
                elif hasattr(o, 'post'):
                    # 'photos'
                    p = o.post
                    if p and p.valid:
                        valid.append(o)
            if valid and hasattr(valid[0], 'timestamp'):
                valid = sorted(valid, key=lambda x: x.timestamp, reverse=True)
            info[a] = valid
        info['followed'] = [r.followed for r in user.followed.all()]
        info['followers'] = [r.follower for r in user.followers.all()]
        info['favorites'] = [c for c in user.favorites.all()]
        return ValidUser(**info)
    
    profile_form = ProfileForm()

    id = session["user_id"]
    if uid == 0:
        uid = id
    user = User.query.get(id)
    user = encapsulate(user)
    visit_user = User.query.get(uid)
    visit_user = encapsulate(visit_user)
    recommend_posts = CF_get_recommendation_posts(uid)
    recommend_category = list(set([p.category.name for p in recommend_posts]))
    recommend_users = CF_get_recommendation_users(uid)

    return render_template(
        "user/profile-tmp.html",
        current_user=user,
        poster_user=visit_user,
        current_all_follower_id=[u.id for u in user.followed],
        profile_form=profile_form,
        recommend_posts=recommend_posts,
        recommend_user=recommend_users,
        recommend_category=recommend_category,
    )


from app import csrf, dropzone


@csrf.exempt
@bp.route("/profile_upload", methods=["POST"])
def profile_upload():
    user_id = session["user_id"]
    if "user_id" in request.form:
        form = request.form
        user_id = int(form.get("user_id"))
        new_name = form.get("username")
        about = form.get("about")
        user = User.query.get(user_id)
        user.username = new_name
        user.about = about
        db.session.commit()
    if "file" in request.files:
        user = User.query.get(user_id)
        f = request.files.get("file")
        filename = random_filename(f.filename)
        upload_path = os.path.join(current_app.config["FILE_UPLOAD_PATH"], filename)
        photo_path = url_for("static", filename="uploads/" + filename)
        f.save(upload_path)
        old_path = user.image
        old_photo = Photo.query.filter(Photo.photo_path==old_path).first()
        if old_photo:
            old_photo.destroy()
            db.session.delete(old_photo)
        photo = Photo(filename=filename,
                      user_id=user_id,
                      photo_path=photo_path)
        db.session.add(photo)
        user.image = photo_path
        db.session.commit()
        print(user.image)
    return redirect(url_for("user.profile", uid=user_id))


@csrf.exempt
@bp.route("/profile_follow", methods=["POST"])
def profile_follow():
    form = request.form
    if 'unfollow' in form:
        uid = session["user_id"]
        unfollow_id = int(form['unfollow'])
        user = User.query.get(uid)
        unfollow_user = User.query.get(unfollow_id)
        user.unfollow(unfollow_user)
        db.session.commit()
        current_poster_user_id = int(form['currentPage'])
        return redirect(url_for("user.profile", uid=current_poster_user_id))
    elif 'follow' in form:
        uid = session["user_id"]
        follow_id = int(form['follow'])
        user = User.query.get(uid)
        follow_user = User.query.get(follow_id)
        user.follow(follow_user)
        db.session.commit()
        current_poster_user_id = int(form['currentPage'])
        return redirect(url_for("user.profile", uid=current_poster_user_id))


# @bp.route("/chat")
# def chat():
#     chat = {
#         "url": "https://tse1-mm.cn.bing.net/th/id/OIP-C.4AJntm4bSRu9C2_h90WTfAAAAA?w=225&h=220&c=7&r=0&o=5&dpr=1.6&pid=1.7",
#         "rightuser": {"username": "sam"},
#         "message": [{"text": "hi"}, {"text": "nihao"}, {"text": "加个好友吧？"}],
#     }
#     return render_template("user/chat.html", chat=chat)


@bp.route("/logout")
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for("user.login"))

    # if request.method == "GET":
    #     return render_template("user/register.html")
    # else:
    #     form = RegisterForm(request.form)
    #     # print(form.email.data)
    #     # print(form.username.data)
    #     # print(form.password.data)
    #     # print(form.captcha.data)
    #     if form.validate():
    #         flash("注册成功")
    #         ### md5(密码加密)
    #         hash_pass = generate_password_hash(password=form.password.data)
    #         user = User(email=form.email.data, username=form.username.data, password=hash_pass)
    #         db.session.add(user)
    #         db.session.commit()
    #         return redirect(url_for("user.login"))
    #     else:
    #         flash("注册未通过")
    #         return redirect(url_for("user.registe                                                                             r"))


@bp.route("/captcha")
def get_captcha():
    address = request.args.get("email")  ### 通过get方法获得的邮箱地址
    chars = string.ascii_letters + string.digits
    captcha = "".join(random.sample(chars, 4))  ##随机生成的验证码
    message = Message(subject="发送验证码", recipients=[address], body=f"【Hobbitat】你的注册验证码是，{captcha}")
    record = Email.query.filter_by(email=address).first()

    if record:
        record.captcha = captcha
        record.create_time = datetime.now()
        db.session.commit()
    else:
        record = Email(email=address, captcha=captcha)
        db.session.add(record)
        db.session.commit()

    mail.send(message)
    return "success"
