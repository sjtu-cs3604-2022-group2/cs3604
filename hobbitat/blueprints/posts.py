from flask import Blueprint, render_template, g, flash, request, redirect, url_for
from decorators import login_request

from extensions import db

bp = Blueprint('posts', __name__)


@bp.route('/')
def index():
    if hasattr(g, 'user'):
        flash(f'欢迎回来，{g.user.username}')
    return render_template('posts/index.html')
    # return 





