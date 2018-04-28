# Create your views here.
import json

from django.http import HttpResponse
from account.models import *
from common.utils import redis_cache, res_utils, string_utils, utils


def check_account(request):
    """
        检测账户是否可用
    :param request:
    :param account: 被检测的账号
    :return: 200为可用,其余为不可用
    """
    if res_utils.isPost(request):
        data = request.POST
        try:
            account = string_utils.obj2Str(data.get('account', ''))
            if Account.superuser.filter(email=account).exists() or Account.superuser.filter(
                    mobile=account).exists():
                return res_utils.error({"reason": "account already exists"}, "check error")
            else:
                return res_utils.success({"info": "account available"})
        except Exception as e:
            return res_utils.error_exception(e)
    else:
        return res_utils.error_method("please use post")


# 注册
def register(request):
    """
        用户注册
    :param request:
    :param flag: 标记0 为邮箱注册，　1为手机注册
    :param account: 账号
    :param password: 密码
    :return: 200 注册成功，其他均为错误
    """
    if res_utils.isPost(request):
        data = request.POST
        try:
            # flag = string_utils.obj2Str(data.get('flag', ''))

            account = string_utils.obj2Str(data.get('account', ''))
            passwd = string_utils.obj2Str(data.get('password', ''))
            password = utils.make_passwd(passwd)

            if utils.check_email(account) and not Account.superuser.filter(email=account).exists():
                Account.superuser.create(account, password)
                return res_utils.success({"info": "register success, please login again"},
                                         "register success")
            elif utils.check_mobil(account) and not Account.superuser.filter(mobile=account).exists():
                Account.superuser.create(account, password)
                return res_utils.success({"info": "register success, please login again"},
                                         "register success")
            else:
                return res_utils.error({"reason": "request parameter error"})
        except Exception as e:
            return res_utils.error_exception(e)
    else:
        return res_utils.error_method("please use post")


# 登录
def login(request):
    if not res_utils.isPost(request):
        return res_utils.error_method("please use post method")
    if not res_utils.log_from(request):
        return res_utils.error_login()
    data = request.POST
    try:
        account = string_utils.obj2Str(data.get('account', ''))
        passwd = string_utils.obj2Str(data.get('password', ''))
        password = Account.superuser.get_password(account).get('password')
        # 登录成功
        if not utils.check_passwd(passwd, password):
            return res_utils.error({"reason": "account or password error"}, "login error")

        uid = Account.superuser.get_password(account).get('uid')
        pre = res_utils.get_login_from(request)
        token = redis_cache.get_token(pre)
        # 如果是同一设备登录则清楚token
        val = redis_cache.read(account)
        if val is not None:
            if redis_cache.is_equal(val, pre):
                redis_cache.remove(val)

        redis_cache.save(account, token)
        redis_cache.save(token, uid)  # 修改下,改成保存对象
        return res_utils.success({"token": token}, "login success")
    except Exception as e:
        return res_utils.error_exception(e)


# 获取用户信息
def get_account(request):
    if not res_utils.isGet(request):
        return res_utils.error_method("please use get method")
    if not res_utils.log_from(request):
        return res_utils.error_login()
    try:
        token = string_utils.obj2Str(res_utils.get_token(request))
        # 如果登录设备不相符也不给返回数据
        if not redis_cache.verification_token(request):
            return res_utils.error_token()
        uid = redis_cache.read(token)
        if uid is None:
            return res_utils.error_token()
        res = Account.superuser.get_account(uid)
        return res_utils.success(res)
    except Exception as e:
        return res_utils.error_exception(e)
