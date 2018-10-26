from django.contrib import admin
from login.models import User
# Register your models here.

#将模型注册到admin站点
admin.site.register(User)      #通知 admin 管理工具为User模型提供界面，访问http://127.0.0.1:8000/admin/，这个页面会出现LOGIN下的用户模型