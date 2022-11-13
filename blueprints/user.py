from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from flask_mail import Message
from extensions import mail, db
from models import User, Email
import string, random
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, LoginForm

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    registerform = RegisterForm()
    if form.submit1.data and form.validate():
        username = form.username.data
        password = form.password.data
        # flash(f'{username,password}')
        record = User.query.filter_by(username=username, password=password).first()
        if record:
            # g.user = record
            session['user_id']=record.id
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


@bp.route("/follows")
def follows():
    return render_template("user/followLs.html")


@bp.route("/selfcenter")
def selfcenter():
    return render_template("user/profile.html")


@bp.route("/logout")
def logout():
    session.clear()
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
    #         return redirect(url_for("user.register"))


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
