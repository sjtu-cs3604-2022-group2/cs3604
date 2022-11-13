"""
Author: zknyyds 1007736246@qq.com
Date: 2022-11-01 16:45:43
LastEditors: zknyyds 1007736246@qq.com
LastEditTime: 2022-11-13 20:46:47
FilePath: \hobbitat\models.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
"""
from extensions import db
from datetime import datetime


class Follow(db.Model):
    __tablename__ = "follows"
    follower_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  ### 记录关注的时间


class Email(db.Model):
    __tablename__ = "email"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    captcha = db.Column(db.String(10), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=True, unique=True)
    password = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(100), nullable=True, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)
    about = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(100), nullable=True)

    posts = db.relationship("Post", backref="user")
    followed = db.relationship(
        "Follow",
        foreign_keys=[Follow.follower_id],
        backref=db.backref("follower", lazy="joined"),
        lazy="dynamic",
        cascade="all,delete-orphan",
    )

    followers = db.relationship(
        "Follow",
        foreign_keys=[Follow.follower_id],
        backref=db.backref("followed", lazy="joined"),
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    ### 在Post 对应的 实例上，会自动添加一个user的属性，这指向的是user对象。


# class QuestionModel(db.Model):
#     __tablename__ = 'question'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     title = db.Column(db.String(100), nullable=True)
#     content=db.Column(db.Text,nullable=False)
#     ### 创建外键
#     author_id=db.Column(db.Integer, db.ForeignKey('user.id'))
#
#     author=db.relationship('User',backref="questions")


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True)

    posts = db.relationship("Post", backref="category")

    def delete(self):
        default_category = Category.query.get(1)
        posts = self.posts[:]
        for post in posts:
            post.category = default_category
        db.session.delete(self)
        db.session.commit()


### 定义用户与用户之间的关联表


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(60))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    can_comment = db.Column(db.Boolean, default=True)

    num_likes = db.Column(db.Integer)
    num_comments = db.Column(db.Integer)
    num_views = db.Column(db.Integer)

    # user = db.relationship('user', back_populates='posts')
    # category = db.relationship('Category', back_populates='posts')
    # user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    ## 这里会有一个user属性
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))

    comments = db.relationship("Comment", back_populates="post", cascade="all, delete-orphan")


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.String(30))
    email = db.Column(db.String(254))
    site = db.Column(db.String(255))
    body = db.Column(db.Text)
    from_author = db.Column(db.Boolean, default=False)

    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))

    post = db.relationship("Post", back_populates="comments")

    ### add a foreign key pointing self. 在同一个模型内的一对多关系称为邻接列表关系（Adjacency List Relationship)
    replied_id = db.Column(db.Integer, db.ForeignKey("comment.id"))

    replies = db.relationship("Comment", back_populates="replied", cascade="all, delete-orphan")
    replied = db.relationship("Comment", back_populates="replies", remote_side=[id])
