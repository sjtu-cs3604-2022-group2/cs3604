from models import User, Post
from sqlalchemy import or_

"""
description:  取得一个用户感兴趣的category,兴趣以重要性递减。
param {*} user_id
return {list}
"""
def get_interest_category(user_id):
    cat_record = dict()
    user = User.query.get(user_id)
    for p in user.posts.all():
        cat_record[p.category_id] = cat_record.get(p.category_id, 0) + 1

    recommend_category = sorted(list(cat_record.keys()), key=lambda x: cat_record[x], reverse=True)[:3]
    return recommend_category


'''
description:  得到给一个用户推荐的帖子
param {*} user_id
return {*}
'''
def get_recommendation_posts(user_id):
    cat_record = dict()
    user = User.query.get(user_id)
    for p in user.posts.all():
        cat_record[p.category_id] = cat_record.get(p.category_id, 0) + 1

    recommend_category = sorted(list(cat_record.keys()), key=lambda x: cat_record[x], reverse=True)[:2]
    print(recommend_category)
    if len(recommend_category) >= 2:
        recommend_posts = Post.query.filter(
            or_(Post.category_id == recommend_category[0], Post.category_id == recommend_category[1])
        ).all()
        recommend_posts = recommend_posts[:10]
    else:
        recommend_posts = []
    return recommend_posts


'''
description:  得到推荐关注的用户
param {*} user_id
return {*}
'''
def get_recommendation_users(user_id):
    cat_record = dict()
    user = User.query.get(user_id)
    for p in user.posts.all():
        cat_record[p.category_id] = cat_record.get(p.category_id, 0) + 1

    recommend_category = sorted(list(cat_record.keys()), key=lambda x: cat_record[x], reverse=True)[:3]

    recommend_user = []
    for u in User.query.all():
        interest_category = get_interest_category(u.user_id)
        if interest_category[0] in recommend_category:
            recommend_user.append(u)
            if len(recommend_user) == 10:
                break
    return recommend_user
