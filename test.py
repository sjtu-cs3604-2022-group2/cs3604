from faker import Faker
import time
import datetime
import os
import random
from flask_dropzone import random_filename

faker = Faker()

a = faker.date_time_this_year()
print(a)
print(type(a))

b = datetime.datetime.now

c = datetime.datetime.strptime("2017-2-26 21:00", '%Y-%m-%d %H:%M')

d = time.strptime("30 Nov 00", "%d %b %y")

print(b, c, d)

e = random_filename("1.png")

print(e)

cur_dir = os.path.curdir

print(cur_dir)

image_pool = set()

def get_image() -> str:
    global image_pool
    id = random.randint(1, 100)
    if len(image_pool) == 100:
        image_pool = set()
    while id in image_pool:
        id = random.randint(1, 100)
    print(id)
    origin = open(f"{cur_dir}/data/avatar/{id}.png", mode="rb")
    path = f"/static/uploads/"+random_filename(f"{id}.png")
    new = open(cur_dir+path, mode="wb")
    new.write(origin.read())
    origin.close()
    new.close()
    print(path)
    return path
    
get_image()

def clear_uploads():
    path = "\\static\\uploads"
    l = os.listdir(cur_dir+path)
    print(l)
    for i in l:
        a = os.path.join(path, i)
        print(a)
        os.remove(cur_dir+a)
    
clear_uploads()