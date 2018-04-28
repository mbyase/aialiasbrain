from django.db import models

from common.utils import utils,date_utils,string_utils
from django.core import serializers

import datetime


# 每日变更内容
class DailyDetailManager(models.Manager):

    def get_queryset(self):
        return super(DailyDetailManager, self).get_queryset().filter(isDelete=False)

    def create(self, userUid, title, detail):
        swap = DailyDetail()
        swap.uid = utils.uid()
        swap.userUid = string_utils.obj2Str(userUid)
        swap.title = title
        swap.detail = detail
        swap.status = 0
        swap.save()
        return swap

    def get(self, userUid):
        item = self.filter(userUid=userUid).order_by("-gmtCreate")
        return serializers.serialize('json', item)

    def gettoday(self, userUid):
        start = date_utils.starttime()['start']
        end = date_utils.starttime()['end']
        item = self.filter(userUid=userUid, gmtCreate__range=[start, end]).order_by("-gmtCreate")
        return serializers.serialize('json', item)

    def getadmintoday(self):
        start = date_utils.starttime()['start']
        end = date_utils.starttime()['end']
        item = self.filter(gmtCreate__range=[start, end]).order_by("-gmtCreate")
        return serializers.serialize('json', item)

    def getadmin(self):
        item = self.order_by("-gmtCreate")
        return serializers.serialize('json', item)

    def updateStatus(self, uid, status):
        gmtDele = datetime.datetime.now()
        res = self.filter(uid=uid).update(status=status, gmtModified=gmtDele)

    def delete(self, uid):
        # gmtDele = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        gmtDele = datetime.datetime.now()
        res = self.filter(uid=uid).update(isDelete=True, gmtDelete=gmtDele)


class DailyDetail(models.Model):
    uid = models.CharField(max_length=64, default="woshishei")
    userUid = models.CharField(max_length=64, default="woshishei")
    gmtCreate = models.DateTimeField(auto_now=False, auto_now_add=True)
    gmtModified = models.DateTimeField(auto_now=True, auto_now_add=False)
    gmtDelete = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    title = models.CharField(max_length=64, default="woshishei")
    detail = models.CharField(max_length=200, default="woshishei")
    isDelete = models.BooleanField(default=False)
    status = models.IntegerField(default=0)
    superuser = DailyDetailManager()
