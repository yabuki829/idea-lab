from rest_framework import serializers
from django.contrib.auth import get_user_model



User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    uid = serializers.CharField(read_only=True)


    class Meta:
        model=User
        fields="__all__"