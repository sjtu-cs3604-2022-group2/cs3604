from flask import Blueprint, render_template, g, flash, request, redirect, url_for, current_app, session
from blueprints import posts
from models import User, Post, Comment, Notification
from actiontype import *
from utils import filter_body_content
from extensions import db

# class ActionInfo:
#     def __init__(self,action,object,body,link):
#         self.action=action
#         self.object=object
#         self.body=body
#         self.link=link


class AbstractAction():
    def __init__(self, post_id, cur_user_id, floor=-1, reply_id=-1, comment_body=''):
        self.post_id = post_id
        self.cur_user_id = cur_user_id
        self.floor = floor
        self.reply_id = reply_id
        self.comment_body = comment_body

    def set_comment_body(self, body=''):
        self.comment_body = filter_body_content(body)

    def to_a_post(self):
        pass

    def to_a_reply(self):
        pass

    def set_action(self, option):
        if (option == OptionType.LIKE):
            return ActionLike(self.post_id, self.cur_user_id, self.floor, self.reply_id, self.comment_body)
        elif (option == OptionType.COMMENT):
            return ActionComment(self.post_id, self.cur_user_id, self.floor, self.reply_id, self.comment_body)


class ActionLike(AbstractAction):
    def to_a_post(self):
        return LikeAPost(self.post_id, self.cur_user_id, self.floor, self.reply_id, self.comment_body)

    def to_a_reply(self):
        return LikeAReply(self.post_id, self.cur_user_id, self.floor, self.reply_id, self.comment_body)


class ActionComment(AbstractAction):
    def to_a_post(self):
        '''Call set_comment_body before calling this'''
        return CommentAPost(self.post_id, self.cur_user_id, self.floor, self.reply_id, self.comment_body)

    def to_a_reply(self):
        '''Call set_comment_body before calling this'''
        return CommentAReply(self.post_id, self.cur_user_id, self.floor, self.reply_id, self.comment_body)


class ObjectPost():
    def __init__(self, post_id, cur_user_id, floor=-1, reply_id=-1, comment_body=''):
        self.post_id = post_id
        self.cur_user_id = cur_user_id
        self.floor = floor
        self.reply_id = reply_id
        self.comment_body = filter_body_content(comment_body)

    def get_post_info(self):
        post_link = url_for("posts.detail", post_id=self.post_id)
        post = Post.query.get(self.post_id)
        return filter_body_content(post.title), post.user_id, post_link

    def send_notification(self, post_id, cur_user_id, floor=-1, reply_id=-1):
        pass


class LikeAPost(ObjectPost):
    def update_likes(self):
        post = Post.query.get(self.post_id)
        cur_user = User.query.get(self.cur_user_id)
        cur_user.like_posts.append(post)
        post.num_likes += 1
        db.session.commit()

    def send_notification(self):
        text, dst_user, link = self.get_post_info()

        notice = Notification(body=text, 
                              state=StateType.UNREAD.value,
                              action=OptionType.LIKE.value, 
                              object=ObjectType.OBJECT_POST.value,
                              link=link, user_id=dst_user,
                              action_id=self.cur_user_id, post_id=self.post_id)
        db.session.add(notice)
        db.session.commit()


class CommentAPost(ObjectPost):
    # def __init__(self,comment_body):
    #     self.comment_body=comment_body
    def update_comments(self, comment):
        post = Post.query.get(self.post_id)
        post.num_comments += 1
        db.session.add(comment)
        db.session.commit()

    def send_notification(self):
        _, dst_user, post_link = self.get_post_info()
        text = self.comment_body
        link = post_link+'#comment'+str(self.floor)
        notice = Notification(body=text, 
                              state=StateType.UNREAD.value,
                              action=OptionType.COMMENT.value, 
                              object=ObjectType.OBJECT_POST.value,
                              link=link, user_id=dst_user,
                              action_id=self.cur_user_id, post_id=self.post_id)
        db.session.add(notice)
        db.session.commit()


class ObjectReply():
    def __init__(self, post_id, cur_user_id, floor=-1, reply_id=-1, comment_body=''):
        self.post_id = post_id
        self.cur_user_id = cur_user_id
        self.floor = floor
        self.reply_id = reply_id
        self.comment_body = comment_body

    def get_post_info(self):
        post_link = url_for("posts.detail", post_id=self.post_id)
        post = Post.query.get(self.post_id)
        return post.user_id, post_link

    def send_notification():
        pass


class LikeAReply(ObjectReply):
    def update_likes(self):
        reply = Comment.query.get(self.reply_id)
        cur_user = User.query.get(self.cur_user_id)
        cur_user.like_comments.append(reply)
        reply.num_likes += 1
        db.session.commit()

    def send_notification(self):
        dst_user, post_link = self.get_post_info()
        reply = Comment.query.get(self.reply_id)
        text = filter_body_content(reply.body)
        link = post_link+'#comment'+str(self.floor)
        notice = Notification(body=text, 
                              state=StateType.UNREAD.value,
                              action=OptionType.LIKE.value, 
                              object=ObjectType.OBJECT_REPLY.value,
                              link=link, user_id=dst_user,
                              action_id=self.cur_user_id, post_id=self.post_id)
        db.session.add(notice)
        db.session.commit()


class CommentAReply(ObjectReply):

    def update_comments(self, comment):
        post = Post.query.get(self.post_id)
        post.num_comments += 1
        db.session.add(comment)
        db.session.commit()

    def send_notification(self):
        dst_user, post_link = self.get_post_info()
        text = filter_body_content(self.comment_body)
        link = post_link+'#comment'+str(self.floor)
        notice = Notification(body=text, 
                              state=StateType.UNREAD.value,
                              action=OptionType.COMMENT.value, 
                              object=ObjectType.OBJECT_REPLY.value,
                              link=link, user_id=dst_user,
                              action_id=self.cur_user_id, post_id=self.post_id)
        db.session.add(notice)
        db.session.commit()
