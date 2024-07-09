from rest_framework import serializers
from accounts.serializers import UserSerializer
from config.utils import Base64ImageField
from rest_framework.viewsets import ModelViewSet
from api.models import Idea,Notice,Tag,Monetization



class IdeaSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
   
    user = UserSerializer(read_only=True)
    tag = serializers.CharField()
    class Meta:
        model = Idea
        fields = "__all__"



class MonetizeSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    description = serializers.CharField()
    idea = IdeaSerializer(read_only=True)
    class Meta:
        model = Monetization
        fields = "__all__"


class NoticeSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = Notice
        fields = "__all__"

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"