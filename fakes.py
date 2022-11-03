
import random

from faker import Faker
from sqlalchemy.exc import IntegrityError

from extensions import db
from models import Category, Post, Comment, User
fake = Faker()
def fake_user(count=5):
    for _ in range(count):
        user=User(
            username= fake.name(),
            about="hello",
            password=fake.pystr(),
        )
        db.session.add(user)
    db.session.commit()

def fake_categories(count=10):
    category = Category(name='Default')
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
            num_likes=random.randint(10,50),
            num_comments=random.randint(0,10),
            num_views=random.randint(50,100), 
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

            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)


    salt = int(count * 0.1)
    for i in range(salt):
        # from user
        comment = Comment(
            author='Mima Kirigoe',
            email='mima@example.com',
            site='example.com',
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            from_author=True,

            post=Post.query.get(random.randint(1, Post.query.count()))
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
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()


