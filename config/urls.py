from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls")),
    
    path("api/auth/", include("djoser.urls")),
    path("api/auth/", include("djoser.urls.jwt")),

    path('api/', include('api.urls')),
    
]
