from django.db import models

# Create your models here.


class SceneInfo(models.Model):
    """
    场景信息
    """
    # 场景编号
    scene_id = models.AutoField(primary_key=True, verbose_name='场景编号')
    name = models.CharField(max_length=20, unique=True)
    img = models.ImageField(upload_to='images', null=True)
    # 场景描述信息
    desc = models.TextField(default="", verbose_name='场景描述', null=True)

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        """重写数据库删除方法实现逻辑删除"""
        self.is_delete = True
        self.save()