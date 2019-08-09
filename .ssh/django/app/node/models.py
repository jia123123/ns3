from django.db import models
# from ..task.models import Task
import django.utils.timezone as timezone

class NodeInfo(models.Model):
    """
    节点信息
    """
    NODE_STATUS_CHOICES = [
        ('OFFLINE', 'offline'),
        ('IDLE', 'idle'),
        ('BUSY', 'busy'),
    ]


    # 节点编号
    node_id = models.AutoField(primary_key=True)
    # 节点IP
    ip = models.GenericIPAddressField()
    # 节点MAC地址
    mac_addr = models.CharField(max_length=20)
    # 节点状态
    node_status = models.CharField(choices=NODE_STATUS_CHOICES, max_length=20, blank=True, default='IDLE')
    # 节点位置横坐标
    loca_x = models.IntegerField(default=0)
    # 节点位置纵坐标
    loca_y = models.IntegerField(default=0)
    # 节点版本号
    version = models.CharField(max_length=10, default="0.0.1")
    # 节点加入时间
    created = models.DateTimeField(default=timezone.now)
    # 服务ID
    psid = models.IntegerField(default=0)
    # 逻辑删除
    is_delete = models.BooleanField(default=False, blank=True, verbose_name='逻辑删除')

    def __str__(self):
        return self.mac_addr

    def delete(self, using=None, keep_parents=False):
        """重写数据库删除方法实现逻辑删除"""
        self.is_delete = True
        self.save()


class NodeConfig(models.Model):
    TX = 'T'
    RX = 'R'
    TR_STATUS_CHOICES = [
        (TX, 'transmitting'),
        (RX, 'receiving'),
    ]

    node = models.ForeignKey('node.NodeInfo', related_name='node_config', on_delete=models.CASCADE, null=False, default=0)
    task = models.ForeignKey('task.Task', related_name='node_config', on_delete=models.CASCADE, null=False, default=0)
    tr_status = models.CharField(choices=TR_STATUS_CHOICES, max_length=20)
    # message = models.CharField(max_length=3000)
    radio = models.IntegerField()
    power = models.IntegerField()
    rate = models.CharField(max_length=20)
    channel = models.IntegerField()
    des_mac_addr = models.CharField(max_length=20)
    psid = models.IntegerField()
    payload = models.CharField(max_length=20)
    pl_length = models.IntegerField()
    periodic = models.BooleanField()
    times = models.IntegerField()
    tx_timeslot = models.IntegerField()





















