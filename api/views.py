# Create your views here.
from django.http import HttpResponse

from api.models import Idea,Tag,Notice
from utils.Ideas import IdeaManager
from django.contrib.auth import get_user_model
from .serializers import IdeaSerializer,NoticeSerializer
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
User = get_user_model()


@csrf_exempt
def index(request):
    data = json.loads(request.body)
    word = data.get('word', '')
    manager = IdeaManager()
    print(word)
    data = manager.create_ideas(word)

        
    print(data["results"])
    return JsonResponse(data["results"])
    
import os

def test(requeat):
    return HttpResponse("テスト")    

from rest_framework.generics import ListAPIView, RetrieveAPIView



class IdeaListView(ListAPIView):
    # 更新日時で降順に並べ替え
    queryset = Idea.objects.all().order_by("-updated_at")
    serializer_class = IdeaSerializer
    # どのユーザーでもアクセス可能にする
    permission_classes = (AllowAny,)

# お知らせの一覧表示
class NoticeListView(ListAPIView):
    
    queryset = Notice.objects.all().order_by("-created_at")
    serializer_class = NoticeSerializer
    
    permission_classes = (AllowAny,)



class IdeaDetailView(RetrieveAPIView):
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer
    permission_classes = (AllowAny,)
    lookup_field = "id"


class IdeaPostViewSet(ModelViewSet):
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer
    lookup_field = "id" 

    def perform_create(self, serializer, **kwargs):
        # 投稿を作成するユーザーを設定
        print("ここまでおk")
        print(self.request.data)
        tag_title = self.request.data.get('tag')  # リクエストからタグのタイトルを取得
        tag, created = Tag.objects.get_or_create(title=tag_title)  # タグが存在しなければ新しく作成する
        serializer.save(user=self.request.user, tag=tag)  # 