from faker import Faker
import time
import datetime

faker = Faker()

a = faker.date_time_this_year()
print(a)
print(type(a))

b = datetime.datetime.now

c = datetime.datetime.strptime("2017-2-26 21:00", '%Y-%m-%d %H:%M')

d = time.strptime("30 Nov 00", "%d %b %y")

print(b, c, d)