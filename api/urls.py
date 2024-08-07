from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views

# router = routers.DefaultRouter()
# router.register("posts", views.IdeaPostViewSet)

urlpatterns = [
    path('test/', views.test, name="test"),
    
    # path('generate/idea/', views.index, name="index"),
    path('posts/', views.IdeaPostAPIView.as_view(), name="index"),
    path('generate/idea/', views.IdeaGenerateAPIView.as_view(), name="index"),
    path("generate/monetization/",views.IdeaMonetizeAPIView.as_view(),name="monetization"),
    path('idea/list/', views.IdeaListView.as_view()),
    path('idea/recommend/', views.RecommendAPIView.as_view()),
    path('idea/<id>/', views.IdeaDetailView.as_view()),
    path('user/<user_id>/idea/', views.UserIdeaListView.as_view()),
    path('news/', views.NoticeListView.as_view()),
    path('news/<id>/', views.NoticeDetailView.as_view()),
    path('tags/', views.TagListView.as_view()),
    path('tags/<str:tag_title>/', views.TagIdeaListView.as_view(), name='tag-idea-list'),
    # path("", include(router.urls)),
]
