import random
import json
from faker import Faker
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from extensions import db
from models import Category, Post, Comment, User, Follow


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

# --------------------------------------


def random_relation(count, active):
    positive = random.randint(0, count-1)
    while (positive == active):
        positive = random.randint(0, count-1)
    return positive


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
    return


def real_categories(count=10):
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


def real_user(count=50):
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


def real_data_load(user=50, category=10, post=100):
    db.drop_all()
    db.create_all()
    real_categories(category)
    print(f'create categories: {category}')
    real_user(user)
    print(f'create user: {user}')
    real_post(post)
    print(f'create post: {post}')
    return
