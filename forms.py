from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import length, email, EqualTo
from models import Email, User
from wtforms.validators import DataRequired, Length
from flask_ckeditor import CKEditorField
from wtforms import SubmitField, StringField, RadioField, SelectMultipleField
from flask_ckeditor import CKEditor


class LoginForm(FlaskForm):
    username = wtforms.StringField(
        "username", validators=[length(1, 10)], render_kw={"placeholder": "用户名/邮箱", "class": "input"}
    )
    password = wtforms.StringField(
        "password", validators=[length(1, 20)], render_kw={"placeholder": "密码", "class": "input"}
    )
    submit1 = wtforms.SubmitField("登录")


class RegisterForm(FlaskForm):
    username = wtforms.StringField(
        "username", validators=[length(1, 20)], render_kw={"placeholder": "用户名", "class": "input"}
    )
    email = wtforms.StringField("email", validators=[email()], render_kw={"placeholder": "邮箱", "class": "input"})
    captcha = wtforms.StringField(
        "captcha", validators=[length(4, 4)], render_kw={"placeholder": "验证码", "class": "input"}
    )
    password = wtforms.StringField(
        "password", validators=[length(1, 20)], render_kw={"placeholder": "密码", "class": "input"}
    )
    password_confirm = wtforms.StringField(
        "password_confirm", validators=[EqualTo("password")], render_kw={"placeholder": "再次填入密码", "class": "input"}
    )
    submit2 = wtforms.SubmitField("注册")

    # def validate_captcha(self, field):  ### 额外验证验证码是否和数据库中相同
    #     email = self.email.data
    #     captcha = field.data
    #     captchainModel = Email.query.filter_by(email=email).first()
    #     # print('数据库中的验证码为：', captchainModel.captcha)
    #     if not captchainModel or captchainModel.captcha.lower() != captcha.lower():
    #         raise wtforms.ValidationError('邮箱验证码错误')

    # def validate_email(self, field):
    #     email = field.data
    #     record = User.query.filter_by(email=email).first()
    #     if record:
    #         raise wtforms.ValidationError('邮箱已经注册过')
    # def validate_csrf_token(self, field):
    #     if not self.csrf_enabled:
    #         return True


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[length(1, 100)])
    content = wtforms.StringField(validators=[length(1, 300)])


class AddReplyForm(FlaskForm):
    # title= StringField('Title', validators=[DataRequired() ,Length(1, 50)])
    text_body1 = CKEditorField(label="text_body1", validators=[DataRequired()])
    submit1 = SubmitField(label="提交")


class CommentTowardsForm(FlaskForm):
    towards = StringField(label="towards")
    text_body2 = CKEditorField(label="text_body2", validators=[DataRequired()])
    submit2 = SubmitField(label="提交")


class AddReplyPopForm(FlaskForm):
    text_body3 = CKEditorField(label="text_body3", validators=[DataRequired()])
    submit3 = SubmitField(label="提交")


class ReportForm(FlaskForm):
    towards = StringField(label="towards")
    reason = RadioField(
        label="Report_reason",
        validators=[DataRequired("请选择理由")],
        render_kw={"style": "list-style-type:none;margin-left:0px;text-align:left;padding-left:0px"},
        choices=[(1, "不实信息"), (2, "引战嫌疑"), (3, "不适当内容"), (4, "涉及抄袭"), (5, "其他")],
        coerce=int,
    )
    other_reason = StringField(label="other_reason")
    submit4 = SubmitField(label="提交")


class NewPostForm(FlaskForm):
    object_list = [(0, "音乐"), (1, "艺术"), (2, "运动"), (3, "游戏")]
    title = StringField(label="title")
    post_text = CKEditorField(label="post_text", validators=[DataRequired()])
    categories = SelectMultipleField("categories", choices=object_list, coerce=int)
    submit = SubmitField(label="提交")
