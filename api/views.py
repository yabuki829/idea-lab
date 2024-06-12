# Create your views here.
from django.http import HttpResponse

from api.models import Idea,Tag
from utils.Ideas import IdeaManager
from django.contrib.auth import get_user_model
from .serializers import IdeaSerializer
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

User = get_user_model()
def index(request):
    manager = IdeaManager()
    data = manager.create_ideas()
    # 各サービスのタイトルと説明を出力
    for service in data['results']:
        title = service['title']
        description = service['explain']
        print("-------------------------------------")
        print("|",title,"|")
        print("-------------------------------------")
        print(description)
        print("-------------------------------------")

        user = User.objects.get(uid="g5KNDdqB")
        Idea.objects.create(title=title,description=description,user=user).save()
    # シリアライザーを作成した方がいいか考える
   
    return HttpResponse(data["results"])


from rest_framework.generics import ListAPIView, RetrieveAPIView



class IdeaListView(ListAPIView):
    # 更新日時で降順に並べ替え
    queryset = Idea.objects.all().order_by("-updated_at")
    serializer_class = IdeaSerializer
    # どのユーザーでもアクセス可能
    permission_classes = (AllowAny,)



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