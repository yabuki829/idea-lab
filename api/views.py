# Create your views here.
from django.http import HttpResponse

from api.models import Idea,Tag,Notice,History
from utils.Ideas import IdeaManager
from django.contrib.auth import get_user_model
from .serializers import IdeaSerializer,NoticeSerializer,TagSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework import status
from datetime import datetime
User = get_user_model()


# 全部APIViewに書き換える


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


class NoticeDetailView(RetrieveAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = (AllowAny,)
    lookup_field = "id"

# tagの一覧表示
class TagListView(ListAPIView):
    
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    
    permission_classes = (AllowAny,)




class TagIdeaListView(ListAPIView):
    serializer_class = IdeaSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        tag_title = self.kwargs['tag_title']
        return Idea.objects.filter(tag__title=tag_title)

# userのアイデアの一覧を取得する
class UserIdeaListView(ListAPIView):
    serializer_class = IdeaSerializer
    permission_classes = (AllowAny,)
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        print("user_id",user_id)
        return Idea.objects.filter(user__uid=user_id)
    

# ログインしているuserがリクエストしてきた場合
# 閲覧履歴を作成する
# 2回目からは最後に閲覧した時刻を保存する
# viewsは最初の一回だけカウントする


class IdeaDetailView(APIView):    
    permission_classes = (AllowAny,)
    def get(self, request, id, format=None):

        idea = Idea.objects.get(id=id)
        serializer = IdeaSerializer(idea)
        
        # ログインしている場合は閲覧履歴を作成する
        
        if request.user.is_authenticated:
            history,created = History.objects.get_or_create(user=request.user, idea=idea)
            print(self.request.user)
            if created: 
                idea.views += 1    
            if history:
                history.timestamp = datetime.now()
                history.save()  

        return Response(serializer.data)

class IdeaPostViewSet(ModelViewSet):
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer
    lookup_field = "id" 

    def perform_create(self, serializer, **kwargs):
        # 投稿を作成するユーザーを設定
        print("ここまでおk")
        print(self.request.user.is_authenticated)
        
        tag_title = self.request.data.get('tag')  # リクエストからタグのタイトルを取得
        tag, created = Tag.objects.get_or_create(title=tag_title)  # タグが存在しなければ新しく作成する
        serializer.save(user=self.request.user, tag=tag)  # 


        # ログインをしていれば
        # history から 10件取得する
        # その投稿のタグの上位５件を取得する
        # ランダムで1件選ぶ。
        # そのタグの中で1週間の中で閲覧数の多い自分の投稿を除いた投稿を返す
        
        
        # ログインしていなければ
        # viewsが多いものを5件返す
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Count
from collections import Counter

import random
import collections
class RecommendAPIView(APIView):
    def get(self,request):
        if request.user.is_authenticated:
            one_week_ago = timezone.now() - timedelta(days=7)
            print(History.objects.filter(user=request.user))
            user_historys = History.objects.filter(timestamp__gte=one_week_ago,user=request.user)
            print("閲覧履歴",user_historys)
            top_historys = user_historys.annotate(num_views=Count('idea__history')).order_by('-num_views')[:10]
            print("閲覧履歴",top_historys)

            all_tags = []
            for history in top_historys:
                all_tags.append(history.idea.tag)

       

            print(all_tags)
            # タグの出現回数を数えて、上位2件を取得
            top_tags = Counter(all_tags).most_common(1)
            print("タグの上位",top_tags)
            random_tag = random.choice(top_tags)[0]
            print("ランダムで選ばれたタグ",random_tag)
            # タグでフィルター
            related_ideas = Idea.objects.filter(tag__title=random_tag)
            print("フィルターされたアイデア",related_ideas)
            # 自分の投稿を除く
            related_ideas = related_ideas.exclude(user=request.user)
            print("自分の投稿を除いたもの",related_ideas)
            # viewsでソートする
            related_ideas = related_ideas.annotate(num_views=Count('history__idea')).order_by('-num_views')

            serializer = IdeaSerializer(related_ideas, many=True)
            print(related_ideas)
            return Response(serializer.data)

            pass
        else:
            top_ideas = Idea.objects.annotate(num_views=Count('history')).order_by('-num_views')[:5]
            print(top_ideas)
        