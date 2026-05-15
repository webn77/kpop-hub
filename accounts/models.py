from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model for KPOP HUB."""

    class Role(models.TextChoices):
        USER = 'USER', '일반 사용자'
        ADMIN = 'ADMIN', '관리자'

    nickname = models.CharField(max_length=50, unique=True, blank=True)
    profile_img = models.ImageField(upload_to='profiles/', blank=True, null=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.USER)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = '사용자 목록'

    def __str__(self):
        return self.nickname or self.username
