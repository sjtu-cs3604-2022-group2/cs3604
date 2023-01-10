# Bridge

from flask import Blueprint, render_template, g, flash, request, redirect, url_for, current_app, session

from models import User, Post, Comment, Notification, AdminNotification, DeleteRecord
from actiontype import *
from utils import filter_body_content
from extensions import db

# 实现类
class Object:
    def get_database(self):
        pass
    def get_text(self):
        pass
    def get_mainlink(self):
        pass
    def get_sublink(self):
        pass

    def get_text(self):
        pass
    def get_object(self):
        pass
    def get_obj_id_tuple(self):
        pass
    def get_object_type(self):
        pass

    def set_invalid(self):
        pass

class ObjectPost(Object):
    def __init__(self,post):
        self.database=Post
        self.object=post
        self.floor=-1

    def get_like_list(self,cur_user):
        return cur_user.like_posts

    def get_database(self):
        return self.database

    def get_text(self):
        return filter_body_content(self.object.title)

    def get_object(self):
        return self.object

    def get_dst_user(self):
        return self.object.user_id

    def get_obj_id_tuple(self):
        return (self.object.id,-1)

    def get_object_type(self):
        return ObjectType.OBJECT_POST.value


    def get_mainlink(self):
        return url_for("posts.detail", post_id=self.object.id)

    def get_sublink(self):
        return ''

    def set_invalid(self):
        self.object.valid=0
        for comment in self.object.comments:
            comment.valid = 0
        db.session.commit()


class ObjectComment(Object):
    def __init__(self,reply,reply_floor=-1):
        self.database=Comment
        self.object=reply
        self.floor=reply_floor  # 是作为被点赞/评论对象的那个reply！

    def get_database(self):
        return self.database

    def get_object(self):
        return self.object

    def get_like_list(self,cur_user):
        return cur_user.like_comments

    def get_text(self):
        return filter_body_content(self.object.body)

    def get_dst_user(self):
        return self.object.user_id

    def get_obj_id_tuple(self):
        return (self.object.post_id,self.object.id)

    def get_object_type(self):
        return ObjectType.OBJECT_COMMENT.value

    def get_mainlink(self):
        return url_for("posts.detail", post_id=self.object.post_id)

    def get_sublink(self):
        return '#comment'+str(self.floor)

    def set_invalid(self):
        self.object.valid=0
        db.session.commit()

#抽象类

class AbstractAction:
    def set_object(self,obj:Object):
        self.obj=obj
    # def update_database():
    #     pass
    # def send_notification():
    #     pass

class ActionLike(AbstractAction):
    def __init__(self,user_id):
        self.user_id=user_id   # 谁做出这个action

    def update_database(self):
        database=self.obj.get_database()
        object=self.obj.get_object()
        cur_user = User.query.get(self.user_id)
        like_list=self.obj.get_like_list(cur_user)
        like_list.append(object)
        object.num_likes += 1
        db.session.commit()

    def send_notification(self):
        text=self.obj.get_text()
        link=self.obj.get_mainlink()+self.obj.get_sublink()
        obj_type=self.obj.get_object_type()
        dst_user=self.obj.get_dst_user()
        post_id=self.obj.get_obj_id_tuple()[0]
        comment_id=self.obj.get_obj_id_tuple()[1]
        notice = Notification(body=text, 
                              state=StateType.UNREAD.value,
                              action=OptionType.LIKE.value, 
                              object=obj_type,
                              link=link, user_id=dst_user,
                              action_id=self.user_id, post_id=post_id,comment_id=comment_id)
        db.session.add(notice)
        db.session.commit()

class ActionReply(AbstractAction):
    def __init__(self,user_id,new_com:Comment,new_floor):
        self.user_id=user_id
        self.new_comment=new_com
        # self.text=filter_body_content(new_com.body)
        self.new_floor=new_floor

    def update_database(self):
        post_id=self.obj.get_obj_id_tuple()[0]
        post=Post.query.get(post_id)
        post.num_comments+=1
        db.session.add(self.new_comment)
        db.session.commit()


    def send_notification(self):
        text=filter_body_content(self.new_comment.body)
        link=self.obj.get_mainlink()+'#comment'+str(self.new_floor)
        obj_type=self.obj.get_object_type()
        post_id=self.obj.get_obj_id_tuple()[0]
        comment_id=self.new_comment.id
        dst_user=self.obj.get_dst_user()
        notice = Notification(body=text, 
                              state=StateType.UNREAD.value,
                              action=OptionType.REPLY.value, 
                              object=obj_type,
                              link=link, user_id=dst_user,
                              action_id=self.user_id, post_id=post_id,comment_id=comment_id)
        db.session.add(notice)
        db.session.commit()


class ActionUnlike(AbstractAction):
    def __init__(self,user_id):
        self.user_id=user_id   # 谁做出这个action

    def update_database(self):
        database=self.obj.get_database()
        object=self.obj.get_object()
        cur_user = User.query.get(self.user_id)
        like_list=self.obj.get_like_list(cur_user)
        if(object in like_list):
            like_list.remove(object)
            object.num_likes -= 1
            db.session.commit()

class ActionReport(AbstractAction):
    def __init__(self,user_id,reason):
        self.user_id=user_id
        self.reason=reason

    def send_report(self):
        post_id,comment_id=self.obj.get_obj_id_tuple()
        link="/admin"+self.obj.get_mainlink()+self.obj.get_sublink()
        obj_type=self.obj.get_object_type()
        text=self.obj.get_text()
        text=text.replace("&nbsp;",' ')
        if(len(text)>23):
            text=text[:20]+'...'
        text=text.replace("   ",'&nbsp;&nbsp;&nbsp;')
        notice=AdminNotification(reason=self.reason,
                                action_id=self.user_id,
                                link=link,
                                state=StateType.UNREAD.value,
                                object=obj_type,
                                post_id=post_id,
                                comment_id=comment_id,
                                body=text)
        db.session.add(notice)
        db.session.commit()

class ActionDelete(AbstractAction):
    def __init__(self,user_id,reason):
        self.user_id=user_id
        self.reason=reason

    def delete_object(self):
        self.obj.set_invalid()

    def send_notification(self):
         
        text=self.obj.get_text()
        
        obj_type=self.obj.get_object_type()
        dst_user=self.obj.get_dst_user()
        post_id=self.obj.get_obj_id_tuple()[0]
        comment_id=self.obj.get_obj_id_tuple()[1]

        ori_link=self.obj.get_mainlink() # +self.obj.get_sublink()

        record=DeleteRecord(reason=self.reason,
                            action_id=self.user_id,user_id=dst_user,
                            object=obj_type,
                            post_id=post_id,comment_id=comment_id,
                            original_link=ori_link)

        db.session.add(record)
        db.session.commit()

        link='#delete_record'+str(record.id)
        notice = Notification(body=text, 
                              state=StateType.UNREAD.value,
                              action=OptionType.DELETE.value, 
                              object=obj_type,
                              link=link, user_id=dst_user,
                              action_id=self.user_id, post_id=post_id,comment_id=comment_id)
        db.session.add(notice)
        db.session.commit()

        

