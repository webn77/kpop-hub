from django.contrib import admin

from .models import Notice


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_pinned', 'view_count', 'created_at')
    list_filter = ('is_pinned',)
    search_fields = ('title', 'content', 'author__username')
    readonly_fields = ('view_count', 'created_at', 'updated_at')
    ordering = ('-is_pinned', '-created_at')
