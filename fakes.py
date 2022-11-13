import random
import json
from faker import Faker
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from extensions import db
from models import Category, Post, Comment, User


fake = Faker()


def fake_user(count=5):
    for _ in range(count):
        user = User(
            username=fake.name(),
            about="hello",
            password=fake.pystr(),
        )
        db.session.add(user)
    db.session.commit()


def fake_categories(count=10):
    category = Category(name="Default")
    db.session.add(category)

    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_posts(count=50):
    for i in range(count):
        post = Post(
            title=fake.sentence(),
            body=fake.text(100),
            category_id=random.randint(1, Category.query.count()),
            timestamp=fake.date_time_this_year(),
            user_id=random.randint(1, User.query.count()),
            num_likes=random.randint(10, 50),
            num_comments=random.randint(0, 10),
            num_views=random.randint(50, 100),
        )

        db.session.add(post)
    db.session.commit()


def fake_comments(count=500):
    for i in range(count):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            post=Post.query.get(random.randint(1, Post.query.count())),
        )
        db.session.add(comment)

    salt = int(count * 0.1)
    for i in range(salt):
        # from user
        comment = Comment(
            author="Mima Kirigoe",
            email="mima@example.com",
            site="example.com",
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            from_author=True,
            post=Post.query.get(random.randint(1, Post.query.count())),
        )
        db.session.add(comment)
    db.session.commit()

    # replies
    for i in range(salt):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            replied=Comment.query.get(random.randint(1, Comment.query.count())),
            post=Post.query.get(random.randint(1, Post.query.count())),
        )
        db.session.add(comment)
    db.session.commit()


def real_post(count=100):
    with open("./data/post.json", "r", encoding="utf8") as f:
        posts = json.load(f)
    for p in Post.query.all():
        db.session.delete(p)
    db.session.commit()
    for i in range(count):
        raw = posts[i]
        post = Post(
            title=raw["title"],
            body=raw["body"],
            category_id=raw["category"],
            timestamp=datetime.strptime(raw["time"][0], "%Y-%m-%d %H:%M"),
            user_id=random.randint(1, User.query.count()),
            num_likes=random.randint(10, 50),
            num_comments=raw["n_comment"],
            num_views=random.randint(50, 100),
        )
        db.session.add(post)
    db.session.commit()
    return


def real_categories(count=10):
    for c in Category.query.all():
        db.session.delete(c)
    db.session.commit()
    for i in range(count):
        if i <= 2:
            names = ["动画", "小说", "游戏"]
            category = Category(name=names[i])
        else:
            category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def real_user(count=50):
    with open("./data/user.json", "r", encoding="utf8") as f:
        users = json.load(f)
    for u in User.query.all():
        db.session.delete(u)
    db.session.commit()
    for i in range(count):
        raw = users[i]
        user = User(
            username=raw["name"],
            password=fake.pystr(),
            email=fake.email(),
            about=raw["sign"],
            image=raw["face"],
        )
        db.session.add(user)
    db.session.commit()
