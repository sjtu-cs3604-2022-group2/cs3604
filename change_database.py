import random
from models import Post,Comment
from extensions import db
def change_comments_num_likes():
    comments=Comment.query.all()
    for comment in comments:
        comment.num_likes=random.randint(20,100)
    db.session.commit()
    

if __name__ == "__main__":
    change_comments_num_likes()
        
    
    
    
    
    