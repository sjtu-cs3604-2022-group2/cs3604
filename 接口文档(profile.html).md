# profile.html


1. 当前登陆的用户：user类对象current_user
    头像src：{{url_for('static',filename=current_user.image)}}
    好友的id:{{current_user.follow[i].username}}
    好友的头像:{{current_user.follow[i].image}}

2. 当前浏览的主页的归属用户poster_user：
    归属用户头像: {{url_for('static',filename=poster_user.image)}}
    归属用户id:{{poster_user.username}}
    归属用户发布动态的照片:{{poster_user.posts[i].image}}
    归属用户发布动态的文字内容:{{poster_user.posts[i].text}}
    归属用户发布动态的@的一个好友:{{poster_user.posts[i].atuser}}
