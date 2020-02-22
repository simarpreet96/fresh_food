from django.contrib import admin
from .models import Post, Comment
from django.utils.html import format_html
from django.db import models

class CommentInline(admin.TabularInline):
    model= Comment

class PostAdmin(admin.ModelAdmin):

    def image_post(self,obj):
        return format_html('<img src="/media/{}" width="150" height="150"/>'.format(obj.image))
    image_post.short_description='Image'

    def make_published(self, request, queryset):
        queryset.update(status='p')
    make_published.short_description ="Mark selected stories as published"
    inlines = [CommentInline]
    list_display = ['author','title','created_date','published_date','image_post','status']
    search_fields = ['title']
    list_filter = ['author','created_date','title',]
    actions=['make_published']

admin.site.register(Post,PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display=['author','text','created_date']
    list_filter=['created_date']

admin.site.register(Comment,CommentAdmin)
