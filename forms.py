import wtforms
from wtforms.validators import length, email, EqualTo
from models import Email,User


class LoginForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(1,10)])
    password = wtforms.StringField(validators=[length(6, 20)])


class RegisterForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(3, 20)])
    email = wtforms.StringField(validators=[email()])
    captcha = wtforms.StringField(validators=[length(4, 4)])
    password = wtforms.StringField(validators=[length(6, 20)])
    password_confirm = wtforms.StringField(validators=[EqualTo('password')])

    def validate_captcha(self, field):  ### 额外验证验证码是否和数据库中相同
        email = self.email.data
        captcha = field.data
        captchainModel = Email.query.filter_by(email=email).first()
        # print('数据库中的验证码为：', captchainModel.captcha)
        if not captchainModel or captchainModel.captcha.lower() != captcha.lower():
            raise wtforms.ValidationError('邮箱验证码错误')

    def validate_email(self, field):
        email = field.data
        record = User.query.filter_by(email=email).first()
        if record:
            raise wtforms.ValidationError('邮箱已经注册过')


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[length(1,100)])
    content = wtforms.StringField(validators=[length(1, 300)])
