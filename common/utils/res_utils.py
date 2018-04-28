# coding=utf-8
# author HerbLee
# 和返回值有关的

from django.http import HttpResponse
import json


# 判断是不是Post
def isPost(request):
    if request.method == 'POST':
        return True
    else:
        return False


# 判断是不是GET
def isGet(request):
    if request.method == 'GET':
        return True
    else:
        return False


"""
 2 正常的访问
    200 访问成功
 4　访问出错，错误在访问端
    400 就是错误
    401
    402
    403 请求方式错误
    404 token 错误
    405 异常
 5　访问出错，错误在服务器端
    
"""


# 数据查找成功后返回的代码
def success(res, state="success"):
    return result_data(state, 200, res)


# 数据查询失败，返回访问者错误
def error(res, state="error"):
    return result_data(state, 400, res)


# 请求方式错误
def error_login():
    return result_data("login-from error", 402, {"reason": "please use pc or android or ios login"})


# 请求方式错误
def error_method(res):
    return result_data("request method error", 403, {"reason": res})


# token错误
def error_token():
    return result_data("token error", 404, {"reason": "login expired, please login again"})


# 异常
def error_exception(res):
    return result_data("exception", 405, {"reason": res})


# 返回结果
def result_data(state, code, data):
    res = {"state": state, "code": code, "data": data}
    return HttpResponse(json.dumps(res), content_type="application/json")


# 获取登录token
def get_token(res):
    meta = get_meta(res)
    return meta.get('HTTP_TOKEN')


# 如果登录的设备是其中的几个就可以访问数据
def log_from(res):
    print(res)
    if get_login_from(res) == 'pc' or get_login_from(res) == 'android' or get_login_from(
            res) == 'ios':
        return True
    else:
        return False


# 获取登录设备
def get_login_from(res):
    return get_meta(res).get('HTTP_LOGIN_FROM')


# 获取访问者ip
def get_ip(res):
    return get_meta(res).get('REMOTE_ADDR')


def get_meta(res):
    return res.META
