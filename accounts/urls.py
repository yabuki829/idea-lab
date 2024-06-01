from django.urls import path
from accounts import views

urlpatterns = [
    # ユーザー詳細
    path("user/<uid>/", views.UserDetailView.as_view()),
]