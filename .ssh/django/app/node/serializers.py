from rest_framework import serializers
from .models import NodeInfo, NodeConfig

class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeInfo
        fields = ('node_id', 'ip', 'mac_addr', 'loca_x', 'loca_y', 'psid')

    # 将上述字段，添加到数据库函数
    # def create(self, Validated_data):
    #     return NodeInfo.objects.create(**Validated_data)


class NodeConfigSerializer(serializers.ModelSerializer):
    # node_id = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = NodeConfig
        fields = "__all__"

