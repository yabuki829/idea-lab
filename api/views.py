# Create your views here.
from django.http import HttpResponse

from api.models import Idea,Tag
from utils.Ideas import IdeaManager
from django.contrib.auth import get_user_model
from .serializers import IdeaSerializer
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

        
    # シリアライザーを作成した方がいいか考える
    print(data["results"])
    # return HttpResponse(data["results"])
    return JsonResponse(data["results"])
    return JsonResponse({'title': '知恵の泉', 'discription': '「知恵の泉」は、勉強や遊びの要素を組み合わせた新しい学習体験を提供するサービスです。ユーザーは、問題解決やクイズ形式のゲームを通じて学習し、知識を深めることができます。また、他のユーザーと競い合ったり、協力したりしながら楽しみながら成長できる環境を提供しています。知識獲得だけでなく、頭の体操やクリエイティブな思考力の向上にも役立つサービスです。'})

import os
def test(requeat):

    return HttpResponse("テスト")    

from rest_framework.generics import ListAPIView, RetrieveAPIView



class IdeaListView(ListAPIView):
    # 更新日時で降順に並べ替え
    queryset = Idea.objects.all().order_by("-updated_at")
    serializer_class = IdeaSerializer
    # どのユーザーでもアクセス可能
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
        tag, created = Tag.objects.get_or_create(title=tag_title)  # タグが存在しなければ新しく作成
        serializer.save(user=self.request.user, tag=tag)  # 