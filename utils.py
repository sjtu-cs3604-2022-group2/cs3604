import re

from models import User, Post
from sqlalchemy import or_
import pandas as pd
from sklearn.metrics.pairwise import pairwise_distances
import os
import numpy as np

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


"""
description:  得到给一个用户推荐的帖子
param {*} user_id
return {*}
"""


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


"""
description:  得到推荐关注的用户
param {*} user_id
return {*}
"""


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


def filter_body_content(str):
    reg_p = re.compile(r"</p>")
    reg_tag = re.compile(r"<.+?>")
    str = reg_p.sub("   ", str)
    str = reg_tag.sub("", str)
    if len(str) > 40:
        str = str[:40]
        if str[-1] != " ":
            str += "..."
    str = str.replace("   ", "&nbsp;&nbsp;&nbsp;")
    return str


"""
description: 根据数据库中信息创建一张pandas的表
return {*}
"""


def get_df_table():
    # if os.path.exists("datasets.csv"):
    #     post_ids = [i for i in range(1, Post.query.count() + 1)]
    #     return pd.read_csv("datasets.csv", header=0, names=post_ids)
    # else:
    num_posts = Post.query.count()
    num_user = User.query.count()

    datasets = [[0 for _ in range(num_posts)] for _ in range(num_user)]
    for user in User.query.all():
        for post in user.like_posts:
            datasets[user.id - 1][post.id - 1] = 1

    users = [i for i in range(1, num_user + 1)]
    items = [i for i in range(1, num_posts + 1)]

    df = pd.DataFrame(datasets, columns=items, index=users)

    df.to_csv("datasets.csv")

    return df


"""
description:  计算用户之间的相似度
return {*}
"""


def compute_user_similar():
    # if os.path.exists("user_similar.csv"):
    #     user_ids = [i for i in range(1, User.query.count() + 1)]
    #     return pd.read_csv("user_similar.csv", header=0, names=user_ids)
    # else:
    df = get_df_table()
    num_posts = Post.query.count()
    num_user = User.query.count()
    users = [i for i in range(1, num_user + 1)]
    # items = [i for i in range(1, num_posts + 1)]

    # 计算用户间相似度
    user_similar = 1 - pairwise_distances(df.values, metric="jaccard")
    user_similar = pd.DataFrame(user_similar, columns=users, index=users)

    # 将该DataFrame 保存到文件中
    user_similar.to_csv("user_similar.csv")
    return user_similar


"""
description: 使用协同过滤（CF）来得到推荐的users
return {*}
"""


def CF_get_recommendation_users(user_id):
    ## 返回的是一个用户对象的列表

    user_similar = compute_user_similar()
    # 取出对应该行的数据，然后移除掉自身
    _df = user_similar.loc[user_id].drop([user_id])
    # print(_df)
    _df_sorted = _df.sort_values(ascending=False)
    # print(_df_sorted)
    top5 = list(_df_sorted.index[:5])
    # topN_users[i] = top2
    return [User.query.get(user_id) for user_id in top5]


def CF_get_recommendation_posts(user_id, num_posts=10):
    df = get_df_table()
    user_similar = compute_user_similar()
    # 取出对应该行的数据，然后移除掉自身
    _df = user_similar.loc[user_id].drop([user_id])
    # print(_df)
    _df_sorted = _df.sort_values(ascending=False)
    top10 = list(_df_sorted.index[:10])

    rs_result = set()  # 存储推荐结果
    for sim_user in top10:
        # 构建初始的推荐结果
        rs_result = rs_result.union(set(df.loc[sim_user].replace(0, np.nan).dropna().index))
    # 过滤掉已经点赞过的post
    rs_result -= set(df.loc[user_id].replace(0, np.nan).dropna().index)

    # return list()
    tmp = list(rs_result)[:num_posts]
    return [Post.query.get(post_id) for post_id in tmp]
