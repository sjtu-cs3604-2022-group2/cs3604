from urllib import parse
from pprint import pprint
import requests

host = 'http://127.0.0.1'
user = {
    'username': 'test',
    'password':'123'
}

s = requests.Session() # => 会话对象

# 登录
login_url = parse.urljoin(host, '/user/login')
lr = s.post(login_url, data=user)
print(type(lr))
print(lr.status_code)
exit(0)
pprint(lr.json())

# 上传图片
upload_url = parse.urljoin(host,'http://127.0.0.1/upload')
# 构造图片数据，这里必须要填上图片相关参数
file = {
    'editormd-image-file': open('static/image/imgs_icons/blossom-background.jpg', 'rb'),   # => 用name指定文件
    'Content-Disposition': 'form-data', 
    'Content-Type': 'image/png', 
    'filename':'1.png'
    }
ur = s.post(upload_url, files=file)  # => 注意这里，参数名是 files
pprint(ur.json())
