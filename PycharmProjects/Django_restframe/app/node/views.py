from .models import NodeInfo, NodeConfig
from rest_framework import viewsets
from .serializers import NodeSerializer, NodeConfigSerializer
from rest_framework.response import Response
from rest_framework import status, generics
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

class NodeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = NodeInfo.objects.all()
    serializer_class = NodeSerializer

    def retrieve(self, request, *args, **kwargs):
        '''重写单个节点的返回，不返回逻辑删除了的对象'''
        instance = self.get_object()
        if instance.is_delete == False:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response(status.HTTP_404_NOT_FOUND)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(NodeInfo.objects.filter(is_delete=False))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    # 根据物理场景id做节点过滤，输出某一场景下所有节点信息
    #detail属性为false表明该函数的调用不需要pk值，若为True则url地址为http://127.0.0.1:8000/nodes/1/scene/?scene_id=1
    @action(detail=False)
    # request不可省，表示查询参数的输入
    def scene(self,request):
        queryset = NodeInfo.objects.all()
        #通过url查询参数进行定义
        scene_id=self.request.query_params.get('scene_id', None)
        if scene_id is not None:
            queryset = queryset.filter(scene_id=scene_id)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(status.HTTP_404_NOT_FOUND)


class NodeConfigViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = NodeConfig.objects.all()
    serializer_class = NodeConfigSerializer


