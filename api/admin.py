from django.contrib import admin

# Register your models here.
from .models import Idea
from django.contrib import admin
from .models import Idea,Tag,Notice,History,Monetization

class IdeaAdmin(admin.ModelAdmin):
    exclude = ('id',)
    list_display = ('id', 'title', 'description', 'updated_at', 'created_at') 

admin.site.register(Idea, IdeaAdmin)
admin.site.register(Tag)


class NoticeAdmin(admin.ModelAdmin):
    exclude = ('id',)
    list_display = ('id', 'title', 'content', 'created_at') 
admin.site.register(Notice,NoticeAdmin)
admin.site.register(History)
admin.site.register(Monetization)
