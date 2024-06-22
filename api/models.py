from django.conf import settings
from django.db import models
from hashids import Hashids
# Create your models here.
import time

class Tag(models.Model):
    title = models.CharField(max_length=255)
    def __str__(self):
        return self.title

class Idea(models.Model):
    id = models.CharField(max_length=30, unique=True, primary_key=True)
    title = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="ユーザー", on_delete=models.CASCADE
    )
    tag = models.ForeignKey(Tag,on_delete=models.CASCADE)
    description = models.TextField()
    updated_at = models.DateTimeField("更新日", auto_now=True)
    created_at = models.DateTimeField("作成日", auto_now_add=True)

    pre_idea = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title


    # 保存するときに現在時刻をもとにハッシュ値を作成する
    def save(self, *args, **kwargs):
        if not self.id:
            hashids = Hashids(salt="xRXSMT8XpzdUbDNM9qkv6raerwre3223", min_length=8)
            self.id = hashids.encode(int(time.time() * 1000))
        super(Idea, self).save(*args, **kwargs)



class Notice(models.Model):
    id = models.CharField(max_length=5, unique=True, primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField("作成日", auto_now_add=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.id:
            hashids = Hashids(salt="xRXSMT8XpzdUbDNM9qkv6raerwre3223", min_length=5)
            self.id = hashids.encode(int(time.time() * 1000))
        super(Notice, self).save(*args, **kwargs)