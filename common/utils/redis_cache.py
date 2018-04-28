# coding=utf-8
# author HerbLee
# 读写缓存工具类

from django.conf import settings
from django.core.cache import cache
from common.utils.utils import uid
from common.utils import res_utils
from common.utils import string_utils


# 写入缓存
def save(key, value, timeout=settings.REDIS_TIMEOUT):
    cache.set(key, value, timeout)


# 　读取缓存
def read(key):
    return cache.get(key)


def remove(key):
    cache.delete(key)


def get_token(pre):
    if pre == 'android':
        return "ad" + uid()
    elif pre == 'pc':
        return "pc" + uid()
    elif pre == 'ios':
        return "is" + uid()
    else:
        return "00" + uid()


def get_pre(pre):
    return str(pre)[0:2]


def is_equal(pre, data):
    if get_pre(pre) == "ad" and data == "android":
        return True
    if get_pre(pre) == "pc" and data == "pc":
        return True
    if get_pre(pre) == "is" and data == "ios":
        return True
    return False


def verification_token(request):
    token = string_utils.obj2Str(res_utils.get_token(request))
    data = string_utils.obj2Str(res_utils.get_login_from(request))
    return is_equal(token, data)
