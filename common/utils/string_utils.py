# coding=utf-8
# author HerbLee
# 字符转换工具类

# 转换成字符串
def obj2Str(data):
    try:
        return str(data)
    except Exception as e:
        return ""

def obj2Boolean(data):
    try:
        return bool.parseBoolean(data)
    except Exception as e:
        return False