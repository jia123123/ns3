from .models import NodeInfo, NodeConfig
from rest_framework import viewsets
from .serializers import NodeSerializer, NodeConfigSerializer

from rest_framework.response import Response
from rest_framework import status


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
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # def post(self, request, format=None):
    #     serializer = NodeSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

class NodeConfigViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = NodeConfig.objects.all()
    serializer_class = NodeConfigSerializer


