from django.db import models
# from ..user.models import User

class Task(models.Model):
    task_id = models.AutoField(primary_key=True)    #任务id
    user = models.ForeignKey('user.User', related_name='task', on_delete=models.CASCADE, null=False)                  #关联用户id
    scene = models.CharField(max_length=50)         #任务场景
    priority = models.IntegerField()                #任务优先级
    start_time = models.DateTimeField()             #任务开始时间

    def __str__(self):
        return self.task_id