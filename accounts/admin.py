from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'nickname', 'role', 'is_staff', 'created_at')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'nickname')
    ordering = ('-created_at',)

    fieldsets = BaseUserAdmin.fieldsets + (
        ('추가 정보', {
            'fields': ('nickname', 'profile_img', 'role', 'bio', 'created_at'),
        }),
    )
    readonly_fields = ('created_at',)
