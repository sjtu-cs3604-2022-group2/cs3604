from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_mail import Message
from extensions import mail, db
from models import User, Email
import string, random
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, LoginForm

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        flash("请登录")
        return render_template("user/login.html")
    else:
        form = LoginForm(formdata=request.form)
        if form.validate():
            username = form.username.data
            password = form.password.data
            # flash(username, password)
            ### 到数据库中查找
            record = User.query.filter_by(username=username).first()
            if record and record.password == password:
                flash(f"hello,{record.username}")
                session["user_id"] = record.id
                return redirect("/")
            elif not record:
                flash("用户名未注册")
                return redirect(url_for("user.login"))
            else:
                flash("密码错误")
                return redirect(url_for("user.login"))
        else:
            flash("用户名或密码格式不正确")
            return redirect(url_for("user.login"))


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("user.login"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    """
    注册账号的逻辑是： 当用户输入邮箱，并点击“获取验证码” 后，服务器发送验证码邮件，并且将email and captcha 存入EmailModel中， 然后输入完整信息，之后会验证各项是否符合（包括验证码是否相同），
    然后会在UserModel中创建一条记录，并写入数据库。
    :return:
    """
    if request.method == "GET":
        return render_template("user/register.html")
    else:
        form = RegisterForm(request.form)
        # print(form.email.data)
        # print(form.username.data)
        # print(form.password.data)
        # print(form.captcha.data)
        if form.validate():
            flash("注册成功")
            ### md5(密码加密)
            hash_pass = generate_password_hash(password=form.password.data)
            user = User(email=form.email.data, username=form.username.data, password=hash_pass)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("user.login"))
        else:
            flash("注册未通过")
            return redirect(url_for("user.register"))


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
