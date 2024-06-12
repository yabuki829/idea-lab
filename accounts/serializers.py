from rest_framework import serializers
from django.contrib.auth import get_user_model
from config.utils import Base64ImageField

User = get_user_model()


# ユーザー情報のシリアライザー
class UserSerializer(serializers.ModelSerializer):
    #
    uid = serializers.CharField(read_only=True)
    
    image = Base64ImageField(
        max_length=None, use_url=True, required=False, allow_null=True
    )

    class Meta:
        model = User
        fields = ["uid","name","image","introduction","email"]