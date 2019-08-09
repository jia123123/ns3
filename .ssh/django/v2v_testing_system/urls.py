"""v2v_testing_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path
# from django.conf.urls import url
#
#
# from app.node.views import NodeViewSet
# # from rest_framework.documentation import include_docs_urls
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     #节点信息
#     # url(r'docs/', include_docs_urls(title="yxh")),
#     url(r'nodes/', NodeViewSet.as_view()),
#
# ]

from django.urls import include, path
from rest_framework import routers
from app.node.views import NodeViewSet, NodeConfigViewSet
from app.task.views import TaskViewSet
from app.user.views import UserViewSet

from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'nodes', NodeViewSet)
router.register(r'configs', NodeConfigViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'users', UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]