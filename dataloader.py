import os
import random
import json
from faker import Faker
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from flask_dropzone import random_filename
from extensions import db
from models import *
from app import *


random.seed(42)
Faker.seed(42)
fake = Faker()


def random_relation(count, active):
    positive = random.randint(0, count - 1)
    while positive == active:
        positive = random.randint(0, count - 1)
    return positive


def clear_uploads():
    cur = os.curdir
    path = "\\static\\uploads"
    rm = os.listdir(cur + path)
    for i in rm:
        rm_path = os.path.join(path, i)
        os.remove(cur + rm_path)


def init_categories(count=5):
    print(f"create {count} Categories")
    for c in Category.query.all():
        db.session.delete(c)
    db.session.commit()
    category = Category(name="开发测试")
    db.session.add(category)
    for i in range(count):
        if i <= 4:
            names = ["动画", "小说", "游戏", "音乐", "电影"]
            category = Category(name=names[i])
        else:
            category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def init_user(count=30):
    print(f"create {count} Users")
    with open("./data/user.json", "r", encoding="utf8") as f:
        users = json.load(f)
    for u in User.query.all():
        db.session.delete(u)
    db.session.commit()

    clear_uploads()
    image_pool = set()

    def get_image() -> str:
        nonlocal image_pool
        cur = os.curdir
        id = random.randint(1, 100)
        if len(image_pool) == 100:
            image_pool = set()
        while id in image_pool:
            id = random.randint(1, 100)
        origin = open(f"{cur}/data/avatar/{id}.png", mode="rb")
        path = f"/static/uploads/" + random_filename(f"{id}.png")
        new = open(cur + path, mode="wb")
        new.write(origin.read())
        origin.close()
        new.close()
        return path

    user = User(
        username="管理员1",
        password="123",
        about="this is me",
        image=get_image(),
    )
    db.session.add(user)
    for i in range(count):
        raw = users[i]
        user = User(
            username=raw["name"],
            password="123",
            email=fake.email(),
            join_time=fake.date_time_this_year(),
            about=raw["sign"],
            image=get_image(),
        )
        db.session.add(user)
    db.session.commit()
    for u in User.query.all():
        for i in range(6):
            if getattr(u, "id", 0):
                positive = random_relation(count, u.id)
                follow_u = User.query.get(positive)
                if follow_u:
                    u.follow(follow_u)
    db.session.commit()


def init_post(count=180):
    print(f"create {count} Posts")
    with open("./data/data.json", "r", encoding="utf8") as f:
        posts = json.load(f)
    for p in Post.query.all():
        db.session.delete(p)
    db.session.commit()

    image_pool = set()
    image_list = os.listdir("./data/pic")

    def get_image() -> str:
        nonlocal image_pool, image_list
        cur = os.curdir
        id = random.randint(0, len(image_list) - 1)
        if len(image_pool) == len(image_list):
            image_pool = set()
        while id in image_pool:
            id = random.randint(0, len(image_list) - 1)
        origin = open(os.path.join(f"{cur}/data/pic", image_list[id]), mode="rb")
        filename = random_filename(image_list[id])
        path = f"/static/uploads/" + filename
        new = open(cur + path, mode="wb")
        new.write(origin.read())
        origin.close()
        new.close()
        return filename, path

    for i in range(count):
        raw = posts[i]
        post = Post(
            title=raw["title"],
            body=raw["body"],
            category_id=raw["category"] + 1,
            timestamp=datetime.strptime(raw["time"][0], "%Y-%m-%d %H:%M"),
            user_id=random.randint(1, User.query.count()),
            num_likes=0,
            num_comments=raw["n_comment"],
            num_views=random.randint(50, 100),
        )
        filename, path = get_image()
        photo = Photo(filename=filename, user_id=post.user_id, post=post, timestamp=post.timestamp, photo_path=path)
        db.session.add(post)
        db.session.add(photo)
        db.session.commit()
        all_comment = raw["comment"] + raw["sub_cmt"]
        for j in range(raw["n_comment"]):
            comment = Comment(
                body=all_comment[j],
                timestamp=datetime.strptime(raw["time"][j + 1], "%Y-%m-%d %H:%M"),
                post_id=post.id,
                user_id=random.randint(1, User.query.count()),
            )
            post.comments.append(comment)
            db.session.add(comment)
            db.session.commit()
    db.session.commit()


def init_message():
    num_users = User.query.count()
    count = num_users * (num_users - 1) // 2
    print(f"create {count} Messages")
    for p in Message.query.all():
        db.session.delete(p)
    db.session.commit()
    for i in range(num_users):
        for j in range(num_users):
            if i == j:
                continue
            comment = Message(
                body=f"嗨!你好",
                timestamp=fake.date_time_this_year(),
                author=User.query.get(i + 1),
                to_id=j + 1,
            )
            db.session.add(comment)
    db.session.commit()


def init_likes():
    print("初始化用户点赞")
    for post in Post.query.all():
        num_like = random.randint(5, 30)
        users = User.query.all()
        random.shuffle(users)
        like_users = users[:num_like]
        post.like_users = like_users
        post.num_likes = num_like
    db.session.commit()


if __name__ == "__main__":
    app = create_app("development")
    context = app.test_request_context()
    context.push()
    db.drop_all()
    db.create_all()
    init_categories()
    init_user()
    init_post()
    init_message()
    init_likes()  # 初始化点赞数据
    # init photo
    # init likes
    # init notifications
    # admin1=User.query.get(1)
    # normal_user=User.query.get(9)
    # admin1.follow(normal_user)
    # db.session.commit()
