
from notebook.models import *
import json
from common.utils import res_utils, string_utils, utils, redis_cache, date_utils


# Create your views here.

# 添加条目
def createitem(request):
    if not res_utils.isPost(request):
        return res_utils.error_method("please use post method")
    # 获取token
    token = res_utils.get_token(request)
    # 判断token存在不存在确定用户是否存在
    if not redis_cache.is_exist(token):
        return res_utils.error_token()
    # 获取数据
    data = request.POST
    try:
        title = string_utils.obj2Str(data.get('title', 'none'))
        detail = string_utils.obj2Str(data.get('detail', 'none'))
        useruid = redis_cache.read(token).get('uid')
        DailyDetail.superuser.create(useruid, title, detail)
        return res_utils.success("添加成功")
    except Exception  as e:
        return res_utils.error_exception(e)


# 获取所有信息
def getModel(request):
    if not res_utils.isGet(request):
        return res_utils.error_method("please use get method")
    try:
        token = res_utils.get_token(request)
        # 判断token存在不存在确定用户是否存在
        if not redis_cache.is_exist(token):
            return res_utils.error_token()
        account = redis_cache.read(token)
        useruid = account.get('uid')
        username = account.get('username')
        if username == 'admin':
            res = DailyDetail.superuser.getadmin()
        else:
            res = DailyDetail.superuser.get(useruid)
        result = json.loads(res)
        return res_utils.success(result)
    except Exception as e:
        return res_utils.error(e)


# 获取今天所有信息
def getToday(request):
    if not res_utils.isGet(request):
        return res_utils.error_method("please use get method")
    try:
        token = res_utils.get_token(request)
        # 判断token存在不存在确定用户是否存在
        if not redis_cache.is_exist(token):
            return res_utils.error_token()
        account = redis_cache.read(token)
        useruid = account.get('uid')
        username = account.get('username')
        if username == 'admin':
            res = DailyDetail.superuser.getadmintoday()
        else:
            res = DailyDetail.superuser.gettoday(useruid)
        result = json.loads(res)
        return res_utils.success(result)
    except Exception as e:
        return res_utils.error(e)


def updateStatus(request):
    if not res_utils.isPost(request):
        return res_utils.error_method("please use post method")
    try:
        # 获取token
        token = res_utils.get_token(request)
        # 判断token存在不存在确定用户是否存在
        if not redis_cache.is_exist(token):
            return res_utils.error_token()
        # 获取数据
        data = request.POST
        uid = string_utils.obj2Str(data.get('uid', 'wo'))
        DailyDetail.superuser.updateStatus(uid, 1)
        return res_utils.success("")
    except Exception as e:
        return res_utils.error(e)


def delete(request):
    if not res_utils.isPost(request):
        return res_utils.error_method("please use post method")
    try:
        # 获取token
        token = res_utils.get_token(request)
        # 判断token存在不存在确定用户是否存在
        if not redis_cache.is_exist(token):
            return res_utils.error_token()
        # 获取数据
        data = request.POST
        uid = string_utils.obj2Str(data.get('uid', 'wo'))
        DailyDetail.superuser.delete(uid)
        return res_utils.success("")
    except Exception as e:
        return res_utils.error(e)