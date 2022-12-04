from flask import render_template, redirect, url_for, request, Blueprint, current_app, abort, session
from flask_login import current_user, login_required
from flask_socketio import emit
from sqlalchemy import or_, and_
# import sys
# sys.path.append('c:\\PROJECTS\\new\\cs3604')
from extensions import socketio, db
# from forms import ProfileForm
from models import Message, User


chat_bp = Blueprint("chat", __name__, url_prefix="/chat")

online_users = []


@socketio.on('new message')
def new_message(message_body):
    uid = session.get('room', 0)
    html_message = message_body
    message = Message(author=current_user._get_current_object(), body=html_message, to_id=uid)
    db.session.add(message)
    db.session.commit()
    emit('new message',
        {'message_html': render_template('chat/_message.html', message=message),
        'message_body': html_message,
        'image': current_user.image,
        'username': current_user.username,
        'user_id': current_user.id},
        broadcast=True)


@socketio.on('new message', namespace='/anonymous')
def new_anonymous_message(message_body):
    html_message = message_body
    image = 'https://www.gravatar.com/avatar?d=mm'
    username = 'Anonymous'
    emit('new message',
         {'message_html': render_template('chat/_anonymous_message.html',
                                          message=html_message,
                                          image=image,
                                          username=username),
          'message_body': html_message,
          'image': image,
          'username': username,
          'user_id': current_user.id},
         broadcast=True, namespace='/anonymous')


@socketio.on('connect')
def connect():
    global online_users
    if current_user.is_authenticated and current_user.id not in online_users:
        online_users.append(current_user.id)
    emit('user count', {'count': len(online_users)}, broadcast=True)


@socketio.on('disconnect')
def disconnect():
    global online_users
    if current_user.is_authenticated and current_user.id in online_users:
        online_users.remove(current_user.id)
    emit('user count', {'count': len(online_users)}, broadcast=True)


@chat_bp.route('/', defaults={"uid": 1})
@chat_bp.route('/<int:uid>')
def home(uid):
    amount = current_app.config['CHAT_MESSAGE_PER_PAGE']
    session['room'] = uid
    print(f'\nnew room: {uid}')
    print('session now', session)
    messages = Message.query.filter(
        or_(
            and_(Message.author_id==current_user.id, Message.to_id==uid),
            and_(Message.author_id==uid, Message.to_id==current_user.id)
        )
    ).order_by(Message.timestamp.asc())[-amount:]
    user_amount = User.query.count()
    return render_template('chat/home.html', messages=messages, user_amount=user_amount, current_user=current_user)


@chat_bp.route('/anonymous')
def anonymous():
    return render_template('chat/anonymous.html')


@chat_bp.route('/messages')
def get_messages():
    page = request.args.get('page', 1, type=int)
    uid = session.get('room', 0)
    pagination = Message.query.filter(
        or_(
            and_(Message.author_id==current_user.id, Message.to_id==uid),
            and_(Message.author_id==uid, Message.to_id==current_user.id)
        )
    ).order_by(Message.timestamp.desc()).paginate(
        page, per_page=current_app.config['CHAT_MESSAGE_PER_PAGE'], error_out=False
    )
    messages = pagination.items
    return render_template('chat/_messages.html', messages=messages[::-1], current_user=current_user)


# @chat_bp.route('/profile', methods=['GET', 'POST'])
# @login_required
# def profile():
#     form = ProfileForm()
#     if form.validate_on_submit():
#         current_user.nickname = form.nickname.data
#         current_user.github = form.github.data
#         current_user.website = form.website.data
#         current_user.bio = form.bio.data
#         db.session.commit()
#         return redirect(url_for('.home'))
#     return render_template('chat/profile.html', form=form)


# @chat_bp.route('/profile/<user_id>')
# def get_profile(user_id):
#     user = User.query.get_or_404(user_id)
#     return render_template('chat/_profile_card.html', user=user)


@chat_bp.route('/message/delete/<message_id>', methods=['DELETE'])
def delete_message(message_id):
    if(request.method=='DELETE'):
        message = Message.query.get_or_404(message_id)
        if current_user != message.author and not current_user.is_admin:
            abort(403)
        db.session.delete(message)
        db.session.commit()
    return '', 204
