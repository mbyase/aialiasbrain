# coding=utf-8
# author HerbLee
import uuid
from django.contrib.auth.hashers import make_password, check_password
import re


# 生成32位的全球唯一码
def uid():
    str1 = str(uuid.uuid1())
    return str1.replace("-", "")


# 加密密码
def make_passwd(passwd):
    return make_password(passwd, None, 'pbkdf2_sha256')


# 检查密码
def check_passwd(passwd, data):
    return check_password(passwd, data)


# 校验是否为邮箱
def check_email(str):
    mat = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
    return re.match(mat, str)


# 校验是否为手机号
def check_mobil(num):
    mat = r'[1][^1269]\d{9}'
    return re.match(mat, num)
