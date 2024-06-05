from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

User = get_user_model()


class UserAdminCustom(UserAdmin):
    # 詳細
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "uid",
                    "name",
                    "email",
                    "image",
                    "password",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
    )

    # 追加
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "name",
                    "email",
                    "image",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

    # 一覧
    list_display = (
        "uid",
        "name",
        "email",
        "is_active",
    )

    list_filter = ()
    # 検索
    search_fields = (
        "uid",
        "email",
    )
    list_display_links = ("uid", "name", "email")
    # 編集不可
    readonly_fields = ("uid",)
    # 並び替え
    ordering = ("email",)

admin.site.register(User, UserAdminCustom)