from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Post, Like, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'view_count', 'like_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'content', 'author__username')
    readonly_fields = ('view_count', 'created_at', 'updated_at')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    list_filter = ('created_at',)


@admin.register(Comment)
class CommentAdmin(MPTTModelAdmin):
    list_display = ('author', 'post', 'content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'author__username')
