from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register("posts", views.IdeaPostViewSet)

urlpatterns = [
    path('test/', views.index, name="index"),
    path('generate/idea/', views.index, name="index"),
    path('idea/list/', views.IdeaListView.as_view()),
    path('idea/<id>/', views.IdeaDetailView.as_view()),
    path('news/', views.NoticeListView.as_view()),
    path("", include(router.urls)),
]
