# coding=utf-8
from django.db import models

# Create your models here.
from django.db import models
from django.core import serializers
from common.utils import utils, string_utils, date_utils


# 用户信息管理
class AccountManager(models.Manager):
    def get_queryset(self):
        return super(AccountManager, self).get_queryset().filter(is_delete=False)

    def create(self, account, password):
        """
            创建新用户
        :param code: 0代表邮箱 1代表手机
        :param data: 邮箱或手机号码
        :param password: 密码
        :return: none
        """
        swap = Account()
        if utils.check_email(account):
            swap.email = account
        else:
            swap.mobile = account
        swap.password = password
        swap.uid = utils.uid()
        swap.save()

    # 获取密码
    def get_password(self, account):
        result = {}
        if self.filter(email=account).exists():
            item = self.filter(email=account)[0]
            result['password'] = item.password
            result['uid'] = item.uid
        elif self.filter(mobile=account).exists():
            item = self.filter(mobile=account)[0]
            result['password'] = item.password
            result['uid'] = item.uid
        else:
            result['password'] = ''
            result['uid'] = ''
        return result

    # 获取账户信息
    def get_account(self, uid):
        item = self.filter(uid=uid)[0]
        result = {'uid': item.uid, 'name': item.name,
                  'nickname': item.nickname, 'gender': item.gender,
                  'email': item.email,
                  'mobile': item.mobile, 'motto': item.motto,
                  'icon': item.icon, 'address': item.address,
                  'birthday': item.birthday}
        return result


# 用户信息表
class Account(models.Model):
    uid = models.CharField(max_length=32)
    t_create = models.DateTimeField(auto_now=False, auto_now_add=True)
    t_modify = models.DateTimeField(auto_now=True, auto_now_add=False)
    t_delete = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    is_delete = models.BooleanField(default=False)
    name = models.CharField(max_length=32, null=True, blank=True)
    nickname = models.CharField(max_length=32, null=True, blank=True)
    gender = models.BooleanField(default=False)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=11, null=True, blank=True)
    motto = models.CharField(max_length=200, null=True, blank=True)
    icon = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    last_login = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    birthday = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    superuser = AccountManager()
