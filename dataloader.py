import random
import json
from faker import Faker
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from extensions import db
from models import *
from app import *


random.seed(42)
Faker.seed(42)
fake = Faker()


def random_relation(count, active):
    positive = random.randint(0, count-1)
    while (positive == active):
        positive = random.randint(0, count-1)
    return positive


def init_categories(count=10):
    print(f'create {count} Categories')
    for c in Category.query.all():
        db.session.delete(c)
    db.session.commit()
    category = Category(name="Default")
    db.session.add(category)
    for i in range(count):
        if i <= 4:
            names = ["动画", "小说", "游戏", "音乐", "体育"]
            category = Category(name=names[i])
        else:
            category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def init_user(count=20):
    print(f'create {count} Users')
    with open("./data/user.json", "r", encoding="utf8") as f:
        users = json.load(f)
    for u in User.query.all():
        db.session.delete(u)
    db.session.commit()
    user=User(username='test', password='123')
    db.session.add(user)
    for i in range(count):
        raw = users[i]
        user = User(
            username=raw["name"],
            password=fake.pystr(),
            email=fake.email(),
            join_time=fake.date_time_this_year(),
            about=raw["sign"],
            image=raw["face"],
        )
        db.session.add(user)
    db.session.commit()
    for u in User.query.all():
        for i in range(3):
            if getattr(u, 'id', 0):
                positive = random_relation(count, u.id)
                follow_u = User.query.get(positive)
                if follow_u:
                    u.follow(follow_u)
    db.session.commit()


def init_post(count=150):
    print(f'create {count} Posts')
    with open("./data/post_raw.json", "r", encoding="utf8") as f:
        posts = json.load(f)
    for p in Post.query.all():
        db.session.delete(p)
    db.session.commit()
    for i in range(count):
        raw = posts[i]
        post = Post(
            title=raw["title"],
            body=raw["body"],
            category_id=raw["category"]+1,
            timestamp=datetime.strptime(raw["time"][0], "%Y-%m-%d %H:%M"),
            user_id=random.randint(1, User.query.count()),
            num_likes=random.randint(10, 50),
            num_comments=raw["n_comment"],
            num_views=random.randint(50, 100),
        )
        db.session.add(post)
        db.session.commit()
        all_comment = raw['comment']+raw['sub_cmt']
        for j in range(raw['n_comment']):
            comment = Comment(
                body=all_comment[j],
                timestamp=datetime.strptime(raw["time"][j+1], "%Y-%m-%d %H:%M"),
                post_id=post.id,
                user_id=random.randint(1, User.query.count()),
            )
            post.comments.append(comment)
            db.session.add(comment)
            db.session.commit()
    db.session.commit()
    

def init_message():
    num_users = User.query.count()
    count = num_users*(num_users-1)//2
    print(f'create {count} Messages')
    for p in Message.query.all():
        db.session.delete(p)
    db.session.commit()
    for i in range(num_users):
        for j in range(num_users):
            if i == j:
                continue
            comment = Message(
                body=f"From {i+1} to {j+1}:"+fake.sentence(),
                timestamp=fake.date_time_this_year(),
                author=User.query.get(i+1),
                to_id=j+1
            )
            db.session.add(comment)
    db.session.commit()


if __name__ == "__main__":
    app = create_app('development')
    context = app.test_request_context()
    context.push()
    db.drop_all()
    db.create_all()
    init_categories()
    init_user()
    init_post()
    init_message()
    # init photo
    # init likes
    # init notifications