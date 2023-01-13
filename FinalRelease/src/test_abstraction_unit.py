from abstraction import *
from app import *
import unittest
from extensions import db
app=create_app("development")
context = app.test_request_context()
context.push()
class HelloTest(unittest.TestCase):
    client = app.test_client()

    def setUp(self): 
        app.config.update( 
            TESTING=True , 
            WTF_CSRF_ENABLED=False, 
            SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
        )

        self.user_id=1 #用于测试的用户
        self.post_id=1 #帖子对象
        self.comment_id=1 #被作用评论对象
        self.user=User.query.get(self.user_id)
        self.post=Post.query.get(self.post_id)
        self.comment=Comment.query.get(self.comment_id)
        self.post_obj=ObjectPost(self.post)
        self.comment_obj=ObjectComment(self.comment,2)

        # 先取消该用户点赞状态
        action_unlike=ActionUnlike(self.user_id)
        
        action_unlike.set_object(self.post_obj)
        action_unlike.update_database()

        action_unlike.set_object(self.comment_obj)
        action_unlike.update_database()


    # 测试点赞和取消点赞post
    def test_like_and_unlike_post(self):
        ori_like_num=self.post.num_likes
        ori_note_num=len(self.post.user.notifications)
        action_like=ActionLike(self.user_id)
        action_like.set_object(self.post_obj)
        action_like.update_database()
        action_like.send_notification()
        new_like_num=self.post.num_likes
        new_note_num=len(self.post.user.notifications)
        self.assertEqual(ori_like_num+1,new_like_num)
        self.assertEqual(ori_note_num+1,new_note_num)

        ori_like_num=self.post.num_likes
        action_unlike=ActionUnlike(self.user_id)
        action_unlike.set_object(self.post_obj)
        action_unlike.update_database()
        new_like_num=self.post.num_likes
        self.assertEqual(ori_like_num-1,new_like_num)

    # 测试点赞和取消点赞post
    def test_like_and_unlike_post(self):
        ori_like_num=self.post.num_likes
        ori_note_num=len(self.post.user.notifications)
        action_like=ActionLike(self.user_id)
        action_like.set_object(self.post_obj)
        action_like.update_database()
        action_like.send_notification()
        new_like_num=self.post.num_likes
        new_note_num=len(self.post.user.notifications)
        self.assertEqual(ori_like_num+1,new_like_num)
        self.assertEqual(ori_note_num+1,new_note_num)

        ori_like_num=self.post.num_likes
        action_unlike=ActionUnlike(self.user_id)
        action_unlike.set_object(self.post_obj)
        action_unlike.update_database()
        new_like_num=self.post.num_likes
        self.assertEqual(ori_like_num-1,new_like_num)


    def test_like_and_unlike_comment(self):
        ori_like_num=self.comment.num_likes
        ori_note_num=len(self.comment.user.notifications)
        action_like=ActionLike(self.user_id)
        action_like.set_object(self.comment_obj)
        action_like.update_database()
        action_like.send_notification()
        new_like_num=self.comment.num_likes
        new_note_num=len(self.comment.user.notifications)
        self.assertEqual(ori_like_num+1,new_like_num)
        self.assertEqual(ori_note_num+1,new_note_num)

        ori_like_num=self.comment.num_likes
        action_unlike=ActionUnlike(self.user_id)
        action_unlike.set_object(self.comment_obj)
        action_unlike.update_database()
        new_like_num=self.comment.num_likes
        self.assertEqual(ori_like_num-1,new_like_num)

    def test_reply_post(self):
        body="回复帖子"
        new_comment=Comment(body=body, from_author=(self.post.user.id==self.user_id), post_id=self.post_id, towards=-1, user_id=self.user_id)
        new_floor=self.post.num_comments+1
        ori_comment_num=self.post.num_comments
        ori_note_num=len(self.post.user.notifications)

        action_reply=ActionReply(self.user_id,new_comment,new_floor)
        action_reply.set_object(self.post_obj)
        action_reply.update_database()
        action_reply.send_notification()

        new_comment_num=self.post.num_comments
        new_note_num=len(self.post.user.notifications)
        self.assertEqual(ori_comment_num+1,new_comment_num)
        self.assertEqual(ori_note_num+1,new_note_num)

    def test_reply_comment(self):
        body="回复评论"
        new_comment=Comment(body=body, from_author=(self.post.user.id==self.user_id), post_id=self.post_id, towards=2, user_id=self.user_id)
        new_floor=self.post.num_comments+1
        ori_comment_num=self.post.num_comments
        ori_note_num=len(self.comment.user.notifications)

        action_reply=ActionReply(self.user_id,new_comment,new_floor)
        action_reply.set_object(self.comment_obj)
        action_reply.update_database()
        action_reply.send_notification()

        new_comment_num=self.post.num_comments
        new_note_num=len(self.comment.user.notifications)
        self.assertEqual(ori_comment_num+1,new_comment_num)
        self.assertEqual(ori_note_num+1,new_note_num)

    def test_report_post(self):
        ori_report_num=len(AdminNotification.query.all())
        reason="引战嫌疑"
        action_report=ActionReport(self.user_id,reason)
        action_report.set_object(self.post_obj)
        action_report.send_report()
        new_report_num=len(AdminNotification.query.all())
        self.assertEqual(ori_report_num+1,new_report_num)

    def test_report_comment(self):
        ori_report_num=len(AdminNotification.query.all())
        reason="涉及抄袭"
        action_report=ActionReport(self.user_id,reason)
        action_report.set_object(self.comment_obj)
        action_report.send_report()
        new_report_num=len(AdminNotification.query.all())
        self.assertEqual(ori_report_num+1,new_report_num)

    def test_create_and_delete(self):

        # 创建帖子和评论
        new_post=Post(title="新建帖子", category_id=0, body="body",user_id=self.user_id,user=self.user)
        db.session.add(new_post)
        db.session.commit()
        body="回复新帖子"
        new_comment=Comment(body=body, from_author=(new_post.user.id==self.user_id), post_id=new_post.id, towards=-1, user_id=self.user_id)
        new_floor=new_post.num_comments+1
        action_reply=ActionReply(self.user_id,new_comment,new_floor)
        action_reply.set_object(self.post_obj)
        action_reply.update_database()
        action_reply.send_notification()

        new_post_obj=ObjectPost(new_post)
        new_comment_obj=ObjectComment(new_comment)

        # 删除评论
        ori_comm_num=new_post.num_comments
        ori_comm_num1=len(list(filter(lambda x:x.valid==1,new_post.comments)))
        ori_delete_record=len(DeleteRecord.query.all())
        ori_note=len(self.user.notifications)
        action_delete=ActionDelete(self.user_id,reason="删除评论理由")
        action_delete.set_object(new_comment_obj)
        action_delete.delete_object()
        action_delete.send_notification()
        new_comm_num=new_post.num_comments
        new_comm_num1=len(list(filter(lambda x:x.valid==1,new_post.comments)))
        new_delete_record=len(DeleteRecord.query.all())
        new_note=len(self.user.notifications)
        self.assertEqual(ori_comm_num,new_comm_num)
        self.assertEqual(ori_comm_num1-1,new_comm_num1)
        self.assertEqual(ori_delete_record+1,new_delete_record)
        self.assertEqual(ori_note+1,new_note)

        # 删除帖子
        ori_post_num1=len(list(filter(lambda x:x.valid==1,Post.query.all())))
        ori_delete_record=len(DeleteRecord.query.all())
        ori_note=len(self.user.notifications)
        action_delete=ActionDelete(self.user_id,reason="删除帖子理由")
        action_delete.set_object(new_post_obj)
        action_delete.delete_object()
        action_delete.send_notification()
        new_post_num1=len(list(filter(lambda x:x.valid==1,Post.query.all())))
        new_delete_record=len(DeleteRecord.query.all())
        new_note=len(self.user.notifications)
        self.assertEqual(ori_post_num1-1,new_post_num1)
        self.assertEqual(ori_delete_record+1,new_delete_record)
        self.assertEqual(ori_note+1,new_note)
    

if __name__ == '__main__':
    unittest.main()