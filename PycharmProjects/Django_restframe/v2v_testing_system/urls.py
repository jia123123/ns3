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


from django.urls import include, path
from rest_framework import routers
from app.node.views import NodeViewSet, NodeConfigViewSet
from app.task.views import TaskViewSet
from app.user.views import UserViewSet
from app.scene.views import SceneViewSet
from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'nodes', NodeViewSet, basename="nodes")
router.register(r'configs', NodeConfigViewSet, basename="configs")
router.register(r'tasks', TaskViewSet, basename='tasks')
router.register(r'users', UserViewSet, basename='users')
router.register(r'scenes', SceneViewSet, basename='scenes')
# router.register(r'node/(?P<scene>[0-9]+)', NodeViewSet.as_view({'get':'scenefilter'}))
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),

]