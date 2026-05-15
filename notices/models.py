from django.conf import settings
from django.db import models


class Notice(models.Model):
    """공지사항 모델."""

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='작성자',
    )
    title = models.CharField(max_length=200, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    is_pinned = models.BooleanField(default=False, verbose_name='상단 고정')
    view_count = models.PositiveIntegerField(default=0, verbose_name='조회수')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        ordering = ['-is_pinned', '-created_at']
        verbose_name = '공지사항'
        verbose_name_plural = '공지사항 목록'

    def __str__(self):
        return self.title
