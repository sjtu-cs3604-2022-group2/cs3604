import string
import random
from datetime import datetime
from collections import namedtuple

# from app import change_comments_num_likes
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from flask_mail import Message
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import mail, db
from models import User, Email, Comment
from forms import RegisterForm, LoginForm



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
        # if username=='zkn' and password=='111':
        #     flash('登陆成功')
        #     return redirect(url_for('posts.index'))
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


@bp.route("/notifations", methods=["GET"])
def notifations():
    return render_template("user/notifations.html")

@bp.route("/follows", methods=["GET"])
def follows():
    Current = namedtuple("Current", ["image", "username", "follow", "posts"])
    try:
        id = session["user_id"]
        user = User.query.get(id)
        followers = [f.followed for f in user.followed.all()]
        current_user = Current(user.image, user.username, followers, user.posts)
    except:
        return redirect(url_for("user.login"))
    return render_template("user/friends-tmp.html", main_user=current_user)


@bp.route("/selfcenter")
def selfcenter():
    Current = namedtuple("Current", ["image", "username", "follow", "posts"])
    try:
        id = session["user_id"]
        user = User.query.get(id)
        followers = [f.followed for f in user.followed.all()]
        current_user = Current(user.image, user.username, followers, user.posts)
    except:
        return redirect(url_for("user.login"))
    return render_template("user/profile-tmp.html", current_user=current_user, poster_user=current_user)


@bp.route("/chat")
def chat():
    chat = {
        "url": "https://tse1-mm.cn.bing.net/th/id/OIP-C.4AJntm4bSRu9C2_h90WTfAAAAA?w=225&h=220&c=7&r=0&o=5&dpr=1.6&pid=1.7",
        "rightuser": {"username": "sam"},
        "message": [{"text": "hi"}, {"text": "nihao"}, {"text": "加个好友吧？"}],
    }
    return render_template("user/chat.html", chat=chat)


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
    message = Message(subject="发送验证码", recipients=[address], body=f"【康宁问答】你的注册验证码是，{captcha}")
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

    # return 'success'
