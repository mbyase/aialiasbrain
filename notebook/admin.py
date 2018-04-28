from django.contrib import admin

from notebook.models import DailyDetail


# Register your models here.
class DailyDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'uid', 'userUid', 'gmtCreate', 'gmtModified', 'gmtDelete', 'title',
                    'detail', 'status', 'isDelete']
    # 筛选功能
    list_filter = ['gmtCreate']
    # 搜索功能
    search_fields = ['gmtCreate']
    # 每页显示多少
    list_per_page = 5


admin.site.register(DailyDetail, DailyDetailAdmin)
