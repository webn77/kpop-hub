from django.db import models
from django.conf import settings
from django.urls import reverse


class Event(models.Model):
    class EventType(models.TextChoices):
        COMEBACK = 'comeback', '컴백'
        CONCERT = 'concert', '콘서트'
        FANSIGN = 'fansign', '팬사인회'
        OTHER = 'other', '기타'

    title = models.CharField(max_length=200, verbose_name='제목')
    description = models.TextField(blank=True, verbose_name='설명')
    event_date = models.DateField(verbose_name='일정 날짜')
    event_type = models.CharField(
        max_length=20,
        choices=EventType.choices,
        default=EventType.OTHER,
        verbose_name='일정 유형',
    )
    artist = models.CharField(max_length=100, blank=True, verbose_name='아티스트')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='events',
        verbose_name='작성자',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='등록일')

    class Meta:
        ordering = ['event_date']
        verbose_name = '일정'
        verbose_name_plural = '일정 목록'

    def __str__(self):
        return f'[{self.get_event_type_display()}] {self.title} ({self.event_date})'

    def get_absolute_url(self):
        return reverse('events:detail', kwargs={'pk': self.pk})
