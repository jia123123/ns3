from django.db import models

class User(models.Model):
    user_name = models.CharField(max_length=20)             #用户名
    user_pwd = models.CharField(max_length=20)              #密码
    email = models.EmailField(default='')                   #email

    def __str__(self):
        return self.user_name