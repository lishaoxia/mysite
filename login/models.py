from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    gender = (
        (u'M',u'男'),
        (u'F',u'女'),
    )
    sex = models.CharField(max_length=32,choices=gender,default='男')
    c_time = models.DateTimeField(auto_now_add=True)

#   使用__str__帮助人性化显示对象信息,__str__()方法告诉 Python 如何将对象以 str 的方式显示出来。 所以， 为每个模型类添加了__str__()方法。
    def __str__(self):
        return self.username

#   定义元数据
    class Meta:
        ordering = ['c_time']           #按创建时间排序
        verbose_name = '用户'           #给模型起一个可读的名字
        verbose_name_plural = '用户'    #同上，复数形式