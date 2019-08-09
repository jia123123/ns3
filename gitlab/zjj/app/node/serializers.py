from rest_framework import serializers
from .models import NodeInfo, NodeConfig


from rest_framework import serializers
from .models import NodeInfo

class NodeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeInfo
        fields = ('node_id', 'ip', 'mac_addr', 'loca_x', 'loca_y', 'scene')

    def to_representation(self, data):
        """
        重写此方法以实现返回内容的控制
        Input：data, 模型对象实例
        Output: 返回的序列化内容
        """
        res = {
            "node_id": data.node_id,
        }
        return res


class NodeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeInfo
        fields = "__all__"


class NodeConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeConfig
        fields = "__all__"


class NodeStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeInfo
        fields = ('node_status',)