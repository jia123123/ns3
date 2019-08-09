from django.shortcuts import render
from .serializers import SceneSerializer

from rest_framework import viewsets
from .models import SceneInfo
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class SceneViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = SceneInfo.objects.all()
    serializer_class = SceneSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())     #自定义filter
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
