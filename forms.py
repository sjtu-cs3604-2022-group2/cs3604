from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import length, email, EqualTo
from models import Email, User
from wtforms.validators import DataRequired, Length
from flask_ckeditor import CKEditorField
from wtforms import SubmitField, StringField, RadioField, SelectMultipleField, IntegerField
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
    user_id1=IntegerField(label="user_id1")
    post_id1=IntegerField(label="post_id1")
    text_body1 = CKEditorField(label="text_body1", validators=[DataRequired()])
    new_floor1=IntegerField(label="new_floor1")
    submit1 = SubmitField(label="提交")


class CommentTowardsForm(FlaskForm):
    towards = IntegerField(label="towards")  # 这里是被评论的楼层
    comment_id=IntegerField(label="comment_id")  # 这里是被评论的comment的id
    post_id2=IntegerField(label="post_id2")
    user_id2=IntegerField(label="user_id2")
    text_body2 = CKEditorField(label="text_body2", validators=[DataRequired()])
    new_floor2=IntegerField(label="new_floor2")
    submit2 = SubmitField(label="提交")


class AddReplyPopForm(FlaskForm):
    user_id3=IntegerField(label="user_id3")
    post_id3=IntegerField(label="post_id3")
    text_body3 = CKEditorField(label="text_body3", validators=[DataRequired()])
    new_floor3=IntegerField(label="new_floor3")
    submit3 = SubmitField(label="提交")


class ReportForm(FlaskForm):
    report_post_id=IntegerField(label='report_post_id')
    report_floor = IntegerField(label="report_floor") #被举报的楼层。一楼(原post)的floor=-1
    report_comment_id=IntegerField(label="report_comment_id") #被举报的comment的id。如果被举报的是原post，值为-1
    report_user_id=IntegerField(label="report_user_id") #举报者
    reason = RadioField(
        label="Report_reason",
        validators=[DataRequired("请选择理由")],
        render_kw={"style": "list-style-type:none;margin-left:0px;text-align:left;padding-left:0px"},
        choices=[(0, "不实信息"), (1, "引战嫌疑"), (2, "不适当内容"), (3, "涉及抄袭"), (4, "其他")],
        coerce=int,
    )
    other_reason = StringField(label="other_reason",render_kw={'style':'outline:none;'})
    submit4 = SubmitField(label="提交")

class NewPostForm(FlaskForm):
    object_list = [(1, "开发测试"), (2, "动画"), (3, "小说"), (4, "游戏"),(5,"音乐"),(6,"体育")]
    title = StringField(label="title")
    post_text = CKEditorField(label="post_text", validators=[DataRequired()])
    categories = SelectMultipleField("categories", choices=object_list, coerce=int)
    submit = SubmitField(label="提交")


class ProfileForm(FlaskForm):
    user_id = IntegerField(label="user_id")
    username = StringField(label="username", validators=[length(1, 100)],
                           render_kw={"placeholder": "新用户名", "class": "input"})
    about = StringField(label="about", validators=[length(1, 100)], 
                        render_kw={"placeholder": "个人简介", "class": "input"})
    submit = wtforms.SubmitField(label="提交")
