from flask import Blueprint, render_template, g, flash, request, redirect, url_for
from decorators import login_request

from forms import QuestionForm
from extentions import db
from models import QuestionModel

bp = Blueprint('posts', __name__)


@bp.route('/')
def index():
    if hasattr(g, 'user'):
        flash(f'欢迎回来，{g.user.username}')
    return render_template('posts/index.html')
    # return 


@bp.route('/public/question', methods=['GET', 'POST'])
@login_request  # ## 要先判断是否登录
def public_question():
    if request.method == 'GET':
        return render_template("public_question.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            record = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(record)
            db.session.commit()
            return redirect(url_for('qa.index'))
        else:
            flash('标题或内容格式错误')
            return render_template("public_question.html")

@bp.route("/question/<int:question_id>")
def question_detail(question_id):
    question=QuestionModel.query.get(question_id)
    return render_template("detail.html",question=question)


