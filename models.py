"""
Author: zknyyds 1007736246@qq.com
Date: 2022-11-01 16:45:43
LastEditors: zknyyds 1007736246@qq.com
LastEditTime: 2022-11-13 20:46:47
FilePath: \hobbitat\models.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
"""
from email.policy import default
from extensions import db
from datetime import datetime


class Follow(db.Model):
    __tablename__ = "follows"
    follower_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # 记录关注的时间


class Email(db.Model):
    __tablename__ = "email"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    captcha = db.Column(db.String(10), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)


user_like_post_table=db.Table('user_like_post', 
                        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                        db.Column('post_id',db.Integer(),db.ForeignKey('post.id'))
                        )


user_like_comment_table=db.Table('user_like_comment', 
                        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                        db.Column('commment_id',db.Integer(),db.ForeignKey('comment.id'))
                        )


    
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=True, unique=True)
    password = db.Column(db.String(256), nullable=True)
    email = db.Column(db.String(128), nullable=True, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)
    about = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(128), nullable=True)
    posts = db.relationship("Post", backref="user", lazy="dynamic")
    photos= db.relationship("Photo", back_populates="user", cascade="all")
    comments = db.relationship("Comment", backref="user", lazy="dynamic")
    like_posts= db.relationship("Post", secondary=user_like_post_table,back_populates='like_users')
    like_comments=db.relationship('Comment', secondary=user_like_comment_table,back_populates='like_users')
    
    followed = db.relationship("Follow",
                               foreign_keys=[Follow.follower_id],
                               backref=db.backref("follower", lazy="joined"),
                               lazy="dynamic",
                               cascade="all, delete-orphan")
    followers = db.relationship("Follow",
                                foreign_keys=[Follow.followed_id],
                                backref=db.backref("followed", lazy="joined"),
                                lazy="dynamic",
                                cascade="all, delete-orphan")
    
    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)

    def unfollow(self, user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)

    def is_following(self, user):
        return self.followed.filter_by(
            followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        return self.followers.filter_by(
            follower_id=user.id).first() is not None

class Photo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    description=db.Column(db.String(500))
    filename=db.Column(db.String(64))
    timestamp=db.Column(db.DateTime,default=datetime.utcnow)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    user=db.relationship('User',back_populates='photos')
    
                        
class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), unique=True)
    posts = db.relationship("Post", backref="category",lazy='dynamic') 

    def delete(self):
        default_category = Category.query.get(1)
        posts = self.posts[:]
        for post in posts:
            post.category = default_category
        db.session.delete(self)
        db.session.commit()


class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.now, index=True)
    can_comment = db.Column(db.Boolean, default=True)

    num_likes = db.Column(db.Integer,default=0)
    num_comments = db.Column(db.Integer,default=0)
    num_views = db.Column(db.Integer,default=0)
    like_users= db.relationship('User',secondary=user_like_post_table,back_populates='like_posts')

    # 隐式属性
    # user = db.relationship('User', back_populates='posts')
    # category = db.relationship('Category', back_ref='posts')
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))

    comments = db.relationship("Comment", back_populates="post", cascade="all, delete-orphan")


class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body = db.Column(db.Text)
    from_author = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    post = db.relationship("Post", back_populates="comments")
    # 隐式属性
    # user = db.relationship('User', back_populates='comments')
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    like_users= db.relationship('User',secondary=user_like_comment_table,back_populates='like_comments')

    # add a foreign key pointing self. 在同一个模型内的一对多关系称为邻接列表关系（Adjacency List Relationship)
    replied_id = db.Column(db.Integer, db.ForeignKey("comment.id"))

    replies = db.relationship("Comment", back_populates="replied", cascade="all, delete-orphan")
    replied = db.relationship("Comment", back_populates="replies", remote_side=[id])
