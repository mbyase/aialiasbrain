from django.contrib import admin

# Register your models here.

from django.contrib import admin
from account.models import *


class AccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'nickname', 'email', 'mobile', 'motto', 't_create', 'last_login']
    list_filter = ['t_create']
    search_fields = ['name']
    list_per_page = 10


admin.site.register(Account, AccountAdmin)
