from .models import SceneInfo
from rest_framework import serializers


class SceneSerializer(serializers.ModelSerializer):
    class Meta:
        model = SceneInfo
        fields = "__all__"