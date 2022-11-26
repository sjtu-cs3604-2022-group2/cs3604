import random
from models import Post, Comment, Message
from extensions import db
from app import *
from fakes import *


def change_comments_num_likes():
    comments=Comment.query.all()
    for comment in comments:
        comment.num_likes=random.randint(20,100)
    db.session.commit()
    

if __name__ == "__main__":
    # change_comments_num_likes()
    app = create_app('development')
    context = app.test_request_context()
    context.push()
    db.create_all()
    user=50; category=10; post=100
    real_categories(category)
    print(f'create categories: {category}')
    real_user(user)
    print(f'create user: {user}')
    real_post(post)
    print(f'create post: {post}')
    fake_message()
    